from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from .forms import ResetTokenForm, TokenForm
from .models import APIConsumer
from .tokens import account_activation_token


def form(request):
    if request.method == 'POST':
        form = TokenForm(request.POST)
        if form.is_valid():
            if not form.cleaned_data.get('email').endswith('upenn.edu'):
                return HttpResponse('Invalid upenn.edu username')
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            mail_subject = 'Activate Your API Consumer Account.'
            message = render_to_string('activate_api_consumer.html', {
                'user': user,
                'domain': settings.EMAIL_LINK,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode('utf-8'),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            from_email = settings.EMAIL_HOST_USER
            send_mail(mail_subject, message, from_email, [to_email], fail_silently=False)
            return HttpResponse('Please confirm your email address to complete the registration')
    else:
        form = TokenForm()
    return render(request, 'api/form.html', {'form': form})


def activate(request, uidb64, token):
    # set to expire (if user doesn't activate) and can't access again (already done)
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = APIConsumer.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, APIConsumer.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        mail_subject = 'Your API Consumer Account Token'
        message = render_to_string('api_consumer_success.html', {
            'user': user,
            'domain': settings.EMAIL_LINK,
            'token': user.token,
        })
        to_email = user.email
        from_email = settings.EMAIL_HOST_USER
        send_mail(mail_subject, message, from_email, [to_email, from_email], fail_silently=False)
        return HttpResponse('Thank you for your email confirmation! Check your email for you API token.')
    else:
        return HttpResponse('Activation link is invalid!')


def reset_token(request):
    if request.method == 'POST':
        form = ResetTokenForm(request.POST)
        if form.is_valid():
            to_email = form.cleaned_data.get('email')
            from_email = settings.EMAIL_HOST_USER
            try:
                user = APIConsumer.objects.get(email=to_email)
            except ObjectDoesNotExist:
                return HttpResponse('Invalid email: APIConsumer user does not exist')
            mail_subject = 'Your API Consumer Account Token (Resent)'
            message = render_to_string('api_consumer_success.html', {
                'user': user,
                'domain': 'http://localhost:8000/',
                'token': user.token,
            })
            send_mail(mail_subject, message, from_email, [to_email], fail_silently=False)
            return HttpResponse('Your API token was resent.')
    else:
        form = ResetTokenForm()
    return render(request, 'api/reset_token.html', {'form': form})
