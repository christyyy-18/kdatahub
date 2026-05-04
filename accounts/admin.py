from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, AgentRequest

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email', 'is_manager', 'is_staff']
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('is_manager', 'profile_picture', 'phone_number')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('is_manager', 'profile_picture', 'phone_number')}),
    )

@admin.register(AgentRequest)
class AgentRequestAdmin(admin.ModelAdmin):
    list_display = ('user', 'business_name', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('user__username', 'business_name', 'phone_number')
    actions = ['approve_requests', 'reject_requests']

    def approve_requests(self, request, queryset):
        queryset.update(status='approved')
        for agent_req in queryset:
            agent_req.user.is_manager = True
            agent_req.user.save()
    approve_requests.short_description = "Approve selected requests and make users managers"

    def reject_requests(self, request, queryset):
        queryset.update(status='rejected')
    reject_requests.short_description = "Reject selected requests"

admin.site.register(CustomUser, CustomUserAdmin)
