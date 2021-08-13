from django.shortcuts import render
from mainapp.models import Product
from basketapp.models import Basket


def index(request):
    title = 'Магазин'
    products = Product.objects.filter(is_deleted=False,category__is_deleted=False)
    basket = []
    if request.user.is_authenticated:
        basket = Basket.objects.filter(user=request.user)
    context = {
        'title': title,
        'products': products,
        'basket': basket,
    }
    return render(request, 'index.html', context)


def contacts(request):
    title = 'Контакты'
    context = {
        'title': title
    }
    return render(request, 'contact.html', context)
