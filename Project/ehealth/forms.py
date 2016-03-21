from django.forms import *
from ehealth.models import Searcher
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.hashers import *

class SearcherForm(ModelForm):
    forename = forms.CharField(max_length=128,help_text="Please enter your forename")
    surname = forms.CharField(max_length=128,help_text="Please enter your surname")
    email = forms.EmailField(max_length=128,help_text="Please enter your e-mail address")
    username = forms.CharField(max_length=128,help_text="Please enter your desired username")
    password = forms.CharField(max_length=128,help_text="Please enter your desired password",widget=PasswordInput())
    picture = forms.ImageField(required=False)
    website = forms.URLField(max_length=128,help_text="Please enter your website",required=False)

    class Meta:
        model = Searcher
        fields=("picture",)


class LoginForm(forms.Form):
    username = forms.CharField(label='username')
    password = forms.CharField(widget=PasswordInput(), label='password')
    form_type = forms.CharField(widget=HiddenInput(), initial='login')

    def clean(self):
        username = self.cleaned_data.get('username')
        try:
            user = User.objects.get(username=username)
            goodUser = True
        except:
            goodUser = False
        if goodUser == False:
            raise forms.ValidationError('Username doesn\'t exist', code='not_exist')
        password = self.cleaned_data.get('password')
        if check_password(password,user.password) == False: #password != user.password:
            raise forms.ValidationError('Wrong password', code='wrong_password')
        return self.cleaned_data


class RegisterForm(forms.ModelForm):
    username = forms.CharField(label='username')
    password = forms.CharField(widget=PasswordInput(), label='password')
    repeat_password = forms.CharField(widget=PasswordInput(), label='repeat password')
    email = forms.EmailField(label='e-mail')
    first_name = forms.CharField(label='first name')
    last_name = forms.CharField(label='last name')
    form_type = forms.CharField(widget=HiddenInput(), initial='register')
    picture = forms.ImageField(required=False)

    def clean(self):
        password1 = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('repeat_password')
        if password1 != password2:
            raise forms.ValidationError('Passwords don\'t match.', code='not_match')
        try:
            userExists = User.objects.get(username=self.cleaned_data.get("username"))
        except:
            userExists = None
        if userExists:
            raise forms.ValidationError("Username is already in use")
        try:
            emailTaken = User.objects.get(email = self.cleaned_data.get("email"))
            emailTaken = True
        except:
            emailTaken = False
        if emailTaken == True:
            raise forms.ValidationError("Email is already in use.")
        return self.cleaned_data

    class Meta:
        model = Searcher
        fields = ['username', 'password', 'repeat_password', 'email']



#rework
class ChangeDetailsForm(forms.Form):
    password = forms.CharField(widget=PasswordInput(),label="Change password",help_text="Please enter your new password",required=False)
    password_retype = forms.CharField(widget=PasswordInput(),label="Change password",help_text="Please re-enter your new password",required=False)
    email = forms.EmailField(label='e-mail',required=False,help_text="Please enter your new e-mail")
    first_name = forms.CharField(label='first name',required=False,help_text="Please enter your updated forename")
    last_name = forms.CharField(label='last name',required=False,help_text="Please enter your updated sirname")

#    def clean(self):
#        try:
#            emailTaken = User.objects.get(email=self.cleaned_data.get("email"))
#        except:
#            emailTaken = None
#        if emailTaken:
#            raise forms.ValidationError("email is already in use")


#        if self.cleaned_data.get("password"):
#            if self.cleaned_data.get("password") != self.cleaned_data.get("password_retype"):
#                raise forms.ValidationError("Passwords don't match", code='not_match')
#            try:
#                pass
#            except:
#                raise forms.ValidationError("Please enter password in both fields")

#       return self.cleaned_data




        #password = self.cleaned_data.get('password')
        #if check_password(password,user.password) == False: #password != user.password:
        #    raise forms.ValidationError('Wrong password', code='wrong_password')