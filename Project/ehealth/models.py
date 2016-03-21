from django.db import models
from django.contrib.auth.models import User


class Searcher(models.Model):
    user = models.OneToOneField(User)
    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)
    public = models.BooleanField(default=False)

    def __unicode__(self):
        return self.user.username

class Page(models.Model):
    title = models.CharField(max_length=128)
    source = models.CharField(max_length=128)
    summary = models.TextField()
    url = models.URLField()
    readability_score = models.FloatField(default=0)
    sentiment_score = models.FloatField(default=0)
    subjectivity_score = models.FloatField(default=0)
    times_saved = models.BigIntegerField(default=0)

    def serialise(self):
        data={"title": self.title,
            "source": self.source,
            "summary": self.summary,
            "url": self.url,
            "readability_score":self.readability_score,
            "sentiment_score":self.sentiment_score,
            "subjectivity_score":self.subjectivity_score,
            "times_saved":self.times_saved,
            }
        return data

    def __unicode__(self):
        return self.title

class Folder(models.Model):
        user = models.ForeignKey(Searcher, related_name="folders")
        name = models.CharField(max_length=128, unique=False)
        pages = models.ManyToManyField(Page,through='FolderPage',related_name="folders")
        public = models.BooleanField(default=False)
        #WHAT ELSE DO WE NEED

        def __unicode__(self):
               return self.name


class FolderPage(models.Model):
    folder = models.ForeignKey(Folder,on_delete=models.CASCADE)
    page = models.ForeignKey(Page,on_delete=models.CASCADE)
    #WHAT ELSE DO WE NEED TO KNOW

    def __unicode__(self):
        return self.page.__unicode__()
