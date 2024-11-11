from mimetypes import guess_type
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib import messages
from library.models import User, books
from django.http import FileResponse, Http404
from django.conf import settings
import os
import mimetypes

@login_required
def index(request):
    username = request.session.get('username', '')
    if username  != "customer":
        return redirect('logout_user')
    return render(request, 'user/index.html', {"title" : "Home", "username" : username})
@login_required
def profile(request):
    userID = request.session.get('userID', '')
    userinfo = User.objects.filter(username = userID)
    return render(request, 'user/profile.html', {"title" : "Your Profile", "userinfo" : userinfo})
@login_required
def eresources(request):
    book = books.objects.all()
    return render(request, 'user/eresources.html', {"title" : "E-Resources", "book" : book})
def logout_user(request):
    logout(request)
    request.session.flush()
    messages.success(request, ("You Were Logged Out"))
    return redirect('library-login')

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
def search_book(request):
    messages = False
    if request.method == "POST":
        book_title = request.POST['title']

        book = books.objects.filter(title = book_title)
        num = books.objects.filter(title = book_title).count()

        if num > 0:
            messages = True
    return render(request, 'user/search-book.html', {"title" : "Search Book", "book" : book, "messages" : messages})

