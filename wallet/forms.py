from django import forms

from wallet.models import Transaction


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['amount', 'transaction_type', 'description']
        widgets = {
            'amount': forms.NumberInput(attrs={'class': 'form-control'})}
