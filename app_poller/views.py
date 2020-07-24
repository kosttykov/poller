import json

from django.contrib.auth.forms import AuthenticationForm
from django.contrib import auth
from django.contrib.auth import login, authenticate

# from django.views.generic import FormView
from django.template import loader, RequestContext
from django.shortcuts import render, redirect
from django.http import Http404  

from app_poller.forms import SignUpForm
from app_poller.models import User, Question, Poll


# Create your views here.


def home(request):
    if request.user.is_authenticated:
        return redirect('app_poller:dashboard')
    else:
        return render(request, 'home.html')


def dashboard(request):
    if request.user.is_authenticated:
        context = {}
        context['username'] = request.user.username
        return render(request, 'dashboard/dashboard.html', context)
    else:
        return redirect('app_poller:home')


def dashboard_profile(request):
    if request.user.is_authenticated:
        context = {}
        getUser = request.user
        context['username'] = getUser.username
        context['id'] = getUser.id
        context['date_joined'] = getUser.date_joined
        context['email'] = getUser.email
        return render(request, 'dashboard/profile.html', context)
    else:
        return redirect('app_poller:home')


def dashboard_questions(request):
    if request.user.is_authenticated:
        context = {}
        context['username'] = request.user.username
        context['questions'] = Question.getAllQuestions()
        return render(request, 'dashboard/questions.html', context)
    else:
        return redirect('app_poller:home')


def dashboard_questions_create(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            Question.createQusetion(request)
            return redirect('app_poller:dashboard_questions')
        else:
            context = {}
            context['username'] = request.user.username
            return render(request, 'dashboard/questions_create.html', context)
    else:
        return redirect('app_poller:home')


def dashboard_questions_delete(request, id):
    if request.user.is_authenticated:
            Question.deleteQuestion(id)
            return redirect('app_poller:dashboard_questions')
    else:
        return redirect('app_poller:home')


def dashboard_questions_edit(request, id):
    context = {}
    if request.user.is_authenticated:
        if request.method == 'POST':
            Question.editQuestion(request, id)
            return redirect('app_poller:dashboard_questions')
        else:
            question = Question.getEditQuestion(id)
            if question == None:
                raise Http404
            else:
                context['questions'] = question
                return render(request, 'dashboard/questions_edit.html', context)
    else:
        return redirect('app_poller:home')


def dashboard_polls(request):
    if request.user.is_authenticated:
        context = {}
        context['username'] = request.user.username
        context['polls'] = Poll.getAllPolls()
        return render(request, 'dashboard/polls.html', context)
    else:
        return redirect('app_poller:home')


def dashboard_polls_create(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            Poll.createPoll(request)
            return redirect('app_poller:dashboard_polls')
        else:
            context = {}
            context['username'] = request.user.username
            context['questions'] = Question.getAllQuestions()
            return render(request, 'dashboard/polls_create.html', context)
    else:
        return redirect('app_poller:home')


def signin(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            auth.login(request, form.get_user())
            return redirect('app_poller:dashboard')
        else:
            context = {'form': AuthenticationForm()}  
            return render(request, 'signin.html', context)
    elif request.user.is_authenticated:
            return redirect('app_poller:dashboard')
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
            return redirect('app_poller:dashboard')
    elif request.user.is_authenticated:
        return redirect('app_poller:dashboard')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


def reset_password(request):
    return render(request, 'reset_password.html')


def logout(request):  
    auth.logout(request)  
    return redirect('app_poller:home')


def handler404(request, *args, **argv):
    response = render_to_response('404.html', {}, context_instance=RequestContext(request))
    response.status_code = 404
    return response


def handler500(request, *args, **argv):
    response = render_to_response('500.html', {}, context_instance=RequestContext(request))
    response.status_code = 500
    return response
