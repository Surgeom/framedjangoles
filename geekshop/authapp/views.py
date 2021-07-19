from django.shortcuts import render
from .forms import ShopUserLoginForm, ShopUserEditForm, ShopUserRegisterForm
from django.contrib import auth
from django.http import HttpResponseRedirect
from django.urls import reverse
from geekshop.settings import BASE_DIR
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView, UpdateView
from .models import ShopUser
from django.shortcuts import get_object_or_404


class ShopUserLoginView(LoginView):
    form_class = ShopUserLoginForm
    template_name = 'authapp/login.html'

    def get_context_data(self, **kwargs):
        context = super(ShopUserLoginView, self).get_context_data(**kwargs)
        context['login_form'] = self.get_form()
        context['next'] = self.get_redirect_url()
        context['title'] = 'вход'
        return context

    def get_success_url(self):
        return reverse('index')

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']

            user = auth.authenticate(username=username, password=password)
            if user and user.is_active:
                auth.login(request, user)
                if 'next' in request.POST.keys():
                    return HttpResponseRedirect(request.POST['next'])
                else:
                    return HttpResponseRedirect(reverse('index'))


# def login(request):
#     title = 'вход'
#     login_form = ShopUserLoginForm(data=request.POST)
#     next = request.GET['next'] if 'next' in request.GET.keys() else ''
#     if request.method == 'POST' and login_form.is_valid():
#         username = request.POST['username']
#         password = request.POST['password']
#
#         user = auth.authenticate(username=username, password=password)
#         if user and user.is_active:
#             auth.login(request, user)
#             if 'next' in request.POST.keys():
#                 return HttpResponseRedirect(request.POST['next'])
#             else:
#                 return HttpResponseRedirect(reverse('index'))
#     context = {
#         'title': title,
#         'login_form': login_form,
#         'next': next
#     }
#     return render(request, 'authapp/login.html', context)

class ShopUserLogoutView(LogoutView):
    def post(self, request, *args, **kwargs):
        print('++++')
        auth.logout(request)
        return HttpResponseRedirect(reverse('index'))


# def logout(request):
#     auth.logout(request)
#     return HttpResponseRedirect(reverse('index'))
#


class RegisterCreateView(CreateView):
    form_class = ShopUserRegisterForm
    template_name = 'authapp/register.html'

    def get_success_url(self):
        return reverse('auth:login')

    def get_context_data(self, **kwargs):
        context = super(RegisterCreateView, self).get_context_data()
        context['register_form'] = self.get_form()
        context['title'] = 'регистрация'
        return context


# def register(request):
#     title = 'регистрация'
#     if request.method == 'POST':
#         register_form = ShopUserRegisterForm(request.POST, request.FILES)
#         if register_form.is_valid():
#             register_form.save()
#             return HttpResponseRedirect(reverse('auth:login'))
#     else:
#         register_form = ShopUserRegisterForm()
#     context = {
#         'title': title,
#         'register_form': register_form
#     }
#     return render(request, 'authapp/register.html', context)

class ShopUserEditUpdateView(UpdateView):
    form_class = ShopUserEditForm
    model = ShopUser
    template_name = 'authapp/edit.html'

    def get_object(self, queryset=None):
        self.object = get_object_or_404(ShopUser, pk=self.request.user.pk)
        return self.object

    def get_success_url(self):
        return reverse('auth:edit')

    def get_context_data(self, **kwargs):
        context = super(ShopUserEditUpdateView, self).get_context_data()
        context['edit_form'] = self.get_form()
        context['title'] = 'редактирование'
        return context

# def edit(request):
#     title = 'редактирование'
#
#     if request.method == 'POST':
#         edit_form = ShopUserEditForm(request.POST, request.FILES, instance=request.user)
#         if edit_form.is_valid():
#             edit_form.save()
#             return HttpResponseRedirect(reverse('auth:edit'))
#     else:
#         edit_form = ShopUserEditForm(instance=request.user)
#
#     context = {
#         'title': title,
#         'edit_form': edit_form
#     }
#
#     return render(request, 'authapp/edit.html', context)
