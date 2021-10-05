from django.urls import path

from .views import index, UserListView, UserUpdateView, UserDeleteView, UserCreateView, CategoryListView, \
    CategoryCreateView

app_name = 'admins'

urlpatterns = [
    path('', index, name='index'),
    path('users/', UserListView.as_view(), name='admin_users'),
    path('users/create/', UserCreateView.as_view(), name='admin_users_create'),
    path('users/update/<int:pk>/', UserUpdateView.as_view(), name='admin_users_update'),
    path('users/delete/<int:pk>/', UserDeleteView.as_view(), name='admin_users_delete'),
    path('categories/', CategoryListView.as_view(), name='categories'),
    path('category/create/', CategoryCreateView.as_view(), name='category_create'),
    path('products/', UserDeleteView.as_view(), name='products'),
    path('product/create/', UserDeleteView.as_view(), name='product_create'),
]
