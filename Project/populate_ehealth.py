import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Project.settings')
import django
django.setup()
from ehealth.models import *

#zdravko is cool


def populate():

    user1 = add_searcher("boris","boris@test.com","boris","boris","lazarov")
    user2 = add_searcher("zdravko","zdravko@test.com","zdravko","zdravko","ivanov")

    cat1 = add_category("DE_ac")
    cat2 = add_category("it hurts")

    bFolder = add_folder(user1,"boris\'s folder","true")
    zFolder = add_folder(user2,"zdravko\'s folder","false")

    page1 = add_page("Facebook","Healthfinder","This is a test page","https://www.facebook.com",100,85,43,15)
    page2 = add_page("Google","Bing","This is also a test page","https://www.google.co.uk/",89,76,75,156)

    folderContent1 = add_pageFolder(page1,bFolder)
    folderContent2 = add_pageFolder(page2,bFolder)
    folderContent3 = add_pageFolder(page1,zFolder)

    pageCat = add_pageCategory(page1,cat1)
    pageCat2 = add_pageCategory(page1,cat2)
    pageCat3 = add_pageCategory(page2,cat1)


def add_page(title,source,summary,url,readability_score,sentiment_score,subjectivity_score,times_saved):
    newPage = Page(title=title,source=source,summary=summary,url=url,readability_score=readability_score,sentiment_score=sentiment_score,subjectivity_score=subjectivity_score,times_saved=times_saved)
    newPage.save()
    return newPage

def add_folder(user,name,public):
    newFolder = Folder(user=user,name=name,public=public)
    newFolder.save()
    return newFolder

def add_category(name):
    newCategory = Category(name=name)
    newCategory.save()
    return newCategory

def add_searcher(username,email,password,first_name,last_name):
        newuser = User.objects.create_user(username=username, email=email, password = password,first_name=first_name,last_name=last_name )
        newuser.save()
        newSearcher = Searcher(user = User.objects.get(username=username))
        newSearcher.save()
        return newSearcher

def add_pageFolder(page,folder):
    relationship = FolderPage(folder=folder,page=page)
    relationship.save()
    return relationship

def add_pageCategory(page,category):
    relationship = PageCategory(page=page,category=category)
    relationship.save()
    return relationship


# Start execution here!
if __name__ == '__main__':
    print "Starting Ehealth population script..."
    populate()
