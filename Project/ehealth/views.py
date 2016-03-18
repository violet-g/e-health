from django.shortcuts import render
from django.http import HttpResponse
from ehealth.forms import SearcherForm, LoginForm, RegisterForm,ChangeDetailsForm
from ehealth.models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from ehealth.bing_search import bing_query
from django.db.models import Count
import json



def index(request):
    if request.method == 'POST':
        form_type = request.POST.get('form_type').encode('UTF-8')
        if form_type == 'register':
            login_form = LoginForm()
            register_form = RegisterForm(request.POST)
            if register_form.is_valid():
                register(request.POST)
                return HttpResponseRedirect("dashboard/")
        elif form_type == 'login':
            login_form = LoginForm(request.POST)
            register_form = RegisterForm()
            if login_form.is_valid():
                username = request.POST["username"].strip()
                password = request.POST["password"].strip()
                user = authenticate(username=username,password=password)
                login(request,user)
                return HttpResponseRedirect("dashboard/")
        else:
            return HttpResponse('Unknown error occurred.')
    else:
        register_form = RegisterForm()
        login_form = LoginForm()

    return render(request, 'login/index.html',{
        'login_form': login_form,
        'register_form': register_form,
    })

def register(request):
    newuser = User.objects.create_user(username=request.POST["username"],email= request.POST["email"],
                                       password = request.POST["password"],first_name=request.POST["first_name"],last_name=request.POST["last_name"] )
    newuser.save()
    newSearcher = Searcher(user = User.objects.get(username=request.POST["username"]))
    newSearcher.save()


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
    try:
        Page.objects.annotate(Count("folders")).order_by("-folders__count")
        print Page.objects.annotate(Count("folders")).order_by("-folders__count")
    except:
        print "stuff broke"
    return render(request, 'dashboard.html',context_dict)



#on all except statements needs to redirect to dashboard
def profile(request,username):
    if request.method=="POST":
        form = ChangeDetailsForm(request.POST)
        if form.is_valid():
            errors = []
            user = request.user
            user=User.objects.get(username=user)
            if request.POST["password"] and request.POST["password_retype"]:
                if request.POST["password"] == request.POST["password_retype"]:
                    user.set_password(request.POST["password"])
                else:
                    errors += ["Passwords don't match"]
            elif (request.POST["password"] and not request.POST["password_retype"]) or (request.POST["password_retype"] and not request.POST["password"]):
                errors += ["You need to enter your password in both password fields"]
            if request.POST["email"]:
                try:
                    User.objects.get(email=request.POST["email"])
                    errors += ["Email is already in use"]
                except:
                    user.email = request.POST["email"]
            if request.POST["first_name"]:
                user.first_name = request.POST["first_name"]
            if request.POST["last_name"]:
                user.last_name = request.POST["last_name"]
            if errors == []:
                user.save()
                return HttpResponseRedirect("/ehealth/dashboard/")
            else:
                context_dict = getProfileInformation(username,request)
                context_dict["errors"] = errors
            #if form.errors:
            #    context_dict["errors"] = form.errors
            #    print form.errors
                return render(request, 'ehealth/profile.html',context_dict)
    elif request.method=="GET":
        context_dict = getProfileInformation(username,request)
        #update_form = ChangeDetailsForm()
        #context_dict["update_form"] = update_form
        return render(request,"ehealth/profile.html",context_dict)
    #    except:
           # return HttpResponse("Fail")
    #        return HttpResponseRedirect("/ehealth/")

def getProfileInformation(username,request):
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
        if searcher == SessionSearcher:
            ownProfile = True
        else:
            ownProfile = False
        context_dict["ownProfile"] = ownProfile
        return context_dict



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
                user.set_password(request.POST["password"])
                #user.update(password=request.get("password"))
                #user.password = request.get("password")
                #user.password.save()
            # THE EMAIL PART WORKS. REWORK EVERYTHING ELSE LIKE IT
            if request.POST["email"]:
                #HttpResponse("new e-mail found")
                #user.update(email=request.get("email"))
                user.email = request.POST["email"]
                #user.save should be at the end of the function
                #user.save()


            if request.POST["first_name"]:
                user.first_name = request.POST["first_name"]
            if request.POST["last_name"]:
                user.last_name = request.POST["last_name"]
                #user.update(last_name=request.get("last_name"))
            user.save()
            return HttpResponseRedirect("/ehealth/dashboard/")
        else:
            return render(request, 'ehealth/profile.html',{
                "update_form":form,
            })
            
        
def add_page_ajax(request):
    if request.method=="POST" and request.is_ajax():
        print 
        try:
            page = Page.objects.get(url=request.POST["link"])
        except:
            page = Page(title=request.POST["title"],source=request.POST["source"],summary=request.POST["summary"],url=request.POST["link"],times_saved=0)
        
        user = request.user
        user=User.objects.get(username=user)
        searcher=Searcher.objects.get(user=user)

        page.times_saved += 1
        page.save()

        folder = Folder.objects.get(name=request.POST["folder"],user=searcher)
        fp = FolderPage(page=page,folder=folder)
        fp.save()
    return JsonResponse({"success":True})


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
        user=request.user
        user=User.objects.get(username=user)
        searcher=Searcher.objects.get(user=user)
        rem_folder=Folder.objects.get(name=fname, user=searcher)
        
        rem_folder.delete()
        #now a related_name is added("folders"), hence there is a backwards relationship and the next line is actually legal
        
        data={'name': fname}
        return JsonResponse(data)
    return render(request, 'dashboard.html')


def delete_page_ajax(request):
    fname=None
    if request.method == 'POST' and request.is_ajax():
        fname=request.POST['folder']
        link=request.POST['link']
        user=request.user
        user=User.objects.get(username=user)
        searcher=Searcher.objects.get(user=user)
        folder=Folder.objects.get(name=fname, user=searcher)
        rem_page=Page.objects.get(url=link)
        
        print rem_page
        
        FolderPage.objects.get(page=rem_page,folder=folder).delete()
        #now a related_name is added("folders"), hence there is a backwards relationship and the next line is actually legal
        
        data={'name': fname}
        return JsonResponse(data)
    return render(request, 'dashboard.html')    


    
def search_ajax(request):
    if request.method == 'POST' and request.is_ajax():
        cat=request.POST['category']
        query=request.POST['query']
        if str(cat).strip() == "All":
            cat=""
        query=str(query).strip()
        if str(cat).strip() == "Users":
            #handle user searching
            users=[]
            for searcher in Searcher.objects.all():
                user={}
                if not searcher.user.is_superuser:
                    user["username"]=searcher.user.username
                    user["first_name"]=searcher.user.first_name
                    user["last_name"]=searcher.user.last_name
                    user["email"] = searcher.user.email
                    if(query in user["username"] or             #is the query in the username
                        query in user["email"].split("@")[0] or #is it at the beginning of the email
                        query==user["email"]):                  #or is it the whole email
                        
                        users.append(user)
            return JsonResponse({'query':query,'category':cat,"users":users})
            
        
        bing_res = bing_query(cat + " " + query)
        # mp_res = medlineplus_query(cat + " " + query)
        # hf_res = healthfinder_query(cat + " " + query)
        
        data={'query':query,'category':cat, "bing_result":bing_res}
        
        # data={'query':query,'category':cat, "bing_result":bing_res, 
        #     "medlineplus_result":mp_res, "healthfinder_result":hf_res}
            
        return JsonResponse(data)
    return render(request, 'dashboard.html')

@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)

    # Take the user back to the homepage.
    return HttpResponseRedirect('/ehealth/')


    
def checkout_folder_ajax(request):
    if request.method == 'POST' and request.is_ajax():
        folder=request.POST['folder']
        user = request.user
        user=User.objects.get(username=user)
        searcher=Searcher.objects.get(user=user)
        pages=[]
        for f in searcher.folders.all():
            if f.name == folder.strip():
                # print f.pages.all()
                for p in f.pages.all():
                    # print p.serialise()
                    pages.append(p.serialise())
        # print "pages", json.dumps(pages[0])
        return JsonResponse({"folder":folder,"pages":pages})
        # return JsonResponse({"folder":folder,"pages":[]})
#def search()

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
