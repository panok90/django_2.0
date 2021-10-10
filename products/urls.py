from django.urls import path
from django.views.decorators.cache import cache_page

from products.views import ProductsListView

app_name = 'products'

urlpatterns = [
    path('', cache_page(60)(ProductsListView.as_view()), name='index'),
    path('<int:category_id>/', ProductsListView.as_view(), name='product'),
    path('page/<int:page>/', ProductsListView.as_view(), name='page')
]
