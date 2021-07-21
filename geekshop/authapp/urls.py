from django.urls import path
from .views import  ShopUserLoginView ,ShopUserLogoutView,RegisterCreateView,ShopUserEditUpdateView

app_name = 'authapp'

urlpatterns = [
    path('login/', ShopUserLoginView.as_view(), name='login'),
    path('logout/', ShopUserLogoutView.as_view(), name='logout'),
    path('register/', RegisterCreateView.as_view(), name='register'),
    path('edit/', ShopUserEditUpdateView.as_view(), name='edit'),
]
