from django.shortcuts import render
from django.http import HttpResponse
from ehealth.forms import SearcherForm, LoginForm, RegisterForm
from ehealth.models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse



def index(request):
    if request.method == 'POST':
        form_type = request.POST.get('form_type').encode('UTF-8')
        if form_type == 'register':
            login_form = LoginForm()
            register_form = RegisterForm(request.POST)
            if register_form.is_valid():
                register_form.save(commit=True)
                return HttpResponse('successfully registered')
        elif form_type == 'login':
            print request.POST
            login_form = LoginForm(request.POST)
            register_form = RegisterForm()
            if login_form.is_valid():
                return HttpResponse('successfully logged in')
        else:
            return HttpResponse('Unknown error occurred.')
    else:
        register_form = RegisterForm()
        login_form = LoginForm()

    return render(request, 'login/index.html',{
        'login_form': login_form,
        'register_form': register_form,
    })


def dashboard(request):
    return render(request, 'dashboard.html')


#
# Create your views here.
#def register(request):
#    if request.method == "POST":
#        errors = []
#        form = SearcherForm(request.POST)
#        if form.is_valid():
#            Username = request.POST["username"]
#            if User.objects.filter(username=request.POST["username"]).exists() == True:
#                errors.append("A user with that username already exists")
#                form = SearcherForm
#                return render(request,'ehealth/register.html',{"errors":errors,"form":form})
#            surname = request.POST["surname"]
#            email = request.POST["email"]
#            password = request.POST["password"]
#            forename = request.POST["forename"]
#            newuser = User.objects.create_user(username=Username, email=email, password = password,first_name=forename,last_name=surname )
#            newuser.save()
#            newSearcher = Searcher.objects.create(user=newuser)
#            if request.POST["picture"]:
#                newSearcher.picture = request.POST["picture"]
#            if request.POST["website"]:
#                newSearcher.website = request.POST["website"]
#            return HttpResponse("Done")
#        else:
#            print form.errors
#    else:
#        form = SearcherForm()
#    return render(request, 'ehealth/register.html', {"form": form})


#def user_login(request):
#    if request.method == 'POST':
#        username = request.POST.get('username')
#        password = request.POST.get('password')
#        user = authenticate(username=username, password=password)
#        if user:
#            if user.is_active:
#                login(request,user)
#                return HttpResponseRedirect('/ehealth/')
#            else:
#                return HttpResponse("Your account is disabled.")
#        else:
#            print "Invalid login details: {0}, {1}".format(username, password)
#           return HttpResponse("Invalid login details supplied.")

#    else:
#        return render(request,'ehealth/login.html', {})


@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)

    # Take the user back to the homepage.
    return HttpResponseRedirect('/ehealth/')