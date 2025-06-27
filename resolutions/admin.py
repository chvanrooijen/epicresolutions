from django.contrib import admin
from .models import Role, Domain, Cause, Resolution

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']
    ordering = ['name']

@admin.register(Domain)
class DomainAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']
    ordering = ['name']

@admin.register(Cause)
class CauseAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']
    ordering = ['name']

@admin.register(Resolution)
class ResolutionAdmin(admin.ModelAdmin):
    list_display = ['display_label', 'role', 'domain', 'positive_action']
    list_filter = ['role', 'domain', 'causes']
    search_fields = ['label', 'positive_action', 'goal']
    filter_horizontal = ['causes', 'related_resolutions']
    ordering = ['role', 'domain', 'label', 'positive_action']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('role', 'domain', 'label', 'causes')
        }),
        ('Resolution Components', {
            'fields': ('positive_action', 'trigger', 'goal', 'incentive', 'negative_action')
        }),
        ('Relationships', {
            'fields': ('related_resolutions',),
            'description': 'Select resolutions that this resolution is related to. For consumer resolutions, select other role resolutions that should be available when this consumer resolution is selected.'
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('role', 'domain').prefetch_related('causes', 'related_resolutions')
