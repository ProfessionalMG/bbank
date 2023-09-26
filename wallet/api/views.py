from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated

from wallet.api.serializers import TransactionSerializer, CreateTransactionSerializer
from wallet.models import Transaction, BankAccount


class TransactionsListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TransactionSerializer

    def get_queryset(self):
        """
        This view should return a list of all transactions
        for the currently authenticated user.
        """
        user = self.request.user
        return Transaction.objects.filter(bank_account__account_holder=user)


class CreateTransactionAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CreateTransactionSerializer

    def perform_create(self, serializer):
        # Get the user's bank account details
        bank_account = BankAccount.objects.get(account_holder=self.request.user)
        # Now you can use `bank_account` as needed, e.g., to set it on the transaction.
        # Depending on your serializer's implementation, this may vary.
        serializer.save(bank_account=bank_account)

# TODO: Create a api account registration process
# TODO: Include uploading of Fica documents
