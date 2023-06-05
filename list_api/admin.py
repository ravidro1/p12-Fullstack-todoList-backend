from django.contrib import admin

from list_api.models import Task, List, CustomUser

admin.site.register(Task)
admin.site.register(List)
admin.site.register(CustomUser)