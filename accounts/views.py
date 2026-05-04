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
    if request.method == 'POST':
        form = AgentSignupForm(request.POST, request.FILES)
        if form.is_valid():
            # Create user
            user = form.save()
            
            # Temporary bypass: grant agent status immediately
            user.is_agent = True
            user.save()
            
            # Log the user in
            login(request, user)
            
            # Trigger SMS
            notify_agent_welcome(user)
            notify_manager_agent_signup(user)
            
            messages.success(request, 'Agent registration successful! You are now an active agent (Fee temporarily bypassed).')
            return redirect('home')
    else:
        form = AgentSignupForm()
    return render(request, 'accounts/become_agent.html', {'form': form})

def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('home')
        else:
            print(f"DEBUG: Signup failed. Errors: {form.errors}")
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        from django.db import connection
        print(f"DEBUG: Login attempt for user: {request.POST.get('username')}")
        print(f"DEBUG: DB in use: {connection.vendor}")
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            print(f"DEBUG: Form valid! User found: {user.username}, Is Staff: {user.is_staff}")
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            if user.is_manager:
                notify_manager_login(user)
                return redirect('orders:manager_dashboard')
            return redirect('home')
        else:
            print(f"DEBUG: Form invalid! Errors: {form.errors}")
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