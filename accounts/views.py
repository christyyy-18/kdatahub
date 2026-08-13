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

def login_view(request):
    if request.method == 'POST':
        from django.db import connection
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if not user.is_manager:
                messages.error(request, 'Access Denied: Only managers can log in.')
                return redirect('accounts:login')
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            notify_manager_login(user)
            return redirect('orders:manager_dashboard')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

def manager_login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user.is_manager:
                login(request, user)
                notify_manager_login(user)
                messages.success(request, f'Welcome to Manager Portal, {user.username}!')
                return redirect('orders:manager_dashboard')
            else:
                messages.error(request, 'Access Denied: Your account does not have manager privileges. Only authorized managers can access this portal.')
                return redirect('accounts:manager_login')
        else:
            messages.error(request, 'Invalid username or password. Please try again.')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'accounts/manager_login.html', {'form': form})

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