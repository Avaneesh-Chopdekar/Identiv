from django.contrib import admin
from .models import LoginLog, PersonDetail, CustomField, Option

# Register your models here.
admin.site.register(LoginLog)
admin.site.register(PersonDetail)
admin.site.register(CustomField)
admin.site.register(Option)
