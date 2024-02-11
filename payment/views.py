from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .utils import *
from .models import Funds, AccountSummary, Withdrawal
from decimal import Decimal
from django.contrib import messages
from .utils2 import handle_basic_investment, handle_standard_investment, handle_platinum_investment, handle_premium_investment
from .forms import WithdrawalForm

def withdraw_view(request):
    user_withdrawals = Withdrawal.objects.filter(user=request.user)
    
    if request.method == 'POST':
        form = WithdrawalForm(request.POST)
        if form.is_valid():
            account_type = form.cleaned_data['account_type']
            amount = form.cleaned_data['amount']
            wallet_address = form.cleaned_data['wallet_address']

            withdrawal = Withdrawal.objects.create(
                user=request.user,
                account_type=account_type,
                amount=amount,
                wallet_address=wallet_address,
            )

            return redirect('withdraw')
    else:
        form = WithdrawalForm()

    context = {
        'user_withdrawals': user_withdrawals,
        'form': form,
    }
    return render(request, 'dashboard/withdraw.html', context)


@login_required
def fund_view(request):
    # Get the latest data
    latest_usdt_trc20 = get_latest_usdt_trc20()
    latest_usdt_erc20 = get_latest_usdt_erc20()
    latest_btc = get_latest_btc()

    user = request.user

    if request.method == 'POST':
        amount_str = request.POST.get('amount')
        account_type = request.POST.get('account_type')

        # Handle the conversion to float gracefully
        try:
            amount = float(amount_str)
        except ValueError:
            # Handle the case where the conversion to float fails
            amount = 0.0  # Set a default value or handle the error appropriately
            messages.error(request, 'Invalid amount. Please enter a valid number.')

        else:
            # Create a new Funds object and save it
            fund = Funds.objects.create(user=user, account_type=account_type, amount=amount)

            # Add success message
            messages.success(request, f'Funds added successfully! Amount: {amount}')

            # Redirect to a success page
            return redirect('success_page')  # Replace 'success_page_name' with the actual name or URL of your success page

    # Include the data in the context
    context = {
        'latest_usdt_trc20': latest_usdt_trc20,
        'latest_usdt_erc20': latest_usdt_erc20,
        'latest_btc': latest_btc,
    }

    return render(request, 'dashboard/fund.html', context)


def success_page(request):
    return render(request, 'message.html')

@login_required
def balance_view(request):
    # Initialize summaries to None
    usdt_trc20_summary = None
    usdt_erc20_summary = None
    btc_summary = None

    # Try to retrieve each AccountSummary
    try:
        usdt_trc20_summary = AccountSummary.objects.get(user=request.user, account_type='USDT_TRC20')
    except AccountSummary.DoesNotExist:
        pass

    try:
        usdt_erc20_summary = AccountSummary.objects.get(user=request.user, account_type='USDT_ERC20')
    except AccountSummary.DoesNotExist:
        pass

    try:
        btc_summary = AccountSummary.objects.get(user=request.user, account_type='BTC')
    except AccountSummary.DoesNotExist:
        pass

    # Include the summaries in the context
    context = {
        'usdt_trc20_summary': usdt_trc20_summary,
        'usdt_erc20_summary': usdt_erc20_summary,
        'btc_summary': btc_summary,
    }

    return render(request, 'dashboard/balance.html', context)


def handle_investment_submission(request, plan_type):
    amount = request.POST.get('amount')
    account_type = request.POST.get('account_type')

    if plan_type == 'basic':
        handle_basic_investment(request.user, amount, account_type)
    elif plan_type == 'standard':
        handle_standard_investment(request.user, amount, account_type)
    elif plan_type == 'platinum':
        handle_platinum_investment(request.user, amount, account_type)
    elif plan_type == 'premium':
        handle_premium_investment(request.user, amount, account_type)

    # Redirect to the success page with a success message
    messages.success(request, f"Investment in {plan_type.capitalize()} plan submitted successfully!")
    return redirect('success_page')


def pricing_view(request):
    if request.method == 'POST':
        plan_type = request.POST.get('plan_type')

        # Call the utility function based on the plan_type
        handle_investment_submission(request, plan_type)

    return render(request, 'dashboard/pricing.html')
