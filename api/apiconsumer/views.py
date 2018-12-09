from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf import settings

from django.contrib.auth import login, authenticate
from .forms import TokenForm, ResetTokenForm

from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token

from .models import APIConsumer
from django.core.mail import EmailMessage
from django.core.mail import send_mail

import requests

def form(request):
    if request.method == 'POST':
        form = TokenForm(request.POST)
        if form.is_valid():
            if not form.cleaned_data.get('email').endswith("upenn.edu"):
                return HttpResponse('Invalid upenn.edu username')
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate Your API Consumer Account.'
            message = render_to_string('api/activate_api_consumer.html', {
                'user': user,
                'domain': 'http://localhost:8000/',
                'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode('utf-8'),
                'token':account_activation_token.make_token(user),
            })
            # print(urlsafe_base64_encode(force_bytes(user.pk)).decode('utf-8'), account_activation_token.make_token(user))
            to_email = form.cleaned_data.get('email')
            send_mail(mail_subject, message, 'pennappslabs@gmail.com', [to_email], fail_silently=False)
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
        # login(request, user)
        # return redirect('home')
        current_site = get_current_site(request)
        mail_subject = 'Your API Consumer Account Token'
        message = render_to_string('api/api_consumer_success.html', {
            'user': user,
            'domain': 'http://localhost:8000/',
            'token': user.token,
        })
        to_email = user.email
        # print(to_email, user.token)
        send_mail(mail_subject, message, 'pennappslabs@gmail.com', [to_email, 'pennappslabs@gmail.com'], fail_silently=False)
        return HttpResponse('Thank you for your email confirmation! Check your email for you API token.')
    else:
        return HttpResponse('Activation link is invalid!')

def reset_token(request):
    if request.method == 'POST':
        form = ResetTokenForm(request.POST)
        if form.is_valid():
            to_email = form.cleaned_data.get('email')
            try:
                user = APIConsumer.objects.get(email=to_email)
            except:
                return HttpResponse('Invalid email: APIConsumer user does not exist')
            # print(user)
            current_site = get_current_site(request)
            mail_subject = 'Your API Consumer Account Token (Resent)'
            message = render_to_string('api/api_consumer_success.html', {
                'user': user,
                'domain': 'http://localhost:8000/',
                'token':user.token,
            })
            send_mail(mail_subject, message, 'pennappslabs@gmail.com', [to_email], fail_silently=False)
            return HttpResponse('Your API token was resent.')
    else:
        form = ResetTokenForm()
    return render(request, "api/reset_token.html", {'form': form})
