import random
from _decimal import Decimal


def create_bank_account(user):
    from .models import BankAccount
    bank_account = BankAccount.objects.create(
        account_holder=user,
    )
    return bank_account


def generate_account_number():
    from .models import BankAccount
    account_number = str(random.randint(1000000000, 9999999999))
    if not BankAccount.objects.filter(account_number=account_number).exists():
        return account_number


def create_dummy_transactions(user):
    from .models import Transaction, BankAccount
    bank_account = BankAccount.objects.get(account_holder=user)
    for i in range(0, 10):
        random_transaction_type = random.choice(['debit', 'credit'])
        random_amount = round(random.uniform(1, 500), 2)
        random_description_debit = random.choice(
            ['Pick n Pay', 'City of Johannesburg', 'Ster-kinikor', 'Mr Price', 'Engen'])
        random_description_credit = random.choice(['Salary', 'Bonus', 'Interest', 'Dividends'])
        transaction = Transaction(
            bank_account=bank_account,
            transaction_type=random_transaction_type,
            amount=random_amount,
        )
        if random_transaction_type == 'debit':
            transaction.description = random_description_debit
            bank_account.balance -= Decimal(str(random_amount))
        else:
            transaction.description = random_description_credit
            bank_account.balance += Decimal(str(random_amount))
        transaction.save()
        bank_account.save()
