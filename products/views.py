from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.conf import settings
from django.core.cache import cache
from django.db import connection

from common.views import CommonContextMixin
from products.models import Product, ProductCategory


def get_links_menu():
    if settings.LOW_CACHE:
        key = 'links_menu'
        links_menu = cache.get(key)
        if links_menu is None:
            links_menu = ProductCategory.objects.filter(is_active=True)
            cache.set(key, links_menu)
        return links_menu
    else:
        return ProductCategory.objects.filter(is_active=True)


def get_products():
    if settings.LOW_CACHE:
        key = 'products'
        products = cache.get(key)
        if products is None:
            products = Product.objects.filter(is_active=True, category__is_active=True).select_related('category')
            cache.set(key, products)
        return products
    else:
        return Product.objects.filter(is_active=True, category__is_active=True).select_related('category')


class IndexView(CommonContextMixin, TemplateView):
    template_name = 'products/index.html'
    title = 'GeekShop'


class ProductsListView(CommonContextMixin, ListView):
    model = Product
    template_name = 'products/products.html'
    paginate_by = 3
    title = 'GeekShop - Каталог'

    def get_queryset(self):
        queryset = super(ProductsListView, self).get_queryset()
        category_id = self.kwargs.get('category_id')
        return queryset.filter(category_id=category_id) if category_id else queryset

    def get_context_data(self, **kwargs):
        context = super(ProductsListView, self).get_context_data(**kwargs)
        context['categories'] = ProductCategory.objects.all()
        context['menu'] = get_links_menu()
        context['products'] = get_products()
        return context


# def index(request):
#     context = {'title': 'GeekShop'}
#     return render(request, 'products/index.html', context)

# def products(request, category_id=None, page=1):
#     context = {'title': 'GeekShop - Каталог', 'categories': ProductCategory.objects.all()}
#     products = Product.objects.filter(category_id=category_id) if category_id else Product.objects.all()
#
#     paginator = Paginator(products, 3)
#     try:
#         products_paginator = paginator.page(page)
#     except PageNotAnInteger:
#         products_paginator = paginator.page(1)
#     except EmptyPage:
#         products_paginator = paginator.page(paginator.num_pages)
#     context['products'] = products_paginator
#     return render(request, 'products/products.html', context)


def db_profile_by_type(prefix, type, queries):
    update_queries = list(filter(lambda x: type in x['sql'], queries))
    print(f'db_profile {type} for {prefix}:')
    [print(query['sql']) for query in update_queries]


@receiver(pre_save, sender=ProductCategory)
def product_is_active_update_productcategory_save(sender, instance, **kwargs):
    if instance.pk:
        if instance.is_active:
            instance.product_set.update(is_active=True)
        else:
            instance.product_set.update(is_active=False)

        db_profile_by_type(sender, 'UPDATE', connection.queries)
