from mimetypes import guess_type
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from library.models import User, books, contacts
from django.contrib.auth import logout
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from django.http import FileResponse, Http404
from django.conf import settings
import os
import mimetypes
import csv

@login_required
def index(request):
    username = request.session.get('username', '')
    if username  != "librarian":
        return redirect('logout_user')
    return render(request, 'librarian/index.html', {"title" : "Home", "username" : username})
@login_required
def profile(request):
    userID = request.session.get('userID', '')
    userinfo = User.objects.filter(username = userID)
    return render(request, 'librarian/profile.html', {"title" : "Your Profile", "userinfo" : userinfo})
@login_required
def users(request):
    msg = False
    msg2 = False
    if request.method == "POST":
        userID = request.POST['userID']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        confpassword = request.POST['confpassword']
        if password != confpassword:
            msg2 = True
        else:
            password = make_password(password)
            savecon = User(uID = userID, first_name = fname, last_name = lname, email = email, username = username, password = password, is_customer = True)
            savecon.save()
            msg = True
    return render(request, 'librarian/users.html', {'title' : 'Users', "message2" : msg2, "message":msg})
@login_required
def reports(request):
    return render(request, 'librarian/reports.html', {"title" : "Reports"})
@login_required
def manage_eresources(request):
    msg = False
    msg2 = False
    if request.method == "POST":
        isbn = request.POST['isbn']
        book = request.FILES['book']
        title = request.POST['title']
        author = request.POST['author']
        publisher = request.POST['publisher']
        pdate = request.POST['pdate']
        genre = request.POST['genre']
        language = request.POST['language']
        edition = request.POST['edition']

        num = books.objects.filter(ISBN=isbn).count()

        if(num > 0):
                msg2 = True
        else:
                savecon = books(ISBN = isbn, cover = book, title = title, author = author, publisher = publisher, pub_date = pdate, genre = genre, language = language, edition = edition)
                savecon.save()
                msg = True
    return render(request, 'librarian/eresources.html', {"title" : "E-Resources", "msg" : msg, "msg2" : msg2})
@login_required
def update_eresources(request):
    resources = books.objects.all()
    return render(request, 'librarian/update-eresources.html', {"title" : "E-Resources", "resources" : resources})
def logout_user(request):
    logout(request)
    request.session.flush()
    messages.success(request, ("You Were Logged Out"))
    return redirect('library-login')
def update_profile(request, id):
    id = request.POST['id']
    fname = request.POST['fname']
    lname = request.POST['lname']
    uemail = request.POST['email']
    uname = request.POST['username']

    userinfo = User.objects.get(id=id)
    userinfo.username = uname
    userinfo.first_name = fname
    userinfo.last_name = lname
    userinfo.email = uemail
    userinfo.save()
    success_msg = True

    userinfo = User.objects.filter(id=id)
    return render(request, 'librarian/profile.html', {'userinfo' : userinfo, "success_msg" : success_msg, "title":"Your Prifile"})

def customer_info(request, id):
    userinfo = User.objects.filter(id = id)
    return render(request, 'librarian/customer-update.html', {"title" : "Users", "userinfo" : userinfo})
def update_customer(request, id):
    password_error = False
    id = request.POST['id']
    fname = request.POST['fname']
    lname = request.POST['lname']
    uemail = request.POST['email']
    uname = request.POST['username']
    # password = request.POST['password']
    # confpassword = request.POST['confpassword']
    # if password != confpassword:
    #     password_error = True
    # else:
    userinfo = User.objects.get(id=id)
    userinfo.username = uname
    userinfo.first_name = fname
    userinfo.last_name = lname
    userinfo.email = uemail
    userinfo.userID = id
    # userinfo.password = password
    userinfo.save()
    success_msg = True

    userinfo = User.objects.filter(id=id)
    return render(request, 'librarian/customer-update.html', {'title':'Users','userinfo' : userinfo, "success_msg" : success_msg, "password_error" : password_error})
def update_doc(request, id):
    msg_error = False
    password_error = False
    isbn = request.POST['isbn']
    book = request.FILES['book']
    title = request.POST['title']
    author = request.POST['author']
    publisher = request.POST['publisher']
    pub_date = request.POST['pub_date']
    genre = request.POST['genre']
    language = request.POST['language']
    edition = request.POST['edition']

    # check = books.objects.filter(id != id, ISBN = isbn).count()
    # if(check > 0):
    #     msg_error = True
    # else:
    bookinfo = books.objects.get(id=id)
    bookinfo.ISBN = isbn
    bookinfo.cover = book
    bookinfo.title = title
    bookinfo.author = author
    bookinfo.publisher = publisher
    bookinfo.pub_date = pub_date
    bookinfo.genre = genre
    bookinfo.language = language
    bookinfo.edition = edition

    bookinfo.save()
    success_msg = True

    book = books.objects.filter(id=id)
    return render(request, 'librarian/update_books.html', {'book' : book, "success_msg" : success_msg, "msg_error" : msg_error})    
def update_users(request):
    num = 1
    customers = User.objects.filter(is_customer = True)
    return render(request, 'librarian/update-user.html', {"title" : "Users", 'customers' : customers, "num" : num})
def delete_book(request, id):
    delete_book = books.objects.get(id=id)
    delete_book.delete()
    delete_msg = True
    resources = books.objects.all()
    return render(request, 'librarian/update-eresources.html', {"title" : "E-Resources", 'resources' : resources, "delete_msg" : delete_msg})

def delete_user(request, id):
    delete_user = User.objects.get(id=id)
    delete_user.delete()
    delete_msg = True
    customers = User.objects.filter(is_customer = True)
    return render(request, 'librarian/update-user.html', {"title" : "Users", 'customers' : customers, "delete_msg" : delete_msg})


def download_file(request, file_id):
    document = get_object_or_404(books, id=file_id)
    file_path = document.cover.path
    if os.path.exists(file_path):
        mime_type, _ = guess_type(file_path)
        if mime_type is None:
            mime_type = 'application/octet-stream'
        response = FileResponse(open(file_path, 'rb'), content_type=mime_type)
        response['Content-Disposition'] = f'attachment; filename="{document.cover.name}"'
        return response
    else:
        raise Http404("File does not exist")
def update_single_book(request, id):
    book = books.objects.filter(id = id)

    return render(request, 'librarian/update_books.html', {"title" : "E-Resources", "book" : book})

def import_id(request):
    message = False
    error_msg = False
    if request.method == 'POST':
        studID = request.POST['studID']
        
        check = User.objects.filter(uID = studID).count()
        if(check > 0):
            error_msg = True
        else :
            savedata = User(uID = studID, is_customer = True)
            savedata.save()
            message = True
    return render(request, 'librarian/import-student.html', {'title': "Users", "message" : message, "error_msg" : error_msg})

def import_students_id(request):
    return render(request, "librarian/import-student.html", {"title" : "Users"})

def feedbacks(request):
    feedba = contacts.objects.all()

    return render(request, 'librarian/feedbacks.html', {"title" : "Feedbacks", "feedba" : feedba})

def delete_feedback(request, id):
    delete_msg = False
    feedback = contacts.objects.get(id = id)

    feedback.delete()

    feedba = contacts.objects.all()
    delete_msg = True
    return render(request, 'librarian/feedbacks.html', {"title" : "Feedbacks", "feedba" : feedba, "delete_msg" : delete_msg})
def librarian_search_book(request):
    messages = False
    if request.method == "POST":
        book_title = request.POST['title']

        book = books.objects.filter(title = book_title)
        num = books.objects.filter(title = book_title).count()

        if num > 0:
            messages = True
    return render(request, 'user/search-book.html', {"title" : "Search Book", "book" : book, "messages" : messages})