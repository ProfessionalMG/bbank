from django.urls import path, include

from wallet.api.views import TransactionsListAPIView, CreateTransactionAPIView

urlpatterns = [
    path('transaction-history/', TransactionsListAPIView.as_view(), name='transaction_history_api'),
    path('create-transaction/', CreateTransactionAPIView.as_view(), name='create_transaction_api'),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
]
