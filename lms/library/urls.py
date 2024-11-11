from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='library-index'),
    path('about/', views.about, name='library-about'),
    path('contact/', views.contact, name='library-contact'),
    path('register/', views.register, name='library-register'),
    path('login/', views.login_view, name='library-login'),
    path('e-resources/', views.e_resources, name='e-resources'),
    path('e-resources/fictions', views.fictions, name='fictions'),
    path('e-resources/academic', views.academic, name='academic'),
    path('e-resources/scifi', views.scifi, name='scifi'),
]