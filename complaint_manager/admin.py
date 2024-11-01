from django.contrib import admin
from .models import Complain

@admin.register(Complain)
class ComplainAdmin(admin.ModelAdmin):
    list_display = ('category', 'subcategory', 'priority', 'confidence_score', 'user')
    list_filter = ('category', 'priority', 'user')
    search_fields = ('issue_description','category')
    ordering = ('-priority', '-confidence_score')
