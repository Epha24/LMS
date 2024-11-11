from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='head-index'),
    path('profile/', views.profile, name='head-profile'),
    path('users/', views.users, name='head-users'),
    path('reports/', views.reports, name='head-reports'),
    path('eresources/', views.eresources, name='head-eresources'),
]