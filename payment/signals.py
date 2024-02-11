# payment/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import InvestmentPlan
from payment.models import Interest  # Make sure to adjust the import path if necessary

@receiver(post_save, sender=InvestmentPlan)
def create_interest(sender, instance, created, **kwargs):
    if created:
        Interest.objects.get_or_create(investment_plan=instance)
