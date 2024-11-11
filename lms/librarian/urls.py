from django.urls import path
from .import views

urlpatterns = [
    path('', views.index, name='librarian-index'),
    path('profile/', views.profile, name='librarian-profile'),
    path('manage-eresources/', views.manage_eresources, name='manage-eresources'),
    path('update-eresources/', views.update_eresources, name='update-eresources'),
    path('users/', views.users, name='librarian-users'),
    path('reports/', views.reports, name='librarian-reports'),
    path('logout_user/', views.logout_user, name="logout_user"),
    path('update_profile/<int:id>', views.update_profile, name="update-profile"),
    path('update_users/', views.update_users, name="update-users"),
    path('delete_user/<int:id>', views.delete_user, name="delete-user"),
    path('delete_book/<int:id>', views.delete_book, name="delete-book"),
    path('update_customer/<int:id>', views.update_customer, name="update-customer"),
    path('customer_info/<int:id>', views.customer_info, name="customer-info"),
    path('download/<int:file_id>/', views.download_file, name='file_download'),
    path('update_doc/<int:id>', views.update_doc, name="update_doc"),
    path('update_single_book/<int:id>/', views.update_single_book, name="Update-single-book"),
    path('import_id', views.import_id, name="import_id"),
    path('import-students-id', views.import_students_id, name="import-students-id"),
    path('feedbacks/', views.feedbacks, name="feedbacks"),
    path('delete_feedback/<int:id>/', views.delete_feedback, name="delete_feedback"),
    path('librarian_search_book/', views.librarian_search_book, name="librarian_search_book"),
]