import time

from django.contrib.auth.forms import AuthenticationForm
from django.contrib import auth, messages
from django.contrib.auth import login, authenticate

# from django.views.generic import FormView
from django.template import loader, RequestContext
from django.shortcuts import render, redirect
from django.http import Http404  
from django.core.mail import send_mail

from app_poller.forms import SignUpForm
from app_poller.models import User, Question, Poll, Answer, editUser

from datetime import date


# Create your views here.

def home(request):
    if request.user.is_authenticated:
        return redirect('app_poller:dashboard')
    else:
        return render(request, 'home.html')


def dashboard(request):
    if request.user.is_authenticated:
        context = {}
        context['dashboard'] = editUser.dashboard(request)
        context['user_correct_answers'] = Answer.userCorrectAnswers(request)
        context['correct_answers'] = Answer.correctAnswers(request)
        return render(request, 'dashboard/dashboard.html', context)
    else:
        return redirect('app_poller:home')


def dashboard_profile(request):
    if request.user.is_authenticated:
        if 'editProfile' in request.POST:
            editUser.editProfile(request)
        elif 'editPassword' in request.POST:
            editUser.editPassword(request)
        elif 'editEmail' in request.POST:
            editUser.editEmail(request)
        elif 'editUsername' in request.POST:
            editUser.editUsername(request)
        return render(request, 'dashboard/profile.html')
    else:
        return redirect('app_poller:home')


def dashboard_questions(request):
    if request.user.is_staff:
        context = {}
        context['questions'] = Question.getAllQuestions()
        return render(request, 'dashboard/questions.html', context)
    else:
        return redirect('app_poller:dashboard')


def dashboard_questions_create(request):
    if request.user.is_staff:
        if request.method == 'POST':
            Question.createQusetion(request)
            return redirect('app_poller:dashboard_questions')
        else:
            return render(request, 'dashboard/questions_create.html')
    else:
        return redirect('app_poller:dashboard')


def dashboard_questions_delete(request, id):
    if request.user.is_staff:
        Question.deleteQuestion(id)
        return redirect('app_poller:dashboard_questions')
    else:
        return redirect('app_poller:dashboard')


def dashboard_questions_edit(request, id):
    if request.user.is_staff:
        context = {}
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
        return redirect('app_poller:dashboard')


def dashboard_polls(request):
    if request.user.is_staff:
        context = {}
        context['polls'] = Poll.getAllPolls()
        return render(request, 'dashboard/polls.html', context)
    else:
        return redirect('app_poller:dashboard')


def dashboard_polls_create(request):
    if request.user.is_staff:
        if request.method == 'POST':
            Poll.createPoll(request)
            return redirect('app_poller:dashboard_polls')
        else:
            context = {}
            context['questions'] = Question.getAllQuestions()
            return render(request, 'dashboard/polls_create.html', context)
    else:
        return redirect('app_poller:dashboard')


def dashboard_polls_delete(request, id):
    if request.user.is_staff:
        Poll.deletePoll(id)
        return redirect('app_poller:dashboard_polls')
    else:
        return redirect('app_poller:dashboard')


def dashboard_polls_edit(request, id):
    if request.user.is_staff:
        context = {}
        if request.method == 'POST':
            Poll.editPoll(request, id)
            return redirect('app_poller:dashboard_polls')
        else:
            poll = Poll.getEditPoll(id)
            if poll == None:
                raise Http404
            else:
                poll.time_to_answer = time.strftime('%H:%M', time.gmtime(poll.time_to_answer))
                context['poll'] = poll
                context['ids'] = [x.id for x in poll.questions.all()]
                context['questions'] = Question.getAllQuestions()
                return render(request, 'dashboard/polls_edit.html', context)
    else:
        return redirect('app_poller:dashboard')


def dashboard_tests(request):
    if request.user.is_staff:
        return redirect('app_poller:dashboard')
    elif request.user.is_authenticated:
        context = {}
        context['polls'] = Poll.getAllPolls()
        context['exists_answer'] = Answer.getExistAnswer(request)
        return render(request, 'dashboard/tests.html', context)
    else:
        return redirect('app_poller:home')


def dashboard_tests_take(request, id):
    if request.user.is_staff:
        return redirect('app_poller:dashboard')
    elif request.user.is_authenticated:
        if request.method == 'POST':
            Answer.saveAnswer(request, id)
            return redirect('app_poller:dashboard_tests')
        if Answer.objects.filter(poll=id, user=request.user.id).exists():
            raise Http404
        poll = Poll.getPollById(id)
        if poll == None:
            raise Http404
        now = date.today()
        pub = poll[0].publishing_time
        fin = poll[0].finishing_time
        if now < pub or now > fin:
            raise Http404
        context = {}
        context['poll'] = poll
        return render (request, 'dashboard/tests_take.html', context)
    else:
        return redirect('app_poller:home')


def dashboard_answers(request):
    if request.user.is_staff:
        context = {}
        context['polls'] = Poll.getAllPolls()
        return render(request, 'dashboard/answers.html', context)
    else:
        return redirect('app_poller:dashboard')


def dashboard_answers_id(request, id):
    if request.user.is_staff:
        context = {}
        answers = Answer.getByPoll(id)
        context['answers'] = answers
        if answers:
            all_total = 0
            all_max = 0
            for answer in answers:
                all_total += answer.total_score
                all_max += answer.max_score
            context['all_percent'] = round((all_total / all_max) * 100)
        return render(request, 'dashboard/answer_by_poll.html', context)
    else:
        return redirect('app_poller:dashboard')


def dashboard_answers_user(request, id, userid):
    if request.user.is_staff:
        context = {}
        answer = Answer.getUserAnswer(id, userid)
        context['answer'] = answer
        context['poll'] = Poll.getPollById(id)
        return render(request, 'dashboard/user_answer.html', context)
    else:
        return redirect('app_poller:dashboard')


def dashboard_users(request):
    if request.user.is_superuser:
        context = {}
        context['users'] = User.objects.all()
        return render(request, 'dashboard/users.html', context)
    else:
        return redirect('app_poller:dashboard')


def dashboard_users_edit(request, id):
    if request.user.is_superuser:
        if request.method == 'POST':
            editUser.adminEditUser(request, id)
            return redirect('app_poller:dashboard_users')
        else:
            context = {}
            context['user'] = editUser.getUser(id)
            return render(request, 'dashboard/users_edit.html', context)
    else:
        return redirect('app_poller:dashboard')


def signin(request):
    if request.user.is_authenticated:
        return redirect('app_poller:dashboard')
    else:
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('app_poller:dashboard')

        return render(request, 'signin.html')    


def signup(request):
    if request.user.is_authenticated:
        return redirect('app_poller:dashboard')
    else:
        if request.method == 'POST':
            editUser.createUser(request)
            login(request, authenticate(request, username=request.POST.get('username'), password=request.POST.get('password1')))
            return redirect('app_poller:dashboard')
        return render(request, 'signup.html')


def reset_password(request):
    if request.user.is_authenticated:
        return redirect('app_poller:dashboard')
    else:
        if request.method == 'POST':
            editUser.resetPassword(request)
        return render(request, 'reset_password.html')


def reset_password_link(request, link):
    a = link


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
