from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=256)


class User(models.Model):
    username = models.CharField(max_length = 20, unique='true')
    password = models.CharField(max_length = 20)
    first_name = models.CharField(max_length = 30)
    last_name = models.CharField(max_length = 30)
    email = models.EmailField(max_length = 50)



class Page(models.Model):
    title = models.CharField(max_length=128)
    source = models.CharField(max_length=128)
    summary = models.TextField()
    url = models.URLField()
    readability_score = models.IntegerField()
    sentiment_score = models.IntegerField()
    subjectivity_score = models.IntegerField()
    times_saved = models.BigIntegerField()
    category = models.ManyToManyField(Category)
   #WHAT ELSE DO WE NEED

    def __unicode__(self):
        return self.title


class Query(models.Model):
    content = models.TextField()
    category = models.ManyToManyField(Category)

class Searcher(models.Model):
    user = models.OneToOneField(User)
    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)
    history = models.ManyToManyField(Query)
    #WHAT ELSE DO WE NEED

    def __unicode__(self):
        return self.user.username


class Folder(models.Model):
        User = models.ForeignKey(Searcher)
        name = models.CharField(max_length=128, unique=True)
        pages = models.ManyToManyField(Page)
        public = models.BooleanField()
        #WHAT ELSE DO WE NEED

        def __unicode__(self):
               return self.name

class UserHistory(models.Model):
    user = models.ForeignKey(Searcher,on_delete=models.CASCADE)
    query = models.ForeignKey(Query,on_delete=models.CASCADE)
    # timestamp = models.DateTimeField(auto_now=True,auto_now_add=True)
    timestamp = models.DateTimeField(auto_now=True)

class FolderPage(models.Model):
    folder = models.ForeignKey(Folder,on_delete=models.CASCADE)
    page = models.ForeignKey(Page,on_delete=models.CASCADE)
    #WHAT ELSE DO WE NEED TO KNOW

class PageCategory(models.Model):
    page = models.ForeignKey(Page,on_delete=models.CASCADE)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)

class QueryCategory(models.Model):
    query = models.ForeignKey(Query,on_delete=models.CASCADE)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
