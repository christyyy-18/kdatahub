from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm, CustomAuthenticationForm, UserProfileForm, BecomeAgentForm, AgentSignupForm
from .models import AgentRequest
from orders.models import Order
from payments.utils import initialize_payment
from kdatahub.throttle import is_rate_limited
from kdatahub.sms import (
    notify_manager_login,
    notify_manager_agent_signup,
    notify_agent_welcome
)

def become_agent_view(request):
    messages.info(request, 'Agent registration is disabled. You do not need to create an account to place orders. Simply click "Place Order"!')
    return redirect('home')

def signup_view(request):
    messages.info(request, 'Registration is disabled. You do not need to create an account to place orders. Simply click "Place Order"!')
    return redirect('home')

# Deliberately identical for every failure: a distinct "you are not a manager"
# message would confirm to an attacker that the password they tried was right.
LOGIN_FAILED = 'Invalid username or password. Please try again.'


def _handle_login(request, template):
    form = CustomAuthenticationForm()

    if request.method == 'POST':
        if is_rate_limited(request, 'login', limit=8, window_seconds=900):
            messages.error(request, 'Too many login attempts. Please try again in a few minutes.')
            return render(request, template, {'form': form})

        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid() and form.get_user().is_manager:
            user = form.get_user()
            login(request, user)
            notify_manager_login(user)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('orders:manager_dashboard')

        messages.error(request, LOGIN_FAILED)

    return render(request, template, {'form': form})


def login_view(request):
    return _handle_login(request, 'accounts/login.html')


def manager_login_view(request):
    return _handle_login(request, 'accounts/manager_login.html')

def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('home')

@login_required
def profile_view(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('accounts:profile')
    else:
        form = UserProfileForm(instance=request.user)
    return render(request, 'accounts/profile.html', {'form': form})