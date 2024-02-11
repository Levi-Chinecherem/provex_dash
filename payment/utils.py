# payment/utils.py
from .models import AccountSummary, Funds, USDT_TRC20, USDT_ERC20, BTC

def get_latest_usdt_trc20():
    return USDT_TRC20.objects.latest('id')

def get_latest_usdt_erc20():
    return USDT_ERC20.objects.latest('id')

def get_latest_btc():
    return BTC.objects.latest('id')

def get_account_balance(user, account_type):
    try:
        funds_entry = Funds.objects.get(user=user, account_type=account_type)
        return funds_entry.amount, funds_entry.wallet_address[-4:]
    except Funds.DoesNotExist:
        return 0, ''
   
def get_account_details(user, account_type):
    # Get the last four digits of the wallet address based on the account type
    if account_type == 'USDT_TRC20':
        wallet_model = USDT_TRC20
    elif account_type == 'USDT_ERC20':
        wallet_model = USDT_ERC20
    elif account_type == 'BTC':
        wallet_model = BTC
    else:
        # Handle unsupported account types or raise an exception
        raise ValueError("Unsupported account type")

    # Get the last four digits of the wallet address
    wallet_entry = wallet_model.objects.filter().last()
    last_four_digits = wallet_entry.wallet_address[-4:]

    # Get the total amount from the AccountSummary model
    summary_entry, _ = AccountSummary.objects.get_or_create(user=user, account_type=account_type)
    total_amount = summary_entry.total_amount

    # Create a dictionary with specific keys for each type of balance and last digits
    result = {
        f'{account_type.lower()}_balance': total_amount,
        f'{account_type.lower()}_last_digits': last_four_digits,
    }

    return result
