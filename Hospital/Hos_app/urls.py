from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('index/', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('booking/', views.booking, name='booking'),
    path('doctors/', views.doctors, name='doctors'),
    path('contacts/', views.contacts, name='contacts'),
    path('department/', views.department, name='department'),
    path('register/', views.registerpage, name='register'),
    path('login/', views.loginpage, name='login'),
    path('logout/', views.logoutpage, name='logout'),
]