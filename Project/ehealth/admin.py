from django.contrib import admin
from ehealth.models import Searcher,Page,Folder,FolderPage

admin.site.register(Searcher)
admin.site.register(Page)
admin.site.register(Folder)
admin.site.register(FolderPage)

