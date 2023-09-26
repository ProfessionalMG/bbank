from django.urls import path

from wallet.views import HomeTemplateView, TransactionHistoryListView, dummy_transactions, TransactionCreateView

urlpatterns = [
    path('', HomeTemplateView.as_view(), name='home'),
    path('transaction-history/', TransactionHistoryListView.as_view(), name='transaction_history'),
    path('transaction/create/', TransactionCreateView.as_view(), name='create_transaction'),
    path('transaction/dummy-data/', dummy_transactions, name='create_dummy_transactions'),
]
