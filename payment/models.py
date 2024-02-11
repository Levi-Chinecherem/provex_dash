# payment/models.py
from django.db import models
from accounts.models import CustomUser
from django.db.models import Sum
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import timedelta
from decimal import Decimal

User = CustomUser

class USDT_TRC20(models.Model):
    coin_name = models.CharField(max_length=255)
    qr_code = models.ImageField(upload_to='usdt_trc20_qrcodes/')
    wallet_address = models.CharField(max_length=255)
    network = models.CharField(max_length=50)

    def __str__(self):
        return self.coin_name

    class Meta:
        verbose_name = "USDT TRC20"
        verbose_name_plural = "USDT TRC20"

class USDT_ERC20(models.Model):
    coin_name = models.CharField(max_length=255)
    qr_code = models.ImageField(upload_to='usdt_erc20_qrcodes/')
    wallet_address = models.CharField(max_length=255)
    network = models.CharField(max_length=50)

    def __str__(self):
        return self.coin_name

    class Meta:
        verbose_name = "USDT ERC20"
        verbose_name_plural = "USDT ERC20"

class BTC(models.Model):
    coin_name = models.CharField(max_length=255)
    qr_code = models.ImageField(upload_to='btc_qrcodes/')
    wallet_address = models.CharField(max_length=255)
    network = models.CharField(max_length=50)

    def __str__(self):
        return self.coin_name

    class Meta:
        verbose_name = "BTC"
        verbose_name_plural = "BTC"

class Funds(models.Model):
    ACCOUNT_TYPES = [
        ('USDT_TRC20', 'USDT TRC20'),
        ('USDT_ERC20', 'USDT ERC20'),
        ('BTC', 'BTC'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    account_type = models.CharField(max_length=20, choices=ACCOUNT_TYPES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    confirmed = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        # Override save method to update AccountSummary when funding is approved
        super().save(*args, **kwargs)
        if self.confirmed:
            AccountSummary.update_summary(self.user, self.account_type, self.amount)

    def __str__(self):
        return f"{self.user.username} - {self.account_type} - {self.amount}"

    class Meta:
        verbose_name = "Funds"
        verbose_name_plural = "Funds"


class AccountSummary(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    account_type = models.CharField(max_length=20, choices=Funds.ACCOUNT_TYPES, unique=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.user.username} - {self.account_type} - {self.total_amount}"

    class Meta:
        verbose_name = "Account Summary"
        verbose_name_plural = "Account Summaries"

    @classmethod
    def update_summary(cls, user, account_type, amount):
        # Update or create an AccountSummary entry based on approved funds
        funds_total = Funds.objects.filter(user=user, account_type=account_type, confirmed=True).aggregate(sum_amount=Sum('amount'))['sum_amount'] or 0

        # Try to get an existing summary for the user and account_type
        summary, created = cls.objects.get_or_create(user=user, account_type=account_type)

        if created or amount > 0:
            # Update the existing summary if created or amount is greater than 0
            summary.total_amount = funds_total
            summary.save()


class InvestmentPlan(models.Model):
    PLAN_TYPES = [
        ('BASIC', 'Basic'),
        ('STANDARD', 'Standard'),
        ('PLATINUM', 'Platinum'),
        ('PREMIUM', 'Premium'),
    ]

    plan_type = models.CharField(max_length=20, choices=PLAN_TYPES, unique=True)
    roi_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    affine_space_duration = models.CharField(max_length=10)
    investment_duration = models.CharField(max_length=15)
    is_active = models.BooleanField(default=False)

    # New fields
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.plan_type} - ROI: {self.roi_percentage}% - Duration: {self.investment_duration}"

    def save(self, *args, **kwargs):
        # Call the original save method
        super().save(*args, **kwargs)

        # Try to get an existing Interest object or create a new one
        interest, created = Interest.objects.get_or_create(investment_plan=self)

    class Meta:
        verbose_name = "Investment Plan"
        verbose_name_plural = "Investment Plans"


class Interest(models.Model):
    investment_plan = models.OneToOneField(InvestmentPlan, on_delete=models.CASCADE, related_name='interest', unique=True)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(null=True, blank=True)
    percentage_return = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    monetary_return = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def save(self, *args, **kwargs):
        # Set the start_date if it's not already set
        if not self.start_date:
            self.start_date = timezone.now()

        # Set the end_date to three months after the start_date if it's not already set
        if not self.end_date:
            self.end_date = self.start_date + timedelta(days=90)

        # Override save method to update percentage_return, monetary_return, and total_amount
        super().save(*args, **kwargs)

        # Calculate and update percentage_return, monetary_return, and total_amount
        now = timezone.now()
        duration = self.end_date - self.start_date
        elapsed_time = now - self.start_date

        if elapsed_time >= duration:
            # Investment plan has ended, set percentage_return, monetary_return, and total_amount to final values
            self.percentage_return = Decimal('100.00')
            self.monetary_return = Decimal(str(self.investment_plan.amount)) * (self.percentage_return / Decimal('100.00'))
            self.total_amount = self.investment_plan.amount + self.monetary_return
        else:
            # Investment plan is still active, calculate percentage_return, monetary_return, and total_amount
            forty_eight_hours = timedelta(hours=48)
            elapsed_periods = elapsed_time // forty_eight_hours
            total_periods = duration // forty_eight_hours

            self.percentage_return = Decimal(str((elapsed_periods / total_periods) * self.investment_plan.roi_percentage))
            self.monetary_return = Decimal(str(self.investment_plan.amount)) * (self.percentage_return / Decimal('100.00'))
            self.total_amount = Decimal(str(self.investment_plan.amount)) + self.monetary_return

            # Save the changes
            super().save(*args, **kwargs)

            # Reset monetary_return to zero for the next 48-hour period
            self.monetary_return = Decimal('0.00')
            super().save(*args, **kwargs)

