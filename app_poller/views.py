import json

from django.contrib.auth.forms import AuthenticationForm
from django.contrib import auth
from django.contrib.auth import login, authenticate

# from django.views.generic import FormView
from django.template import loader, RequestContext
from django.shortcuts import render, redirect
from django.http import Http404  

from app_poller.forms import SignUpForm
from app_poller.models import Question, User


# Create your views here.


def home(request):
    if request.user.is_authenticated:
        return redirect('app_poller:dashboard')
    else:
        return render(request, 'home.html')


def dashboard(request):
    context = {}
    if request.user.is_authenticated:
        context['username'] = request.user.username
        return render(request, 'dashboard/dashboard.html', context)
    else:
        return redirect('app_poller:home')


def dashboard_profile(request):
    context = {}
    if request.user.is_authenticated:
        context['username'] = request.user.username
        context['id'] = request.user.id
        context['date_joined'] = request.user.date_joined
        context['email'] = request.user.email
        return render(request, 'dashboard/profile.html', context)
    else:
        return redirect('app_poller:home')


def dashboard_questions(request):
    context = {}
    if request.user.is_authenticated:
        context['username'] = request.user.username
        questions = Question.objects.all()
        for question in questions:
            question.body = json.loads(question.body)
        context['questions'] = questions
        return render(request, 'dashboard/questions.html', context)
    else:
        return redirect('app_poller:home')


def dashboard_questions_create(request):
    context = {}
    if request.user.is_authenticated:
        if request.method == 'POST':
            title = request.POST.get('title')
            owned = User.objects.get(username=request.user.username)
            option = list(filter(None, request.POST.getlist('option')))
            right_answer = request.POST.getlist('right')
            is_several = request.POST.get('is_several')
            body = {"option": option, "right_answer": right_answer, "is_several": is_several}
            Question.save_question(title, body, owned)
            return redirect('app_poller:dashboard_questions')

        else:   
            context['username'] = request.user.username
            questions = Question.objects.all()
            context['questions'] = questions
            return render(request, 'dashboard/questions_create.html', context)
    else:
        return redirect('app_poller:home')


def dashboard_questions_delete(request, id):
    if request.user.is_authenticated:
        if Question.objects.filter(id=id).exists():
            Question.delete_question(id)
            return redirect('app_poller:dashboard_questions')
        else:
            raise Http404
    else:
        return redirect('app_poller:home')


def dashboard_questions_edit(request, id):
    context = {}
    if request.user.is_authenticated:
        if request.method == 'POST':
            title = request.POST.get('title')
            option = list(filter(None, request.POST.getlist('option')))
            right_answer = request.POST.getlist('right')
            is_several = request.POST.get('is_several')
            body = {"option": option, "right_answer": right_answer, "is_several": is_several}
            Question.edit_question(title, body, id)
            return redirect('app_poller:dashboard_questions')
        else:
            if Question.objects.filter(id=id).exists():
                question = Question.objects.get(id=id)
                question.body = json.loads(question.body)
                count_option = 10 - len(question.body["option"])
                for i in range(count_option):
                    question.body['option'].append('')
                context['questions'] = question
                return render(request, 'dashboard/questions_edit.html', context)
            else:
                raise Http404
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
