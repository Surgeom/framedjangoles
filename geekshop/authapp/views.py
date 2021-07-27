from django.shortcuts import render
from .forms import ShopUserLoginForm, ShopUserEditForm, ShopUserRegisterForm
from django.contrib import auth
from django.http import HttpResponseRedirect
from django.urls import reverse
from geekshop.settings import BASE_DIR
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView, UpdateView
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from django.conf import settings
from .models import ShopUser
from django.db import transaction
from authapp.forms import ShopUserProfileEditForm


def send_verify_mail(user):
    verify_link = reverse('auth:verify', args=[user.email, user.activation_key])

    title = f'Подтверждение учетной записи {user.username}'

    message = f'Для подтверждения учетной записи {user.username} на портале \
{settings.DOMAIN_NAME} перейдите по ссылке: \n{settings.DOMAIN_NAME}{verify_link}'

    return send_mail(title, message, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)


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


def register(request):
    title = 'регистрация'
    if request.method == 'POST':
        register_form = ShopUserRegisterForm(request.POST, request.FILES)
        if register_form.is_valid():
            user = register_form.save()
            if send_verify_mail(user):
                print('сообщение подтверждения отправлено')
                return HttpResponseRedirect(reverse('auth:login'))
            else:
                print('ошибка отправки сообщения')
                return HttpResponseRedirect(reverse('auth:login'))
    else:
        register_form = ShopUserRegisterForm()
    context = {
        'title': title,
        'register_form': register_form
    }
    return render(request, 'authapp/register.html', context)


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


@transaction.atomic
def edit(request):
    title = 'редактирование'

    if request.method == 'POST':
        edit_form = ShopUserEditForm(request.POST, request.FILES, instance=request.user)
        profile_form = ShopUserProfileEditForm(request.POST, instance=request.user.shopuserprofile)

        if edit_form.is_valid() and profile_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('auth:edit'))
    else:
        edit_form = ShopUserEditForm(instance=request.user)
        profile_form = ShopUserProfileEditForm(
            instance=request.user.shopuserprofile
        )
    context = {
        'title': title,
        'edit_form': edit_form,
        'profile_form': profile_form
    }

    return render(request, 'authapp/edit.html', context)


def verify(request, email, activation_key):
    try:
        user = ShopUser.objects.get(email=email)
        if user.activation_key == activation_key and not user.is_activation_key_expired():
            user.is_active = True
            user.save()
            auth.login(request, user)
            return render(request, 'authapp/verification.html')
        else:
            print(f'error activation user: {user}')
            return render(request, 'authapp/verification.html')
    except Exception as e:
        print(f'error activation user : {e.args}')
        return HttpResponseRedirect(reverse('index'))
