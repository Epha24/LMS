from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    uID = models.CharField(max_length=100, default=1)
    is_admin=models.BooleanField('Is admin', default=False)
    is_customer=models.BooleanField('Is customer', default=False)
    is_head=models.BooleanField('Is department head', default=False)
    is_librarian=models.BooleanField('Is librarian', default=False)

class contacts(models.Model):
    fname = models.CharField(max_length=60)
    lname = models.CharField(max_length=60)
    email = models.EmailField(max_length=254)
    message = models.TextField()

class department(models.Model):
    dep_name = models.CharField(max_length=100)

class books(models.Model) :
    ISBN = models.CharField(max_length=13, unique=True)
    cover = models.ImageField(upload_to='books')
    file_name = models.CharField(max_length=255, blank=True)
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    publisher = models.CharField(max_length=100)
    pub_date = models.DateField()
    genre = models.CharField(max_length=50)
    language = models.CharField(max_length=50)
    edition = models.CharField(max_length=50)
    add_date = models.DateTimeField(auto_now_add=True)


    def save(self, *args, **kwargs):
        self.file_name = self.cover.name
        super(books, self).save(*args, **kwargs)