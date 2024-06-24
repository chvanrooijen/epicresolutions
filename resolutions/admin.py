from django.contrib import admin
from .models import Role, Cause, Resolution

# Register your models here.
admin.site.register(Role)
admin.site.register(Cause)
admin.site.register(Resolution)
