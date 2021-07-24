from django.urls import path, re_path
from .views import ShopUserLoginView, ShopUserLogoutView, RegisterCreateView, ShopUserEditUpdateView, send_verify_mail, \
    verify, register

app_name = 'authapp'

urlpatterns = [
    path('login/', ShopUserLoginView.as_view(), name='login'),
    path('logout/', ShopUserLogoutView.as_view(), name='logout'),
    # path('register/', RegisterCreateView.as_view(), name='register'),
    path('register/', register, name='register'),
    path('edit/', ShopUserEditUpdateView.as_view(), name='edit'),
    path('verify/<str:email>/<str:activation_key>/', verify, name='verify'),

]
