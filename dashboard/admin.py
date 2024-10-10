from django.contrib import admin
from .models import LoginLog, PersonDetail, CustomField, Option, Notification, Blacklist

# Register your models here.
admin.site.register(LoginLog)
admin.site.register(PersonDetail)
admin.site.register(CustomField)
admin.site.register(Option)
admin.site.register(Notification)
admin.site.register(Blacklist)
