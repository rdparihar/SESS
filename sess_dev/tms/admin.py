from django.contrib import admin

# Register your models here.
from .models import TimeRecords,TimeMenus
from .models import ProjectName

admin.site.register(TimeRecords)
admin.site.register(TimeMenus)
admin.site.register(ProjectName)