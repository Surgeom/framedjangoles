import random

from django.shortcuts import render, get_object_or_404
from .models import ProductCategory, Product
from basketapp.models import Basket


def get_basket(user):
    if user.is_authenticated:
        return Basket.objects.filter(user=user)
    else:
        return []


def get_hot_product():
    products = Product.objects.all()
    return random.sample(list(products), 1)[0]


def get_same_products(hot_product):
    same_products = Product.objects.filter(category=hot_product.category).exclude(pk=hot_product.pk)
    return same_products


def products(request, pk=None):
    title = 'продукты/каталог'
    basket = get_basket(request.user)

    links_menu = ProductCategory.objects.all()
    products = Product.objects.all().order_by('price')
    if pk is not None:
        if pk == 0:
            products = Product.objects.all().order_by('price')
            category = {'name': 'все'}
        else:
            category = get_object_or_404(ProductCategory, pk=pk)
            products = Product.objects.filter(category__pk=pk).order_by('price')
        hot_product = get_hot_product()
        same_products = get_same_products(hot_product)
        context = {
            'title': title,
            'links_menu': links_menu,
            'products': products,
            'category': category,
            'same_products': same_products,
            'hot_product': hot_product,

        }
        return render(request=request, template_name='products.html', context=context)
    hot_product = get_hot_product()
    same_products = get_same_products(hot_product)
    context = {
        'title': title,
        'links_menu': links_menu,
        'same_products': same_products,
        'products': products,
        'basket': basket,
        'hot_product': hot_product

    }
    return render(request=request, template_name='products.html', context=context)


def product(request, pk):
    title = 'продукты'

    context = {
        'title': title,
        'links_menu': ProductCategory.objects.all(),
        'product': get_object_or_404(Product, pk=pk),
        'basket': get_basket(request.user),
    }

    return render(request, 'product.html', context)
