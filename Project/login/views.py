from django.shortcuts import render
from .forms import LoginForm, RegisterForm
from django.http import HttpResponse
from profiles.models import User

def index(request):
    if request.method == 'POST':
        form_type = request.POST.get('form_type').encode('UTF-8')
        if form_type == 'register':
            login_form = LoginForm()
            register_form = RegisterForm(request.POST)
            if register_form.is_valid():
                register_form.save()
                return HttpResponse('successfully registered')
        elif form_type == 'login':
            login_form = LoginForm(request.POST)
            register_form = RegisterForm()
            if login_form.is_valid():
                return HttpResponse('successfully logged in')
        else:
            return HttpResponse('Unknown error occurred.')
    else:
        register_form = RegisterForm()
        login_form = LoginForm()

    return render(request, 'login/index.html',{
        'login_form': login_form,
        'register_form': register_form,
    })
