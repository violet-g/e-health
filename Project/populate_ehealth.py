import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Project.settings')
import django
django.setup()
from ehealth.models import *



def populate():

    python_cat = add_cat(name='Python',views=128,likes=64)

    add_page(cat=python_cat,
        title="Official Python Tutorial",
        
        url="http://docs.python.org/2/tutorial/")

    add_page(cat=python_cat,
        title="How to Think like a Computer Scientist",
        url="http://www.greenteapress.com/thinkpython/")

    add_page(cat=python_cat,
        title="Learn Python in 10 Minutes",
        url="http://www.korokithakis.net/tutorials/python/")

    django_cat = add_cat("Django",views=64,likes=32)

    add_page(cat=django_cat,
        title="Official Django Tutorial",
        url="https://docs.djangoproject.com/en/1.5/intro/tutorial01/")

    add_page(cat=django_cat,
        title="Django Rocks",
        url="http://www.djangorocks.com/")

    add_page(cat=django_cat,
        title="How to Tango with Django",
        url="http://www.tangowithdjango.com/")

    frame_cat = add_cat("Other Frameworks",views=32,likes=16)

    add_page(cat=frame_cat,
        title="Bottle",
        url="http://bottlepy.org/docs/dev/")

    add_page(cat=frame_cat,
        title="Flask",
        url="http://flask.pocoo.org")

    # Print out what we have added to the user.
    for c in Category.objects.all():
        for p in Page.objects.filter(category=c):
            print "- {0} - {1}".format(str(c), str(p))





def add_page(cat, title, url, views=0):
    p = Page.objects.get_or_create(category=cat, title=title)[0]
    p.url=url
    p.views=views
    p.save()
    return p




class Folder(models.Model):
        user = models.ForeignKey(Searcher, related_name="folders")
        name = models.CharField(max_length=128, unique=True)
        pages = models.ManyToManyField(Page,blank=True)
        public = models.BooleanField(default=False)



def add_folder(user,name,pages,public):


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

# Start execution here!
if __name__ == '__main__':
    print "Starting Rango population script..."
    populate()
