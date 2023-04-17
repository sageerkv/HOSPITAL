from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.registerpage, name='register'),
    path('login/', views.loginpage, name='login'),
    path('logout/', views.logoutpage, name='logout'),
    path('profile/<username>/', views.profile, name='profile'),
    path('index/', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('booking/', views.booking, name='booking'),
    path('<int:id>/', views.booking, name='booking_update'),
    path('delete/<int:id>/', views.booking_delete, name='booking_delete'),
    path('doctors/', views.doctors, name='doctors'),
    path('department/', views.department, name='department'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),

    path('password_change/', views.password_change, name="password_change"),
]