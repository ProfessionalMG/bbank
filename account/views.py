from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ValidationError
from django.core.mail import EmailMessage
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.template.loader import get_template
from django.urls import reverse_lazy, reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views import View
from django.views.generic import CreateView, FormView, RedirectView

from account.forms import RegisterForm, LoginForm, DocumentUploadForm
from account.models import EmailVerificationToken
from wallet.models import BankAccount
from wallet.utils import create_bank_account


# Create your views here.


class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'account/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        try:
            token = default_token_generator.make_token(user)
            verification_token = EmailVerificationToken(user=user)
            verification_token.save()
            # Send verification email
            current_site = get_current_site(self.request)
            mail_subject = 'Activate your account'
            to_email = form.cleaned_data.get('email')
            from_email = settings.EMAIL_HOST_USER

            verification_url = reverse('verify_email',
                                       args=[urlsafe_base64_encode(force_bytes(user.pk)), verification_token.token])
            comp_verification_url = f'{current_site.domain}{verification_url}'
            context_obj = {
                'user': user,
                'url': comp_verification_url,

            }
            message = get_template('account/verification_email.html').render(context=context_obj)

            mail = EmailMessage(
                subject=mail_subject,
                body=message,
                from_email=from_email,
                to=(to_email,),
            )
            mail.content_subtype = 'html'
            mail.send(fail_silently=False)
            messages.success(self.request, 'Verification email sent. Please check your email.')
        except Exception as e:
            print(e)
            pass

        return super().form_valid(form)

    # Raise error if form is invalid
    def form_invalid(self, form):
        error_message = form.errors.as_text()
        raise ValidationError(error_message)


class LoginView(FormView):
    form_class = LoginForm
    template_name = 'account/login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def form_valid(self, form):

        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        user = authenticate(self.request, email=email, password=password)
        if user is not None:
            login(self.request, user)
            return super().form_valid(form)
        else:
            form.add_error(None, 'Invalid email or password')
            return self.form_invalid(form)

    def get_success_url(self):
        bank_account = BankAccount.objects.get(account_holder=self.request.user)
        if bank_account.verified:
            return reverse('transaction_history')
        else:
            return reverse('fica')


class LogoutView(RedirectView):
    url = '/'

    def get(self, request, *args, **kwargs):
        logout(request)
        return super(LogoutView, self).get(request, *args, **kwargs)


class VerifyEmailView(View):
    def get(self, request, user_id, token):
        User = get_user_model()
        user = get_object_or_404(User, pk=urlsafe_base64_decode(user_id))
        verification_token = EmailVerificationToken.objects.filter(user=user).first()
        if verification_token and verification_token.token == token:
            # Activate user's account
            user.is_active = True
            user.is_verified = True
            user.save()

            # Delete the verification token
            EmailVerificationToken.objects.filter(user=user).delete()
            create_bank_account(user)

            # Redirect to login page
            return HttpResponseRedirect(reverse('login'))

        # Verification failed
        return HttpResponseRedirect(reverse('verification_failed'))


class FicaUploadFormView(LoginRequiredMixin, FormView):
    form_class = DocumentUploadForm
    template_name = 'account/fica.html'
    success_url = reverse_lazy('transaction_history')

    def form_valid(self, form):
        id_doc = form.cleaned_data['id_doc']
        proof_of_res = form.cleaned_data['proof_of_res']
        bank_account = BankAccount.objects.get(account_holder=self.request.user)
        bank_account.id_doc = id_doc
        bank_account.proof_of_res = proof_of_res
        bank_account.verified = True
        bank_account.save()
        return super().form_valid(form)

    def get_success_url(self):
        return super().get_success_url()

# TODO: Get all HTML files for password reset process
