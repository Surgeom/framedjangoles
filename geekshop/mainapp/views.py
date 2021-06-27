from django.shortcuts import render
from .models import ProductCategory


def products(request):
    title = 'продукты/каталог'
    links_menu = ProductCategory.objects.all()
    links_translate = {
        'Дом': 'products_home',
        'Офис': 'products_office',
        'Модерн': 'products_modern',
        'Классика': 'products_classic'
    }
    #         [
    #         {'href': 'products_all', 'name': 'все'},
    #         {'href': 'products_home', 'name': 'дом'},
    #         {'href': 'products_office', 'name': 'офис'},
    #         {'href': 'products_modern', 'name': 'модерн'},
    #         {'href': 'products_classic', 'name': 'классика'},
    # ]
    context = {
        'title': title,
        'links_menu': links_menu,
        'links_translate':links_translate

    }
    return render(request=request, template_name='products.html', context=context)
