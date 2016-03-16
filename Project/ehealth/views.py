from django.shortcuts import render
from django.http import HttpResponse
from ehealth.forms import SearcherForm, LoginForm, RegisterForm,ChangeDetailsForm
from ehealth.models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse



def index(request):
    if request.method == 'POST':
        form_type = request.POST.get('form_type').encode('UTF-8')
        if form_type == 'register':
            login_form = LoginForm()
            register_form = RegisterForm(request.POST)
            if register_form.is_valid():
                register_form.save(commit=True)
                return HttpResponseRedirect("dashboard/")
                #return HttpResponse('successfully registered')
        elif form_type == 'login':
            login_form = LoginForm(request.POST)
            register_form = RegisterForm()
            if login_form.is_valid():
                username = request.POST["username"].strip()
                password = request.POST["password"].strip()
                user = authenticate(username=username,password=password)
                login(request,user)
                return HttpResponseRedirect("dashboard/")
                #return HttpResponse('successfully logged in')
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
    context_dict={}
    try:
        user = request.user     #get the cureent logged in user

        #get them from the User table and search for them in the searcher table,
        # since the user is of type django User whatever and the search key needs to be of the same type
        user=User.objects.get(username=user)
        searcher=Searcher.objects.get(user=user)

        #now a related_name is added("folders"), hence there is a backwards relationship and the next line is actually legal
        folders = searcher.folders.all()
        context_dict["folders"]=folders
    except:
        return HttpResponseRedirect("/ehealth/")
        #return HttpResponse("something went wrong")
    return render(request, 'dashboard.html',context_dict)



#on all except statements needs to redirect to dashboard
def profile(request,username):
    ownProfile = True
    context_dict={}
    update_form = ChangeDetailsForm()
    context_dict["update_form"] = update_form
    try:
        user = User.objects.get(username=username)
        searcher = Searcher.objects.get(user=user)
        context_dict["ViewedUser"] = [user.first_name,user.last_name,user.email,user.password,searcher.website,searcher.picture]
    except:
        return HttpResponse("User does not exist")
    try:
        SessionUserID = request.user
        SessionUser=User.objects.get(username=SessionUserID)
        SessionSearcher=Searcher.objects.get(user=SessionUser)
    except:
        SessionSearcher=""
    try:
        folders = Folder.objects.filter(user=searcher)
    except:
        return HttpResponse("Cant get folders")
    foldersToParse = []
    try:
        for folder in folders:
            element = [folder,FolderPage.objects.filter(folder=folder)]
            foldersToParse.append(element)
            context_dict["folders"] = foldersToParse
    except:
        return HttpResponse("Cant get pages")
    if searcher == SessionSearcher:
        ownProfile = True
    else:
        ownProfile = False
    context_dict["ownProfile"] = ownProfile
    return render(request,"ehealth/profile.html",context_dict)
#    except:
       # return HttpResponse("Fail")
#        return HttpResponseRedirect("/ehealth/")

@login_required()
def update_profile(request):
    if request.method=="POST":
        form = ChangeDetailsForm(request.POST)
        if form.is_valid():


            user = request.user     #get the cureent logged in user
        #get them from the User table and search for them in the searcher table,
        # since the user is of type django User whatever and the search key needs to be of the same type
            user=User.objects.get(username=user)
            searcher=Searcher.objects.get(user=user)
            if request.POST["password"]:
                user.update(password=request.get("password"))
                #user.password = request.get("password")
                #user.password.save()



            # THE EMAIL PART WORKS. REWORK EVERYTHING ELSE LIKE IT
            if request.POST["email"]:
                #HttpResponse("new e-mail found")
                #user.update(email=request.get("email"))
                user.email = request.POST["email"]
                #user.save should be at the end of the function
                user.save()


            if request.POST["first_name"]:
                user.update(first_name=request.get("first_name"))
            if request.POST["last_name"]:
                user.update(last_name=request.get("last_name"))
            return HttpResponseRedirect("dashboard/")
        else:
            return HttpResponseRedirect("/ehealth/")


def test_ajax(request):
    if request.method=='GET':
        return HttpResponse("MAINA")
    return HttpResponse("No maina")

def new_folder_ajax(request):
    fname=None
    if request.method == 'POST' and request.is_ajax():
        fname=request.POST['folder']
        user = request.user
        user=User.objects.get(username=user)
        searcher=Searcher.objects.get(user=user)
        
        #now a related_name is added("folders"), hence there is a backwards relationship and the next line is actually legal
        new_folder=Folder(user=searcher, name=fname)
        new_folder.save()
        
        data={'name': fname}
        return JsonResponse(data)
    return render(request, 'dashboard.html')

def delete_folder_ajax(request):
    fname=None
    if request.method == 'POST' and request.is_ajax():
        fname=request.POST['folder']
        
        #now a related_name is added("folders"), hence there is a backwards relationship and the next line is actually legal
        delete_folder=Folder.objects.filter(name=fname)
        delete_folder.delete()
        
        data={'name': fname}
        return JsonResponse(data)
    return render(request, 'dashboard.html')
    
def search_ajax(request):
    if request.method == 'POST' and request.is_ajax():
        cat=request.POST['category']
        query=request.POST['query']
        data={'query':query,'category':cat}
        return JsonResponse(data)
    return render(request, 'dashboard.html')

@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)

    # Take the user back to the homepage.
    return HttpResponseRedirect('/ehealth/')



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
