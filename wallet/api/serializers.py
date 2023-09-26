from rest_framework import serializers

from wallet.models import Transaction


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'


class CreateTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ('amount', 'description', 'transaction_type')

    # def create(self, validated_data):
    #     # Get the user from the serializer context
    #     user = self.context.get('user')
    #     print(user)
    #     # Fetch the bank account for the user
    #     bank_account = BankAccount.objects.get(account_holder=user)
    #     # Create the transaction with the user's bank account
    #     transaction = Transaction.objects.create(bank_account=bank_account, **validated_data)
    #     return transaction
