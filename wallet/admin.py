from django.contrib import admin

from wallet.models import BankAccount, FICA, Transaction

# Register your models here.
admin.site.register(BankAccount)
admin.site.register(FICA)
admin.site.register(Transaction)
