from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, \
    PasswordResetCompleteView
from django.urls import path

from account.views import RegisterView, LoginView, LogoutView, VerifyEmailView, FicaUploadFormView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='registration'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('reset-password/', PasswordResetView.as_view(template_name='account/password_reset.html'),
         name='reset_password'),
    path('reset-password-sent/', PasswordResetDoneView.as_view(template_name='account/password_reset_sent.html'),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='account/password_reset_form.html'),
         name='password_reset_confirm'),
    path('reset-password-complete/',
         PasswordResetCompleteView.as_view(template_name='account/password_reset_done.html'),
         name='password_reset_complete'),
    path('verify-email/<str:user_id>/<str:token>/', VerifyEmailView.as_view(), name='verify_email'),
    path('fica/', FicaUploadFormView.as_view(), name='fica'),

]
