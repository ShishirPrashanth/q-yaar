from django.contrib import admin

from account.models import PlatformUser


class PlatformUserAdmin(admin.ModelAdmin):
    list_display = ("email", "external_id", "is_active", "is_suspended")
    readonly_fields = ("is_admin", "last_login")
    exclude = ("password", "auth_secret")
    list_filter = ("is_active", "is_suspended")
    search_fields = ("email", "phone", "external_id")


admin.site.register(PlatformUser, PlatformUserAdmin)
