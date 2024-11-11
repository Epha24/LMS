from django.contrib import admin
from . models import contacts, department, books, User

class AdminContact(admin.ModelAdmin):
    list_display = [
        'fname', 'lname', 'email', 'message'
    ]

admin.site.register(contacts, AdminContact)

class BookAdmin(admin.ModelAdmin):
    list_display = [
        'ISBN', 'title', 'cover', 'file_name', 'author', 'publisher', 'pub_date', 'genre', 'language', 'edition', 'add_date'
    ]
admin.site.register(books, BookAdmin)

class DepartmentAdmin(admin.ModelAdmin):
    list_display = [
        'dep_name',
    ]
admin.site.register(department, DepartmentAdmin)   

admin.site.register(User)