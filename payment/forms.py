# payment/forms.py

from django import forms
from .models import Funds

class WithdrawalForm(forms.Form):
    account_type = forms.ChoiceField(
        label='Account Type',
        choices=Funds.ACCOUNT_TYPES,
        required=True,
        widget=forms.Select(attrs={'class': 'form-control mb-0 btn-border'})
    )
    amount = forms.DecimalField(
        label='Amount',
        max_digits=10,
        decimal_places=2,
        required=True,
        widget=forms.NumberInput(attrs={'class': 'form-control mb-0 btn-border'})
    )
    wallet_address = forms.CharField(
        label='Wallet Address',
        max_length=255,
        required=False,
        help_text='Paste your wallet address for funding',
        widget=forms.TextInput(attrs={'class': 'form-control mb-0 btn-border'})
    )
