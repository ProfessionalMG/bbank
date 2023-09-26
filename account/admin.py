from django.contrib import admin

from account.models import User, EmailVerificationToken

# Register your models here.
admin.site.register(User)
admin.site.register(EmailVerificationToken)
