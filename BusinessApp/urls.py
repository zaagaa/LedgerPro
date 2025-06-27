from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views
from django.shortcuts import render

urlpatterns = [
    path('db_setup/', views.db_setup, name='db_setup'),
    path('admin/', admin.site.urls),
    path('authenticate/', include('authentication.urls')),
    path('', include('dashboard.urls')),
    path('general/tax_code/', include('tax_code.urls')),
    path('general/inventory/', include('inventory.urls')),
    path('company/', include('company.urls')),
    path('general/attribute/', include('attribute.urls')),
    path('stock/purchase/', include('purchase.urls')),
    path('account/supplier/', include('supplier.urls')),
    path('setting/', include('setting.urls')),
    path('pos/', include('pos.urls')),
    path('customer/', include('customer.urls')),
    path('expenses/', include('expenses.urls')),
    path('bank/', include('bank.urls')),
    path('sync/', include('sync.urls')),
    path('todo/', include('todo.urls')),
    path('staff/', include('staff.urls')),
    path('qrcode/', include('qr_code.urls')),
    path('statement/', include('statement.urls')),



]

# Media files (always serve)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Static files (only if DEBUG is False)
if not settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Custom error handlers
from django.conf.urls import handler404, handler403

# handler404 = 'dashboard.views.custom_404'

def custom_permission_denied_view(request, exception=None):
    return render(request, '403.html', status=403)

handler403 = custom_permission_denied_view
