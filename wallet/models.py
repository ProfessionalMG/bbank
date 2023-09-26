from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import pre_save

from .utils import generate_account_number

User = get_user_model()


# Create your models here.
class BankAccount(models.Model):
    account_holder = models.ForeignKey(User, on_delete=models.CASCADE)
    account_number = models.CharField(max_length=10, unique=True)
    is_active = models.BooleanField(default=True)
    verified = models.BooleanField(default=False)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    currency = models.CharField(max_length=3, default='ZAR')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.account_number} - {self.balance}"


class FICA(models.Model):
    """Model for FICA documents"""
    account = models.OneToOneField(BankAccount, on_delete=models.CASCADE)
    id_doc = models.FileField(upload_to='id_documents/', blank=True, null=True)
    proof_of_res = models.FileField(upload_to='proof_of_residence/', blank=True, null=True)
    FICAd = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.account.account_holder.first_name} - {self.id_doc} - {self.proof_of_res}"


class Transaction(models.Model):
    """Model for transactions. Debit minus from balance, credit adds to balance"""
    TRANSACTION_TYPES = (
        ('debit', 'Debit'),
        ('credit', 'Credit')
    )

    bank_account = models.ForeignKey(BankAccount, on_delete=models.CASCADE, related_name='transactions')
    transaction_type = models.CharField(max_length=6, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=240, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.transaction_type} - ${self.amount} on {self.timestamp}"


# Pre-Saver that creates an account number for the user
def create_account_number(sender, instance, *args, **kwargs):
    if not instance.account_number:
        instance.account_number = generate_account_number()


pre_save.connect(create_account_number, sender=BankAccount)
