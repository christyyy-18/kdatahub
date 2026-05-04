from django.shortcuts import render, redirect

def home_view(request):
    if not request.user.is_authenticated:
        return redirect('accounts:login')
    return render(request, 'home.html')
