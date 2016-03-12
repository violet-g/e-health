from django import forms
from ehealth.models import Searcher

class SearcherForm(forms.ModelForm):
    forename = forms.CharField(max_length=128,help_text="Please enter your forename")
    surname = forms.CharField(max_length=128,help_text="Please enter your surname")
    email = forms.EmailField(max_length=128,help_text="Please enter your e-mail address")
    username = forms.CharField(max_length=128,help_text="Please enter your desired username")
    password = forms.CharField(max_length=128,help_text="Please enter your desired password",widget=forms.PasswordInput())
    picture = forms.ImageField(required=False)
    website = forms.URLField(max_length=128,help_text="Please enter your website",required=False)

    class Meta:
        model = Searcher
        fields=("picture",)