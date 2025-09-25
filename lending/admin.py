from django.contrib import admin
from .models import Lending


# Register your models here.
@admin.register(Lending)
class LendingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_email', 'book_id', 'date_borrowed', 'date_due')
    list_filter = ('date_borrowed', 'date_due')
    search_fields = ('user_email', 'book_id')
    ordering = ('-date_borrowed',)
