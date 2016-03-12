from django.forms import *
from ehealth.models import Searcher, User

class SearcherForm(ModelForm):
    forename = CharField(max_length=128,help_text="Please enter your forename")
    surname = CharField(max_length=128,help_text="Please enter your surname")
    email = EmailField(max_length=128,help_text="Please enter your e-mail address")
    username = CharField(max_length=128,help_text="Please enter your desired username")
    password = CharField(max_length=128,help_text="Please enter your desired password",widget=PasswordInput())
    picture = ImageField(required=False)
    website = URLField(max_length=128,help_text="Please enter your website",required=False)

    class Meta:
        model = Searcher
        fields=("picture",)

class LoginForm(Form):
    username = CharField(label='username')
    password = CharField(widget=PasswordInput(), label='password')
    form_type = CharField(widget=HiddenInput(), initial='login')

    def clean(self):
        username = self.cleaned_data.get('username')
        try:
            user = User.objects.get(username=username)
        except:
            raise forms.ValidationError('Username doesn\'t exist', code='not_exist')

        password = self.cleaned_data.get('password')
        if password != user.password:
            raise forms.ValidationError('Wrong password', code='wrong_password')
        return self.cleaned_data


class RegisterForm(ModelForm):
    username = CharField(label='username')
    password = CharField(widget=PasswordInput(), label='password')
    repeat_password = CharField(widget=PasswordInput(), label='repeat password')
    email = EmailField(label='e-mail')
    first_name = CharField(label='first name')
    last_name = CharField(label='last name')
    form_type = CharField(widget=HiddenInput(), initial='register')

    def clean(self):
        password1 = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('repeat_password')
        if password1 != password2:
            raise forms.ValidationError('Passwords don\'t match.', code='not_match')
        return self.cleaned_data

    class Meta:
        model = User
        fields = ['username', 'password', 'first_name', 'last_name', 'email']
