from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home_view, name='home'),
    path('support/', TemplateView.as_view(template_name='support.html'), name='support'),
    path('accounts/', include('accounts.urls')),
    path('orders/', include('orders.urls')),
    path('payments/', include('payments.urls')),
    path('favicon.ico', RedirectView.as_view(url='/static/img/favicon.ico')),
    path('favicon.png', RedirectView.as_view(url='/static/img/favicon.png')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
