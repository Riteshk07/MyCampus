from django.contrib import admin
from Main.models import Analytics
# Register your models here.

class AnalyticsAdmin(admin.ModelAdmin):
    list_display=['ip','user_id','email','date']

admin.site.register(Analytics,AnalyticsAdmin)