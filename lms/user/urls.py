from django.urls import path
from .import views

urlpatterns = [
    path('', views.index, name='user-index'),
    path('profile/', views.profile, name='user-profile'),
    path('eresources/', views.eresources, name='user-eresources'),
    path('logout_user/', views.logout_user, name="logout_user"),
    path('download/<int:file_id>/', views.download_file, name='file_download'),
    path("search_book/", views.search_book, name="search_book"),
]