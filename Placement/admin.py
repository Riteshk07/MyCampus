from django.contrib import admin
from .models import Company, Saved_Company, Salary


# Register your models here.
class CompanyAdmin(admin.ModelAdmin):
    list_display=['id', 'name','desc','link', 'icon_url']
    list_editable=['name','desc', 'link', 'icon_url']
admin.site.register(Company, CompanyAdmin)

class Saved_CompanyAdmin(admin.ModelAdmin):
    list_display=['id', 'company_id','user_id','last_open']
    list_editable=['company_id','user_id']
admin.site.register(Saved_Company, Saved_CompanyAdmin)

class SalaryAdmin(admin.ModelAdmin):
    list_display=['id','company_id','position', 'base','bonus','stock', 'country']
    list_editable=['base','bonus','stock']
admin.site.register(Salary, SalaryAdmin)
