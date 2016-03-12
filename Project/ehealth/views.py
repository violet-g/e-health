from django.shortcuts import render
from django.http import HttpResponse
from ehealth.forms import SearcherForm
from ehealth.models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse



def index(request):
    context = dict()
    return render(request,"ehealth/index.html", context)


# Create your views here.
def register(request):
    if request.method == "POST":
        errors = []
        form = SearcherForm(request.POST)
        if form.is_valid():
            Username = request.POST["username"]
            if User.objects.filter(username=request.POST["username"]).exists() == True:
                errors.append("A user with that username already exists")
                form = SearcherForm
                return render(request,'ehealth/register.html',{"errors":errors,"form":form})
            surname = request.POST["surname"]
            email = request.POST["email"]
            password = request.POST["password"]
            forename = request.POST["forename"]
            newuser = User.objects.create_user(username=Username, email=email, password = password,first_name=forename,last_name=surname )
            newuser.save()
            newSearcher = Searcher.objects.create(user=newuser)
            if request.POST["picture"]:
                newSearcher.picture = request.POST["picture"]
            if request.POST["website"]:
                newSearcher.website = request.POST["website"]
            return HttpResponse("Done")
        else:
            print form.errors
    else:
        form = SearcherForm()
    return render(request, 'ehealth/register.html', {"form": form})


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect('/ehealth/')
            else:
                return HttpResponse("Your account is disabled.")
        else:
            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse("Invalid login details supplied.")

    else:
        return render(request,'ehealth/login.html', {})


@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)

    # Take the user back to the homepage.
    return HttpResponseRedirect('/ehealth/')