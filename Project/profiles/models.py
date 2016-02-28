from django.db.models import *

class User(Model):
    username = CharField(max_length = 20, unique='true')
    password = CharField(max_length = 20)
    first_name = CharField(max_length = 30)
    last_name = CharField(max_length = 30)
    email = EmailField(max_length = 50)
