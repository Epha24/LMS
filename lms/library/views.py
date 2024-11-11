from django.shortcuts import render, redirect
from .models import contacts, books, User
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import authenticate, login

def index(request):
    return render(request, 'library/index.html', {"title" : "Home"})
def about(request):
    return render(request, 'library/about.html', {'title' : 'About Us'})
def contact(request):
    msg = False
    if request.method == "POST":
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        message = request.POST['message']
        savecon = contacts(fname = fname, lname = lname, email = email, message = message)
        savecon.save()
        msg = True
    return render(request, 'library/contact.html', {"title" : "Contact Us", "message" : msg})
def register(request):
    msg = False
    msg2 = False
    exist = False
    if request.method == "POST":
        userID = request.POST['userID']
        username = request.POST['username']
        password = request.POST['password']
        confpassword = request.POST['confpassword']
        if password != confpassword:
            msg2 = True
        else:
            check = User.objects.filter(username=username).count()
            if check > 0:
                exist = True
            else:    
                password = make_password(password)
                savecon = User(uID = userID, username = username, password = password, is_customer = True)
                savecon.save()
                msg = True
    return render(request, 'library/register.html', {'title' : 'Membership Registration', "message2" : msg2, "message":msg, "exist" : exist})
def login_view(request):
    msg2 = False
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None and user.is_customer:
            role = "customer"
            login(request, user)
            request.session['username'] = role
            request.session['userID'] = username
            return redirect('user-index')
        elif user is not None and user.is_head:
            role = "head"
            login(request, user)
            request.session['username'] = role
            request.session['userID'] = username
            return redirect('head-index')
        elif user is not None and user.is_admin:
            role = "admin"
            login(request, user)
            request.session['username'] = role
            request.session['userID'] = username
            return redirect('admin')
        elif user is not None and user.is_librarian:
            role = "librarian"
            login(request, user)
            request.session['username'] = role
            request.session['userID'] = username
            return redirect('librarian-index')
        else:
            msg2 = True
            # return redirect('library-login')
    return render(request, 'library/login.html', {'title' : 'Sign In', "msg2" : msg2})
def e_resources(request):
    academic = books.objects.filter(genre='Academic')
    fiction = books.objects.filter(genre='Fiction')
    scifi = books.objects.filter(genre='SciFi')
    return render(request, 'library/e-resources.html', {"title" : "E-Resources", "academic" : academic, "fiction" : fiction, "scifi" : scifi})
def fictions(request):
    book = books.objects.filter(genre='Fiction')
    return render(request, 'library/fictions.html', {"title" : "Fiction Materials", "book" : book})
def academic(request):
    book = books.objects.filter(genre='Academic')
    return render(request, 'library/academic.html', {"title" : "Academic Books", "book" : book})
def scifi(request):
    book = books.objects.filter(genre='SciFi')
    return render(request, 'library/scifi.html', {"title" : "Science Fiction Books", "book" : book})

