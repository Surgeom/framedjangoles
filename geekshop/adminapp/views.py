from django.db.models import F
from django.http import HttpResponseRedirect
from django.urls import reverse

from authapp.forms import ShopUserRegisterForm, ShopUserEditForm
from authapp.models import ShopUser
from django.shortcuts import get_object_or_404, render
from mainapp.models import Product, ProductCategory
from django.contrib.auth.decorators import user_passes_test
from .forms import ShopUserAdminEditForm, ProductEditForm, ProductCategoryCreateForm, ProductCategoryEditForm
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.dispatch import receiver
from django.db.models.signals import pre_save
from django.db import connection


class UsersListView(LoginRequiredMixin, ListView):
    model = ShopUser
    template_name = 'adminapp/users.html'
    context_object_name = 'objects'
    login_url = '/auth/login/'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(UsersListView, self).get_context_data()
        context['title'] = 'админка/пользователи'
        return context

    def get_queryset(self):
        return self.model.objects.all().order_by('-is_active', '-is_superuser', '-is_staff', 'username')


# @user_passes_test(lambda u: u.is_superuser)
# def users(request):
#     title = 'админка/пользователи'
#
#     users_list = ShopUser.objects.all().order_by('-is_active', '-is_superuser', '-is_staff', 'username')
#
#     context = {
#         'title': title,
#         'objects': users_list
#     }
#
#     return render(request, 'adminapp/users.html', context)

class UserCreateCreateView(LoginRequiredMixin, CreateView):
    login_url = '/auth/login/'
    model = ShopUser
    template_name = 'adminapp/user_create.html'
    form_class = ShopUserRegisterForm
    success_url = '/admin_staff/users/read/'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(UserCreateCreateView, self).get_context_data()
        context['title'] = 'пользователи/создать'
        return context


# @user_passes_test(lambda u: u.is_superuser)
# def user_create(request):
#     title = 'пользователи/создать'
#     if request.method == 'POST':
#         user_form = ShopUserRegisterForm(request.POST, request.FILES)
#         if user_form.is_valid():
#             user_form.save()
#             return HttpResponseRedirect(reverse('admin_staff:users'))
#     else:
#         user_form = ShopUserRegisterForm()
#     context = {
#         'title': title,
#         'user_form': user_form
#     }
#     return render(request, 'adminapp/user_create.html', context)

class UserUpdateView(LoginRequiredMixin, UpdateView):
    login_url = '/auth/login/'
    model = ShopUser
    form_class = ShopUserAdminEditForm
    template_name = 'adminapp/user_update.html'
    success_url = '/admin_staff/users/read/'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(UserUpdateView, self).get_context_data()
        context['title'] = 'пользователи/редактировать'
        context['user_form'] = self.get_form()
        return context


# @user_passes_test(lambda u: u.is_superuser)
# def user_update(request, pk):
#     title = 'пользователи/редактировать'
#     edit_user = get_object_or_404(ShopUser, pk=pk)
#     if request.method == 'POST':
#         user_form = ShopUserAdminEditForm(request.POST, request.FILES, instance=edit_user)
#         if user_form.is_valid():
#             user_form.save()
#             return HttpResponseRedirect(reverse('admin_staff:user_update', args=[edit_user.pk]))
#         return HttpResponseRedirect(reverse('admin_staff:users'))
#     else:
#         user_form = ShopUserAdminEditForm(instance=edit_user)
#     context = {
#         'title': title,
#         'user_form': user_form,
#     }
#     return render(request, 'adminapp/user_update.html', context)

class UserDeleteView(LoginRequiredMixin, DeleteView):
    login_url = '/auth/login/'
    model = ShopUser
    template_name = 'adminapp/user_delete.html'
    success_url = '/admin_staff/users/read/'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.is_deleted = True
        self.object.is_active = False
        self.object.save()
        return HttpResponseRedirect(success_url)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(UserDeleteView, self).get_context_data()
        context['title'] = 'пользователи/редактировать'
        context['user_to_delete'] = self.object
        return context


# @user_passes_test(lambda u: u.is_superuser)
# def user_delete(request, pk):
#     title = 'пользователи/удаление'
#
#     user = get_object_or_404(ShopUser, pk=pk)
#
#     if request.method == 'POST':
#         user.is_deleted = True
#         user.is_active = False
#         user.save()
#         return HttpResponseRedirect(reverse('admin_staff:users'))
#
#     context = {'title': title, 'user_to_delete': user}
#
#     return render(request, 'adminapp/user_delete.html', context)


class CategoriesListView(LoginRequiredMixin, ListView):
    login_url = '/auth/login/'
    model = ProductCategory
    template_name = 'adminapp/categories.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CategoriesListView, self).get_context_data()
        context['title'] = 'админка/категории'
        context['objects'] = self.object_list
        return context


# @user_passes_test(lambda u: u.is_superuser)
# def categories(request):
#     title = 'админка/категории'
#
#     categories_list = ProductCategory.objects.all()
#
#     context = {
#         'title': title,
#         'objects': categories_list
#     }
#
#     return render(request, 'adminapp/categories.html', context)


class CategoryCreateView(LoginRequiredMixin, CreateView):
    login_url = '/auth/login/'
    model = ProductCategory
    form_class = ProductCategoryCreateForm
    template_name = 'adminapp/category_create.html'

    def get_success_url(self):
        return reverse('adminapp:categories')


# @user_passes_test(lambda u: u.is_superuser)
# def category_create(request):
#     if request.method == 'POST':
#         category_form = ProductCategoryCreateForm(request.POST)
#         if category_form.is_valid():
#             category_form.save()
#             return HttpResponseRedirect(reverse('adminapp:categories'))
#         return HttpResponseRedirect(reverse('adminapp:category_create'))
#     else:
#         category_form = ProductCategoryCreateForm()
#     context = {
#         'form': category_form
#     }
#     return render(request, 'adminapp/category_create.html', context)


class CategoryUpdateView(LoginRequiredMixin, UpdateView):
    login_url = '/auth/login/'
    model = ProductCategory
    form_class = ProductCategoryEditForm
    template_name = 'adminapp/category_update.html'

    def get_success_url(self):
        return reverse('adminapp:categories')

    def get_context_data(self, **kwargs):
        context = super(CategoryUpdateView, self).get_context_data()
        context['category_to_update'] = self.object
        return context

    def form_valid(self, form):
        if 'discount' in form.cleaned_data:
            discount = form.cleaned_data['discount']
            if discount:
                self.object.product_set.update(price=F('price') * (1 - discount / 100))
                db_profile_by_type(self.__class__, 'UPDATE', connection.queries)

        return super().form_valid(form)


# @user_passes_test(lambda u: u.is_superuser)
# def category_update(request, pk):
#     category_to_update = get_object_or_404(ProductCategory, pk=pk)
#     if request.method == 'POST':
#         category_form = ProductCategoryCreateForm(request.POST, instance=category_to_update)
#         if category_form.is_valid():
#             category_form.save()
#             return HttpResponseRedirect(reverse('adminapp:categories'))
#         return HttpResponseRedirect(reverse('adminapp:category_update', args=[category_to_update.pk]))
#     else:
#         category_form = ProductCategoryCreateForm(instance=category_to_update)
#     context = {
#         'form': category_form,
#         'category_to_update': category_to_update,
#     }
#     return render(request, 'adminapp/category_update.html', context)


class CategoryDeleteView(LoginRequiredMixin, DeleteView):
    login_url = '/auth/login/'
    model = ProductCategory
    template_name = 'adminapp/category_delete.html'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_deleted = True
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('adminapp:categories')

    def get_context_data(self, **kwargs):
        context = super(CategoryDeleteView, self).get_context_data()
        context['category_to_delete'] = self.object
        return context


# @user_passes_test(lambda u: u.is_superuser)
# def category_delete(request, pk):
#     category_to_delete = get_object_or_404(ProductCategory, pk=pk)
#     if request.method == 'POST':
#         category_to_delete.is_deleted = True
#         category_to_delete.save()
#         return HttpResponseRedirect(reverse('adminapp:categories'))
#     context = {
#         'category_to_delete': category_to_delete,
#     }
#     return render(request, 'adminapp/category_delete.html', context)


class ProductListView(LoginRequiredMixin, ListView):
    login_url = '/auth/login/'
    model = Product
    template_name = 'adminapp/products.html'

    def get_queryset(self):
        self.category = get_object_or_404(ProductCategory, pk=self.kwargs.get('pk'))
        return self.model.objects.filter(category__pk=self.category.pk).order_by('name')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductListView, self).get_context_data()
        context['category'] = self.category
        context['objects'] = self.get_queryset()
        context['title'] = 'админка/продукт'
        return context


# @user_passes_test(lambda u: u.is_superuser)
# def products(request, pk):
#     title = 'админка/продукт'
#
#     category = get_object_or_404(ProductCategory, pk=pk)
#     products_list = Product.objects.filter(category__pk=pk).order_by('name')
#
#     context = {
#         'title': title,
#         'category': category,
#         'objects': products_list,
#     }
#
#     return render(request, 'adminapp/products.html', context)


class ProductCreateView(LoginRequiredMixin, CreateView):
    login_url = '/auth/login/'
    model = Product
    form_class = ProductEditForm
    template_name = 'adminapp/product_create.html'

    def get_success_url(self):
        return reverse('admin_staff:products', args=[self.kwargs.get('pk')])

    def get_context_data(self, **kwargs):
        context = super(ProductCreateView, self).get_context_data()
        category = get_object_or_404(ProductCategory, pk=self.kwargs.get('pk'))
        self.initial = {'category': category}
        context['category'] = category
        context['update_form'] = self.get_form()
        context['title'] = 'продукты/создание'
        return context


# @user_passes_test(lambda u: u.is_superuser)
# def product_create(request, pk):
#     title = 'продукты/создание'
#
#     category = get_object_or_404(ProductCategory, pk=pk)
#
#     if request.method == 'POST':
#         product_form = ProductEditForm(request.POST, request.FILES)
#         if product_form.is_valid():
#             product_form.save()
#
#             return HttpResponseRedirect(reverse('admin_staff:products', args=[pk]))
#     else:
#         product_form = ProductEditForm(initial={'category': category})
#
#     context = {
#         'title': title,
#         'update_form': product_form,
#         'category': category,
#     }
#
#     return render(request, 'adminapp/product_create.html', context)


class ProductReadListView(LoginRequiredMixin, ListView):
    login_url = '/auth/login/'
    model = Product
    template_name = 'adminapp/product_read.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductReadListView, self).get_context_data()
        self.product = get_object_or_404(self.model, pk=self.kwargs.get('pk'))
        context['product'] = self.product
        context['category'] = get_object_or_404(ProductCategory, pk=self.product.category.pk)
        return context


# @user_passes_test(lambda u: u.is_superuser)
# def product_read(request, pk):
#     title = 'продукты/подробнее'
#
#     product = get_object_or_404(Product, pk=pk)
#     category = get_object_or_404(ProductCategory, pk=product.category.pk)
#     context = {'title': title,
#                'product': product,
#                'category': category,
#                }
#     print(product.img)
#     return render(request, 'adminapp/product_read.html', context)

class ProductUpdateView(LoginRequiredMixin, UpdateView):
    login_url = '/auth/login/'
    model = Product
    template_name = 'adminapp/product_update.html'
    form_class = ProductEditForm

    def get_success_url(self):
        return reverse('admin_staff:product_update', args=[self.object.pk])

    def get_context_data(self, **kwargs):
        context = super(ProductUpdateView, self).get_context_data()
        context['update_form'] = self.get_form()
        context['product'] = self.object
        context['category'] = self.object.category

        return context


# @user_passes_test(lambda u: u.is_superuser)
# def product_update(request, pk):
#     title = 'продукты/редактирование'
#
#     product = get_object_or_404(Product, pk=pk)
#
#     if request.method == 'POST':
#         product_form = ProductEditForm(request.POST, request.FILES, instance=product)
#         if product_form.is_valid():
#             product_form.save()
#
#             return HttpResponseRedirect(reverse('admin_staff:product_update', args=[product.pk]))
#     else:
#         product_form = ProductEditForm(instance=product)
#
#     context = {
#         'title': title,
#         'update_form': product_form,
#         'category': product.category,
#         'product': product,
#     }
#
#     return render(request, 'adminapp/product_update.html', context)


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    login_url = '/auth/login/'
    model = Product
    template_name = 'adminapp/product_delete.html'

    def get_success_url(self):
        return reverse('admin_staff:products', args=[self.object.category.pk])

    def get_context_data(self, **kwargs):
        context = super(ProductDeleteView, self).get_context_data()
        context['product_to_delete'] = self.object
        return context

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_deleted = True
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


# @user_passes_test(lambda u: u.is_superuser)
# def product_delete(request, pk):
#     title = 'продукты/удаление'
#
#     product_to_delete = get_object_or_404(Product, pk=pk)
#
#     if request.method == 'POST':
#         product_to_delete.is_deleted = True
#         product_to_delete.save()
#         return HttpResponseRedirect(reverse('admin_staff:products', args=[product_to_delete.category.pk]))
#
#     context = {'title': title, 'product_to_delete': product_to_delete}
#
#     return render(request, 'adminapp/product_delete.html', context)

def db_profile_by_type(prefix, type, queries):
    update_queries = list(filter(lambda x: type in x['sql'], queries))
    print(f'db_profile {type} for {prefix}:')
    [print(query['sql']) for query in update_queries]


@receiver(pre_save, sender=ProductCategory)
def product_is_active_update_productcategory_save(sender, instance, **kwargs):
    if instance.pk:
        instance.product_set.update(is_deleted=False)
    else:
        instance.product_set.update(is_deleted=True)

    db_profile_by_type(sender, 'UPDATE', connection.queries)
