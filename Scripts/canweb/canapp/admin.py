from django.contrib import admin

admin.site.site_header = "ADMINISTRATION SECTION"
admin.site.site_title = "My Admin Portal"
admin.site.index_title = "Welcome to THE  Admin PANEL "

# Register your models here.
from django.contrib import admin

class MyModelAdmin(admin.ModelAdmin):
    def has_module_permission(self, request):
        return request.user.is_superuser  # Only superusers can see this app

