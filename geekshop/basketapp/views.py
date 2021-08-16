from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, reverse
from mainapp.models import Product
from .models import Basket
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView
from django.db.models import F,Q


class BasketDatailView(LoginRequiredMixin, DetailView):
    model = Basket
    template_name = 'basketapp/basket.html'

    def get_object(self, queryset=None):
        self.object = Basket.objects.filter(user=self.request.user)
        return self.object

    def get_context_data(self, **kwargs):
        context = super(BasketDatailView, self).get_context_data()
        context['basket'] = self.object
        return context


# @login_required
# def basket(request):
#     if request.user.is_authenticated:
#         basket = Basket.objects.filter(user=request.user)
#         context = {
#             'basket': basket
#         }
#
#         return render(request, 'basketapp/basket.html', context)
#     return render(request, 'basketapp/basket.html')


@login_required
def basket_add(request, pk):
    product = get_object_or_404(Product, pk=pk)
    basket = Basket.objects.filter(user=request.user, product=product).first()

    if not basket:
        basket = Basket(user=request.user, product=product)
    basket.quantity += 1
    # basket[0].quantity = F('quantity') + 1
    basket.save()
    if 'login' in request.META.get('HTTP_REFERER'):
        return HttpResponseRedirect(reverse('products:product', args=[pk]))
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def basket_remove(request, pk):
    basket_record = get_object_or_404(Basket, pk=pk)
    basket_record.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def basket_edit(request, pk, quantity):
    if request.is_ajax():
        quantity = int(quantity)
        new_basket_item = Basket.objects.get(pk=int(pk))

        if quantity > 0:
            new_basket_item.quantity = quantity
            new_basket_item.save()
        else:
            new_basket_item.delete()

        basket = Basket.objects.filter(user=request.user).order_by('product__category')

        context = {
            'basket': basket,
        }

        result = render_to_string('basketapp/includes/inc_basket_list.html', context)

        return JsonResponse({'result': result})
