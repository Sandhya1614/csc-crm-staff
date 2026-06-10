from django.contrib import admin
from .models import Document


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('name',  'doc_type', 'status', 'uploaded_at')
    list_filter = ('status', 'doc_type', 'uploaded_at')
    search_fields = ('name', 'staff__username', 'staff__first_name', 'staff__last_name')
    readonly_fields = ('uploaded_at', 'updated_at', 'doc_type')
    ordering = ('-uploaded_at',)

    fieldsets = (
        ('Document Info', {
            'fields': ('name', 'file', 'doc_type')
        }),
        
        ('Status', {
            'fields': ('status',)
        }),
        ('Timestamps', {
            'fields': ('uploaded_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )

    actions = ['mark_verified', 'mark_pending', 'mark_rejected']

    @admin.action(description='Mark selected documents as Verified')
    def mark_verified(self, request, queryset):
        updated = queryset.update(status='verified')
        self.message_user(request, f'{updated} document(s) marked as Verified.')

    @admin.action(description='Mark selected documents as Pending')
    def mark_pending(self, request, queryset):
        updated = queryset.update(status='pending')
        self.message_user(request, f'{updated} document(s) marked as Pending.')

    @admin.action(description='Mark selected documents as Rejected')
    def mark_rejected(self, request, queryset):
        updated = queryset.update(status='rejected')
        self.message_user(request, f'{updated} document(s) marked as Rejected.')
