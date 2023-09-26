# Create your views here.
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import TemplateView, ListView, CreateView

from wallet.forms import TransactionForm
from wallet.models import Transaction, BankAccount
from wallet.utils import create_dummy_transactions


class HomeTemplateView(TemplateView):
    template_name = 'wallet/home.html'


class TransactionHistoryListView(LoginRequiredMixin, ListView):
    model = Transaction
    template_name = 'wallet/transaction_history.html'
    context_object_name = 'transactions'

    def get_queryset(self):
        return Transaction.objects.filter(bank_account__account_holder=self.request.user).order_by('-timestamp')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TransactionHistoryListView, self).get_context_data(**kwargs)
        context['balance'] = BankAccount.objects.get(account_holder=self.request.user).balance
        return context


def dummy_transactions(request):
    create_dummy_transactions(request.user)
    return HttpResponseRedirect(reverse('transaction_history'))


class TransactionCreateView(LoginRequiredMixin, CreateView):
    model = Transaction
    form_class = TransactionForm
    template_name = 'wallet/create_transaction.html'

    def form_valid(self, form):
        bank_account = BankAccount.objects.get(account_holder=self.request.user)
        form.instance.bank_account = bank_account
        if form.is_valid():
            form.save()
            if form.instance.transaction_type == 'debit':
                bank_account.balance -= form.instance.amount
            else:
                bank_account.balance += form.instance.amount
            bank_account.save()

        return super(TransactionCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('transaction_history')
