from .models import InvestmentPlan, AccountSummary, Funds
from decimal import Decimal
from django.db.models import Sum

def handle_basic_investment(user, amount, account_type):
    roi_percentage = 1.16
    affine_space = '48HRS'
    duration = '3 MONTHS'
    
    # Check if the user has sufficient funds in the AccountSummary
    if has_sufficient_funds(user, account_type, amount):
        investment_plan = InvestmentPlan.objects.create(
            user=user,
            amount=amount,
            is_active=True,
            plan_type='basic',
            roi_percentage=roi_percentage,
            affine_space_duration=affine_space,
            investment_duration=duration
        )

        # Deduct the invested amount from the corresponding AccountSummary
        update_account_summary(user, account_type, amount)

def handle_standard_investment(user, amount, account_type):
    roi_percentage = 0.45
    affine_space = '48HRS'
    duration = '3 MONTHS'

    # Check if the user has sufficient funds in the AccountSummary
    if has_sufficient_funds(user, account_type, amount):
        investment_plan = InvestmentPlan.objects.create(
            user=user,
            amount=amount,
            is_active=True,
            plan_type='standard',
            roi_percentage=roi_percentage,
            affine_space_duration=affine_space,
            investment_duration=duration
        )

        # Deduct the invested amount from the corresponding AccountSummary
        update_account_summary(user, account_type, amount)

def handle_platinum_investment(user, amount, account_type):
    # Replace with actual Platinum ROI, Affine Space, and Duration
    roi_percentage = 0.45
    affine_space = '48HRS'
    duration = '3 MONTHS'

    # Check if the user has sufficient funds in the AccountSummary
    if has_sufficient_funds(user, account_type, amount):
        investment_plan = InvestmentPlan.objects.create(
            user=user,
            amount=amount,
            is_active=True,
            plan_type='platinum',
            roi_percentage=roi_percentage,
            affine_space_duration=affine_space,
            investment_duration=duration
        )

        # Deduct the invested amount from the corresponding AccountSummary
        update_account_summary(user, account_type, amount)

def handle_premium_investment(user, amount, account_type):
    # Replace with actual Premium ROI, Affine Space, and Duration
    roi_percentage = 0.50
    affine_space = '48HRS'
    duration = '3 MONTHS'

    # Check if the user has sufficient funds in the AccountSummary
    if has_sufficient_funds(user, account_type, amount):
        investment_plan = InvestmentPlan.objects.create(
            user=user,
            amount=amount,
            is_active=True,
            plan_type='premium',
            roi_percentage=roi_percentage,
            affine_space_duration=affine_space,
            investment_duration=duration
        )

        # Deduct the invested amount from the corresponding AccountSummary
        update_account_summary(user, account_type, amount)

def has_sufficient_funds(user, account_type, amount):
    # Convert amount to Decimal if it's not already
    if not isinstance(amount, Decimal):
        amount = Decimal(amount)

    # Check if the user has sufficient funds in the AccountSummary
    summary = AccountSummary.objects.filter(user=user, account_type=account_type).first()

    if summary and summary.total_amount >= amount:
        return True
    else:
        return False

def update_account_summary(user, account_type, amount):
    # Update or create an AccountSummary entry based on approved funds
    funds_total = Funds.objects.filter(user=user, account_type=account_type, confirmed=True).aggregate(sum_amount=Sum('amount'))['sum_amount'] or 0

    # Try to get an existing summary for the user and account_type
    summary, created = AccountSummary.objects.get_or_create(user=user, account_type=account_type)

    if created or amount > 0:
        # Update the existing summary if created or amount is greater than 0
        summary.total_amount = funds_total - amount  # Deduct the invested amount
        summary.save()
