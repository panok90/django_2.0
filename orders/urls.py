from django.urls import path

from .views import OrderList, order_forming_complete, OrderCreate, OrderRead, OrderUpdate, OrderDelete

app_name="orders"

urlpatterns = [
   path('', OrderList.as_view(), name='orders_list'),
   path('forming/complete/<pk>/', order_forming_complete, name='order_forming_complete'),
   path('create/', OrderCreate.as_view(), name='order_create'),
   path('read/<pk>/', OrderRead.as_view(), name='order_read'),
   path('update/<pk>/', OrderUpdate.as_view(), name='order_update'),
   path('delete/<pk>/', OrderDelete.as_view(), name='order_delete'),
]
