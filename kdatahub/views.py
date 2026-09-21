from django.shortcuts import render

from orders.catalog import catalog_for


def home_view(request):
    is_agent = getattr(request.user, 'is_agent', False)
    return render(request, 'home.html', {'catalog': catalog_for(is_agent=is_agent)})
