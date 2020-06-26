from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import auth
from django.http.response import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import FormView
from django.contrib.auth.forms import UserCreationForm
from app_poller.forms import SignUpForm
from app_poller.models import Question
from django.contrib.auth import login, authenticate

# Create your views here.

def home(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse_lazy('app_poller:dashboard'))
    else:
        template = loader.get_template('home.html')
        return HttpResponse(template.render())

def dashboard(request):
    context = {}
    if request.user.is_authenticated:
        context['username'] = request.user.username
        return render(request, 'dashboard/dashboard.html', context)
    else:
        return HttpResponseRedirect(reverse_lazy('app_poller:home'))

def dashboard_profile(request):
    context = {}
    if request.user.is_authenticated:
        context['username'] = request.user.username
        context['id'] = request.user.id
        context['date_joined'] = request.user.date_joined
        context['email'] = request.user.email
        return render(request, 'dashboard/profile.html', context)
    else:
        return HttpResponseRedirect(reverse_lazy('app_poller:home'))

def dashboard_questions(request):
    context = {}
    if request.user.is_authenticated:
        context['username'] = request.user.username
        questions = Question.objects.all()
        context['questions'] = questions
        return render(request, 'dashboard/questions.html', context)
    else:
        return HttpResponseRedirect(reverse_lazy('app_poller:home'))

def dashboard_questions_create(request):
    context = {}
    if request.user.is_authenticated:
        context['username'] = request.user.username
        questions = Question.objects.all()
        context['questions'] = questions
        return render(request, 'dashboard/questions_create.html', context)
    else:
        return HttpResponseRedirect(reverse_lazy('app_poller:home'))

def signin(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            auth.login(request, form.get_user())
            return HttpResponseRedirect(reverse_lazy('app_poller:dashboard'))
        else:
            context = {'form': AuthenticationForm()}  
            return render(request, 'signin.html', context)
    elif request.user.is_authenticated:
            return HttpResponseRedirect(reverse_lazy('app_poller:dashboard'))
    else:  
        return render(request, 'signin.html')    



def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return HttpResponseRedirect(reverse_lazy('app_poller:dashboard'))
    elif request.user.is_authenticated:
        return HttpResponseRedirect(reverse_lazy('app_poller:dashboard'))
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def reset_password(request):
    template = loader.get_template('reset_password.html')
    return HttpResponse(template.render())

def logout(request):  
    auth.logout(request)  
    return HttpResponseRedirect(reverse_lazy('app_poller:home'))
