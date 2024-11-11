from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    return render(request, 'head/index.html', {"title" : "Home"})
@login_required
def profile(request):
    return render(request, 'head/profile.html', {"title" : "Your Profile"})
@login_required
def users(request):
    return render(request, 'head/users.html', {"title" : "Users"})
@login_required
def reports(request):
    return render(request, 'head/reports.html', {"title" : "Reports"})
@login_required
def eresources(request):
    return render(request, 'head/eresources.html', {"title" : "E-Resources"})
