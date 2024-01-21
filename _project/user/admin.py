from django.contrib import admin
from .models import Supplier, Seller, Container, Item, ContainerItem, Sale,Payment, Lose, ContainerExpense, ContainerBill
from django.db.models import Sum

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('name', 'place', 'his_money', 'on_him_money', 'total','num_of_containers')  # Display the 'total' field in admin panel

@admin.register(Container)
class ContainerAdmin(admin.ModelAdmin):
    readonly_fields = ('num_of_items','main_total_count','con_weight','total_con_price')

class ContainerItemAdmin(admin.ModelAdmin):
    readonly_fields = ('total_item_price','name','remaining_count')

class ContainerAdmin(admin.ModelAdmin):
    readonly_fields = ('total_con_price',)

admin.site.register(Seller)
admin.site.register(Item)
admin.site.register(ContainerItem)
admin.site.register(Sale)
admin.site.register(Payment)
admin.site.register(Lose)
admin.site.register(ContainerExpense)
admin.site.register(ContainerBill)