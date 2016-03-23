from django.shortcuts import render
from django.http import HttpResponse
from ehealth.forms import LoginForm, RegisterForm,ChangeDetailsForm
from ehealth.models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from ehealth.bing_search import bing_query
from ehealth.healthfinder_search import healthfinder_query
from textstat.textstat import textstat
from django.contrib.auth.models import User
import codecs
from textblob import *
from django.utils.encoding import *
from ehealth.MedlinePlus_search import medlinePlus_query
from django.db.models import Count
import json
import urllib2
from django.core.validators import validate_email


def index(request):
    #if the user is sending a post request
    if request.method == 'POST':
        form_type = request.POST.get('form_type').encode('UTF-8')
        #if the user is trying to register, we check if the form is valid, and if it is, we register the user and log him in.
        if form_type == 'register':
            login_form = LoginForm()
            register_form = RegisterForm(request.POST)
            if register_form.is_valid():
                #if a user successfuly registers as AnonymousUser, he can go to profiles and automatically log himself in, which we dont want
                if request.POST["username"] != "AnonymousUser":
                    register(request.POST["username"],request.POST["email"],request.POST["password"],request.POST["first_name"],request.POST["last_name"])
                    user = authenticate(username = request.POST["username"].strip(),password = request.POST["password"].strip())
                    login(request,user)
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

#an extra function, used in the index function, when a user is registering
def register(username,email,password,first_name,last_name):
    newuser = User.objects.create_user(username=username,email=email,
                                       password = password,first_name = first_name,last_name = last_name)
    newuser.save()
    newSearcher = Searcher(user = User.objects.get(username=username))
    newSearcher.save()


#finds the information about the currently logged in user as well as the most saved pages in general.
def dashboard(request):
    context_dict={}
    try:
        user = request.user
        user=User.objects.get(username=user)
        searcher=Searcher.objects.get(user=user)
        folders = searcher.folders.all()
        context_dict["folders"]=folders
    except:
        #if it can't find the user, we assume he is not properly logged in and redirect him back to the starting page
        return HttpResponseRedirect("/ehealth/")
    try:
        topPages = Page.objects.order_by("times_saved")[:15]
        for page in topPages:
            page.summary=page.summary[:300] + "..."
        context_dict["pages"] = topPages
    except:
        #even if the top pages aren't found, the user can still use the website for its intended purpose, no need for redirecting
        print "Can't find top pages"
    return render(request, 'dashboard.html',context_dict)



#if the user is sending a GET request, we get and display the information of the profile he is searching for
def profile(request,username):
    if request.method=="POST":
        #if we get here, it means that the user is trying to change his profile information
        form = ChangeDetailsForm(request.POST)
        if form.is_valid():
            #if the form he has submitted is valid, check whether the two password fields match, the email is not taken
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
                    emailTaken = User.objects.get(email=request.POST["email"])
                    emailTaken = True
                except:
                    emailTaken = False
                if emailTaken == True:
                    errors += ["Email is already taken"]
                else:
                    user.email = request.POST["email"]
            if request.POST["first_name"]:
                user.first_name = request.POST["first_name"]
            if request.POST["last_name"]:
                user.last_name = request.POST["last_name"]
            if errors == []:
                #if there are no errors, save the changes made to the user profile and return him to his profile
                user.save()
                return HttpResponseRedirect("/ehealth/profile/")
            else:
                #if there are errors, return him back to the profile page with the form for information change
                context_dict = getProfileInformation(username,request)
                context_dict["errors"] = errors
                return render(request, 'ehealth/profile.html',context_dict)
        else:
            #if the form isnt valid, return the user back to the profile page with the information change form
            context_dict = getProfileInformation(username,request)
            context_dict["errors"] = ["Form is not valid, please try again"]
            return render(request, 'ehealth/profile.html',context_dict)
    elif request.method=="GET":
        context_dict = getProfileInformation(username,request)
        return render(request,"ehealth/profile.html",context_dict)

#this function is used in the profile function. Its purpose is to get the information about the user that is logged in,
#the profile information that the user is trying to access, as well as whether he is trying to view his own profile or not.
def getProfileInformation(username,request):
    ownProfile = True
    context_dict={}
    update_form = ChangeDetailsForm()
    context_dict["update_form"] = update_form
    context_dict["logged_in"]=True
    own_folders=[]
    try:
        user = User.objects.get(username=username)
        searcher = Searcher.objects.get(user=user)
    except:
        return HttpResponse("User does not exist")
    try:
        SessionUserID = request.user
        SessionUser=User.objects.get(username=SessionUserID)
        SessionSearcher=Searcher.objects.get(user=SessionUser)
    except:
        SessionSearcher=""
        context_dict["logged_in"]=False
    if searcher == SessionSearcher:
        ownProfile = True
    else:
        ownProfile = False
    context_dict["ownProfile"] = ownProfile
    if ownProfile==True:
        folders = Folder.objects.filter(user=searcher)
    elif ownProfile==False:
        folders = Folder.objects.filter(user=searcher,public=True)
    
    context_dict["folders"] = folders
    searcher_public = searcher.public
    context_dict["ViewedUser"] = {"public":searcher.public,
                                "first_name":user.first_name,
                                "last_name":user.last_name,
                                "email":user.email,
                                }
    try:
        own_folders = Folder.objects.filter(user=SessionSearcher)
        context_dict["own_folders"] = own_folders
    except:
        pass
    return context_dict

#this function is used only to redirect an user to their profile, in case they type /ehealth/profile/ in the url field
#instead of ehealth/profile/profilename
def profileRedirect(request):
    try:
        user = request.user
        user=User.objects.get(username=user)
        return HttpResponseRedirect("/ehealth/profile/"+user.username+"/")
    except:
        return HttpResponseRedirect("/ehealth/")

#This function adds a page to a user-made folder
def add_page_ajax(request):
    if request.method=="POST" and request.is_ajax():
        try:
            page = Page.objects.get(url=request.POST["link"].strip())
        except:
            page = Page(title=request.POST["title"].strip(),source=request.POST["source"].strip(),summary=request.POST["summary"].strip(),url=request.POST["link"].strip(),times_saved=0)
            try:
                temp = calculateScores(page.summary)
                page.readability_score = temp["readability_score"]
                page.sentiment_score = temp["sentiment_score"]
                page.subjectivity_score = temp["subjectivity_score"]
            except:
                pass
        user = request.user
        user=User.objects.get(username=user)
        searcher=Searcher.objects.get(user=user)
        print "summary",page.source
        page.times_saved += 1
        # print page.summary
        page.save()

        folder = Folder.objects.get(name=request.POST["folder"].strip(),user=searcher)
        try:
            fp = FolderPage.objects.get(page=page,folder=folder)
            page.times_saved -= 1
        except:
            fp = FolderPage.objects.get_or_create(page=page,folder=folder)[0]
            fp.save()
        return JsonResponse({"success":True})
    return JsonResponse({"success":False})


def test_ajax(request):
    if request.method=='POST' and request.is_ajax():
        return HttpResponse("MAINA")
    return HttpResponse("No maina")

def save_folder_privacy_ajax(request):
    if request.method=='POST' and request.is_ajax():
        user = request.user
        user=User.objects.get(username=user)
        searcher=Searcher.objects.get(user=user)
        for f in json.loads(request.POST['folders']):
            print f['folder'],f['privacy']
            folder = Folder.objects.get(user=searcher, name=f['folder'])
            folder.public= True if f['privacy']=="Public" else False
            folder.save()
        return JsonResponse({"maina":"maina"})
    return HttpResponse("No maina")
    

def privacy_details_ajax(request):
    user = request.user
    print user
    try:
        user=User.objects.get(username=user)
        searcher=Searcher.objects.get(user=user)
    except:
        searcher=Searcher() # create an empty searcher - that's fine because we would only need the public field
                            # and it breaks when the user is not logged in
        
    if request.method=='POST' and request.is_ajax():
        if request.POST['publicity']=="Public":
            searcher.public=True
        elif request.POST['publicity']=="Hidden":
            searcher.public=False
        searcher.save()
        return HttpResponse('success')
    if request.method=='GET':
        return JsonResponse({"public":searcher.public})


#This function for adding a new user profile
def new_folder_ajax(request):
    fname=None
    if request.method == 'POST' and request.is_ajax():
        fname=request.POST['folder']
        user = request.user
        user=User.objects.get(username=user)
        searcher=Searcher.objects.get(user=user)
        data={'name': fname, "repeat":True}
        #now a related_name is added("folders"), hence there is a backwards relationship and the next line is actually legal
        if not Folder.objects.filter(user=searcher, name=fname):
            new_folder=Folder(user=searcher, name=fname)
            new_folder.save()
            data["repeat"]=False
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
        mp_res = medlinePlus_query(cat + " " + query)
        hf_res = healthfinder_query(cat + " " + query)

        #sort results based on how many conditions they meet
        for result in bing_res:
            result["summary"] = result["summary"].encode('ASCII','ignore')
            try:
                temp = calculateScores(result['summary'])
            except:
                continue
            
            result["readability_score"] = temp["readability_score"]
            result["subjectivity_score"] = temp["subjectivity_score"]
            result["sentiment_score"] = temp["sentiment_score"]
        for result in mp_res:
            result["summary"] = result["summary"].encode('ASCII','ignore')
            try:
                temp = calculateScores(result["summary"])
            except:
                continue
            result["readability_score"] = temp["readability_score"]
            result["subjectivity_score"] = temp["subjectivity_score"]
            result["sentiment_score"] = temp["sentiment_score"]
        for result in hf_res:
            result["summary"] = result["summary"].encode('ASCII','ignore')
            try:
                temp = calculateScores(result["summary"])
            except:
                continue
            result["readability_score"] = temp["readability_score"]
            result["subjectivity_score"] = temp["subjectivity_score"]
            result["sentiment_score"] = temp["sentiment_score"]

        print "readability: " + request.POST["readability_score"]
        print "sentiment: " + request.POST["sentiment_score"]
        print "subjectivity: " + request.POST["subjectivity_score"]
        readabilityS = int(request.POST["readability_score"])
        sentimentS = int(request.POST["sentiment_score"])
        subjectivityS = int(request.POST["subjectivity_score"])
        bing_res = sortResults(bing_res,readabilityS,sentimentS,subjectivityS)
        mp_res = sortResults(mp_res,readabilityS,sentimentS,subjectivityS)
        hf_res = sortResults(hf_res,readabilityS,sentimentS,subjectivityS)
        data={'query':query,'category':cat, "bing_result":bing_res,
            "medlineplus_result":mp_res, "healthfinder_result":hf_res}
        return JsonResponse(data)
    return render(request, 'dashboard.html')


def sortResults(results,readability,sentiment,subjectivity):
    toBack = []
    AllConditions = []
    TwoConditions = []
    OneCondition = []
    for result in results:
        conditionsMet = 0
        if result["readability_score"] >= readability:
            conditionsMet += 1
        if result["sentiment_score"] > sentiment-10:
            conditionsMet += 1
        if result["subjectivity_score"] > subjectivity-10 and result["subjectivity_score"] < subjectivity+10:
            conditionsMet += 1
        if conditionsMet == 3:
            AllConditions.append(result)
        elif conditionsMet == 2:
            TwoConditions.append(result)
        elif conditionsMet == 1:
            OneCondition.append(result)
        else:
            toBack.append(result)
    return AllConditions + TwoConditions + OneCondition + toBack
#content = unicode(q.content.strip(codecs.BOM_UTF8), 'utf-8')

def calculateScores(text):
    text = smart_bytes(text,encoding="utf-8",strings_only=False,errors="replace")
    temp = TextBlob(text)
    toReturn = {}
    toReturn["readability_score"] = textstat.flesch_reading_ease(text)
    toReturn["subjectivity_score"] = temp.sentiment.subjectivity * 100
    toReturn["sentiment_score"] = (temp.sentiment.polarity + 1) * 50
    return toReturn

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
        if(request.POST["user"].strip()):
            user=request.POST["user"]
        user=User.objects.get(username=user)
        searcher=Searcher.objects.get(user=user)
        pages=[]
        for f in searcher.folders.all():
            if f.name == folder.strip():
                # print f.pages.all()
                for p in f.pages.all():
                    # print p.serialise()
                    pages.append(p.serialise())
                    print "pages sources",p.source
        # print "pages", json.dumps(pages[0])
        return JsonResponse({"folder":folder,"pages":pages})
        # return JsonResponse({"folder":folder,"pages":[]})




