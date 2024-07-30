from django.contrib import admin
from ecommapp.models import Product
# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    list_display=['id','name','price','pdetails']
    list_filter=['cat','is_active']    
admin.site.register(Product,ProductAdmin)