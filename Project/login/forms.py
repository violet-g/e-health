from django.forms import *

class LoginForm(Form):
    username = CharField(label='username')
    password = CharField(widget=PasswordInput(), label='password')

class RegisterForm(Form):
    username = CharField(label='username')
    password = CharField(widget=PasswordInput(), label='password')
    repeat_password = CharField(widget=PasswordInput(), label='repeat password')
    email = EmailField(label='e-mail')
    first_name = CharField(label='first name')
    last_name = CharField(label='last name')
