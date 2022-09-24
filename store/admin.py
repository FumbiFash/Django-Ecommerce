from django.contrib import admin
from .models import *
from .models import User
# Register your models here.


class customerAdmin(admin.ModelAdmin):
    list_display = ("user","name","email")

class productAdmin(admin.ModelAdmin):
    list_display = ("name","price","digital")

class orderAdmin(admin.ModelAdmin):
    list_display = ("customer","date_ordered","complete","transaction_id")

class orderitemAdmin(admin.ModelAdmin):
    list_display = ("product","order","quantity","date_added")

class shippingaddressAdmin(admin.ModelAdmin):
    list_display = ("customer","order","address","city")

class userAdmin(admin.ModelAdmin):
    list_display = ("name","email")

class categoryAdmin(admin.ModelAdmin):
    list_display = ('name','type')


admin.site.register(Customer,customerAdmin)
admin.site.register(Product,productAdmin)
admin.site.register(Order,orderAdmin)
admin.site.register(OrderItem,orderitemAdmin)
admin.site.register(ShippingAddress,shippingaddressAdmin)
admin.site.register(Category,categoryAdmin)
admin.site.register(User,userAdmin)