from django.urls import path
from . import views

urlpatterns = [
    path('',views.login_user, name='login' ),
    path('logout',views.logout_user, name='logout' ),
    path('register',views.register, name='register' ),
    path('home',views.home, name='home' ),
# =====================================================================================
    path('addcontainer',views.add_container, name='addcontainer' ),
    path('containerdelete/<int:id>',views.container_delete, name='containerdelete' ),
    path('containerupdate/<int:id>',views.container_update, name='containerupdate' ),
    path('condetails/<int:id>',views.container_details, name='condetails' ),
    path('containerexpensesdelete/<int:id>',views.container_expenses_delete, name='containerexpensesdelete' ),
    path('containerbillupdate/<int:id>', views.container_bill_update, name='containerbillupdate'),
    path('containerbilldelete/<int:id>', views.container_bill_delete, name='containerbilldelete'),
    path('containerItems/<int:id>',views.container_items, name='containeritems' ),
    path('containeritemdelete/<int:id>',views.containeritem_delete, name='containeritemdelete' ),
    path('today',views.today_containers, name='today' ),
    path('remain',views.remain_containers, name='remain' ),
    path('finished',views.finished_containers, name='finished' ),
    path('sellcon/<int:id>',views.sell_container, name='sellcon' ),
    # path('saleupdate/<int:id>',views.sale_update, name='saleupdate' ),
    path('saledelete/<int:id>',views.sale_delete, name='saledelete' ),
# =====================================================================================
    path('profits',views.profits, name='profits' ),
    path('profitsupdate/<int:id>',views.profits_update, name='profitsupdate' ),
    path('profitsdelete/<int:id>',views.profits_delete, name='profitsdelete' ),
    path('loses',views.loses, name='loses' ),
    path('losesdelete/<int:id>',views.loses_delete, name='losesdelete' ),
    path('daymoney',views.day_money, name='daymoney' ),
# =====================================================================================
    path('items',views.add_items, name='items' ),
    path('itemupdate/<int:id>',views.item_update, name='itemupdate' ),
    path('itemdelete/<int:id>',views.item_delete, name='itemdelete' ),
# =====================================================================================
    path('sellerpage/<int:id>',views.seller_page, name='sellerpage' ),
    path('selleraccounts',views.seller_accounts, name='selleraccounts' ),
    path('sellerdelete/<int:id>',views.seller_delete, name='sellerdelete' ),
    path('sellerupdate/<int:id>',views.seller_update, name='sellerupdate' ),
    path('sellersort',views.seller_sort, name='sellersort' ),
# =====================================================================================
    path('supplierpage/<int:id>',views.supplier_page, name='supplierpage' ),
    path('suppliersaccounts',views.suppliers_accounts, name='suppliersaccounts' ),
    path('suppliersort',views.supplier_sort, name='suppliersort' ),
    path('suppliersdelete/<int:id>',views.supplier_delete, name='suppliersdelete' ),
    path('supplierupdate/<int:id>',views.supplier_update, name='supplierupdate' ),
    path('supplierprofits',views.supplier_profits, name='supplierprofits' ),
    path('supplierprofitsdelete/<int:id>',views.supplier_profits_delete, name='supplierprofitsdelete' ),
]
    