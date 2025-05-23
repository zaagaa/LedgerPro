from django.contrib import admin
from .models import Payment

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    search_fields = ['id']
    list_display = ['id', 'supplier', 'amount', 'transaction_date', 'tran_no']
    list_filter = ['transaction_date', 'supplier']  # Optional filters
