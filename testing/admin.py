from django.contrib import admin
from .models import BugTicket

# Register your models here.

@admin.register(BugTicket)
class BugTicketAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('title', 'bug_description')
    readonly_fields = ('created_at',)

# Made with Bob
