from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone
from datetime import timedelta
import random
from .forms import UserRegisterForm, VerificationCodeForm
from .models import EmailVerification

def signup(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            code = f"{random.randint(0, 999999):06d}"
            expires_at = timezone.now() + timedelta(minutes=10)
            EmailVerification.objects.update_or_create(
                user=user,
                defaults={'code': code, 'expires_at': expires_at, 'attempts': 0}
            )

            subject = 'Your verification code'
            message = f"Hello {user.username},\n\nYour verification code is: {code}.\nIt expires in 10 minutes.\n\nIf you did not request this, please ignore this email."
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])

            request.session['pending_user_id'] = user.id
            return redirect('verify_email')
    else:
        form = UserRegisterForm()
    return render(request, 'users/signup.html', {'form': form})

@login_required
def profile(request):
    return render(request, 'users/profile.html')


def verify_email(request):
    pending_user_id = request.session.get('pending_user_id')
    if not pending_user_id:
        return redirect('signup')

    from django.contrib.auth.models import User
    try:
        user = User.objects.get(id=pending_user_id)
    except User.DoesNotExist:
        return redirect('signup')

    if user.is_active:
        return redirect('job_list')

    verification, _ = EmailVerification.objects.get_or_create(
        user=user,
        defaults={
            'code': f"{random.randint(0, 999999):06d}",
            'expires_at': timezone.now() + timedelta(minutes=10),
            'attempts': 0,
        },
    )

    info_message = None
    if 'resend' in request.GET:
        verification.code = f"{random.randint(0, 999999):06d}"
        verification.expires_at = timezone.now() + timedelta(minutes=10)
        verification.attempts = 0
        verification.save()
        subject = 'Your verification code'
        message = f"Hello {user.username},\n\nYour new verification code is: {verification.code}.\nIt expires in 10 minutes."
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])
        info_message = 'A new code has been sent to your email.'

    if request.method == 'POST':
        form = VerificationCodeForm(request.POST)
        if form.is_valid():
            if verification.is_expired():
                verification.code = f"{random.randint(0, 999999):06d}"
                verification.expires_at = timezone.now() + timedelta(minutes=10)
                verification.attempts = 0
                verification.save()
                form.add_error('code', 'Code expired. A new code has been sent.')
                subject = 'Your verification code'
                message = f"Hello {user.username},\n\nYour new verification code is: {verification.code}.\nIt expires in 10 minutes."
                send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])
            else:
                input_code = form.cleaned_data['code']
                if input_code != verification.code:
                    verification.attempts += 1
                    verification.save(update_fields=['attempts'])
                    if verification.attempts >= 5:
                        verification.code = f"{random.randint(0, 999999):06d}"
                        verification.expires_at = timezone.now() + timedelta(minutes=10)
                        verification.attempts = 0
                        verification.save()
                        form.add_error('code', 'Too many attempts. A new code has been sent.')
                        subject = 'Your verification code'
                        message = f"Hello {user.username},\n\nYour new verification code is: {verification.code}.\nIt expires in 10 minutes."
                        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])
                    else:
                        form.add_error('code', 'Invalid code. Please try again.')
                else:
                    user.is_active = True
                    user.save(update_fields=['is_active'])
                    verification.delete()
                    login(request, user)
                    request.session.pop('pending_user_id', None)
                    return redirect('job_list')
    else:
        form = VerificationCodeForm()

    return render(request, 'users/verify_email.html', {'form': form, 'info_message': info_message, 'email': user.email})