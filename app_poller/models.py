import json
import datetime
import time

from django.contrib.postgres.fields import JSONField
from django.db import models
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import Http404  


# Create your models here.


class Question(models.Model):
    title = models.CharField(max_length=130)
    body = JSONField()
    image = models.ImageField(upload_to='db_images/', default=None, blank=True)
    owned = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def getAllQuestions():
        questions = Question.objects.all()
        for question in questions:
            question.body = json.loads(question.body)
        return questions

    
    def createQusetion(request):
        title = request.POST.get('title')
        owned = User.objects.get(id=request.user.id)
        image = request.FILES.get('image')
        option = list(filter(None, request.POST.getlist('option')))
        right_answer = []
        ra = request.POST.getlist('right')
        for x in ra:
            right_answer.append(int(x))
        is_several = request.POST.get('is_several')
        body = {"option": option, "right_answer": right_answer, "is_several": is_several}
        Question(title=title, body=json.dumps(body), image=image, owned=owned).save()


    def deleteQuestion(id):
        Question.objects.filter(id=id).delete()


    def editQuestion(request, id):
        title = request.POST.get('title')
        image = request.FILES.get('image')
        option = list(filter(None, request.POST.getlist('option')))
        right_answer = []
        ra = request.POST.getlist('right')
        for x in ra:
            right_answer.append(int(x))
        is_several = request.POST.get('is_several')
        body = {"option": option, "right_answer": right_answer, "is_several": is_several}
        model = Question.objects.get(id=id)
        model.title = title
        if image != None:
            model.image = image
        model.body = json.dumps(body)
        model.save()


    def getEditQuestion(id):
        question = Question.objects.filter(id=id).first()
        if question == None:
            return None
        else:
            question.body = json.loads(question.body)
            count_option = 10 - len(question.body["option"])
            for i in range(count_option):
                question.body['option'].append('')
            return question


class Poll(models.Model):
    title = models.CharField(max_length=130)
    questions = models.ManyToManyField(Question)
    owned = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    publishing_time = models.DateField(default=None, null=True, blank=True)
    finishing_time = models.DateField(default=None, null=True, blank=True)
    time_to_answer = models.IntegerField(default=None, null=True, blank=True)
    points = JSONField()

    def __str__(self):
        return self.title

    def getAllPolls():
        polls = Poll.objects.all()
        return polls


    def getPollById(id):
        poll = Poll.objects.filter(id=id).first()
        if poll == None:
            return None
        questions = poll.questions.all()
        for question in questions:
            question.body = json.loads(question.body)
        return poll, questions

    
    def createPoll(request):
        title = request.POST.get('title')
        questions = request.POST.getlist('questions')
        points = {}
        for item in questions:
            point = request.POST.get(item)
            points.update({int(item):int(point)})
        owned = User.objects.get(id=request.user.id)
        publishing_time = request.POST.get('publishing_time')
        finishing_time = request.POST.get('finishing_time')  
        time = request.POST.get('time_to_answer').split(":")
        h = int(time[0]) * 3600
        m = int(time[1]) * 60
        time_to_answer = h+m
        poll = Poll(title=title, owned=owned, publishing_time=publishing_time, finishing_time=finishing_time, time_to_answer=time_to_answer, points=points)
        poll.save()
        for question in questions:
            poll.questions.add(question)


    def deletePoll(id):
        Poll.objects.filter(id=id).delete()

    
    def editPoll(request, id):
        poll = Poll.objects.get(id=id)
        poll.title = request.POST.get('title')
        poll.publishing_time = request.POST.get('publishing_time')
        poll.finishing_time = request.POST.get('finishing_time')
        tta = request.POST.get('time_to_answer')
        ta = tta.split(":")
        h = int(ta[0]) * 3600
        m = int(ta[1]) * 60
        poll.time_to_answer = h+m
        questions = request.POST.getlist('questions')
        points = {}
        for item in questions:
            point = request.POST.get(item)
            points.update({int(item):int(point)})
        poll.points = points
        poll.save()
        poll.questions.set(questions)


    def getEditPoll(id):
        poll = Poll.objects.filter(id=id).first()
        return poll


class Answer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    body = JSONField()
    total_score = models.IntegerField(default=0)
    max_score = models.IntegerField(default=0)
    percent = models.IntegerField(default=0)
    
    
    def saveAnswer(request, id):
        questions = Poll.getPollById(id)
        questions_id = [str(question.id) for question in questions[1]]
        points = questions[0].points
        values = points.values()
        answer_list = []
        total_score = 0
        max_score = 0

        for n in questions_id:
            a = request.POST.getlist(n)
            for i in a:
                answer_list.append([int(s) for s in i.split() if s.isdigit()])

        for question in questions[1]:
            for item in answer_list:
                if item[0] == question.id:
                    if question.body.get('right_answer') != []:
                        if item[1] in question.body.get('right_answer'):
                            x = points.get(str(question.id))
                            total_score += x
                            break
                    else:
                        x = points.get(str(question.id))
                        total_score += x
                        break

        for value in values:
            max_score += value

        percent = round((total_score / max_score) * 100)

        user = User.objects.get(id=request.user.id)
        poll = Poll.objects.get(id=id)
        Answer(user=user, poll=poll, body=json.dumps(answer_list), total_score=total_score, max_score=max_score, percent=percent).save()

    def userCorrectAnswers(request):
        answers = Answer.objects.filter(user=request.user.id)
        max_points = 0
        points = 0
        for answer in answers:
            max_points += answer.max_score
            points += answer.total_score

        if max_points == 0:
            percent = 0
        else:
            percent = round((points / max_points) * 100)

        data = {"percent": percent, "max_score": max_points, "your_score": points}
        return data


    def correctAnswers(request):
        answers = Answer.objects.all()
        max_points = 0
        points = 0
        for answer in answers:
            max_points += answer.max_score
            points += answer.total_score

        if max_points == 0:
            return 0

        data = round((points / max_points) * 100)
        return data


    def getAllAnswers():
        answers = Answer.objects.all()
        return answers

    
    def getByPoll(id):
        answers = Answer.objects.filter(poll=id)
        return answers


    def getUserAnswer(id, userid):
        answer = Answer.objects.filter(user=userid, poll=id).first()
        if answer == None:
                raise Http404
        answer.body = json.loads(answer.body)
        return answer


    def getExistAnswer(request):
        EA = Answer.objects.filter(user=request.user.id)
        ids = []
        for item in EA:
            ids.append(item.poll.id)
        return ids

class editUser():


    def dashboard(request):
        user = User.objects.get(id=request.user.id)
        polls = Poll.objects.count()
        questions = Question.objects.count()
        answers = Answer.objects.count()
        user_answers = Answer.objects.filter(user=request.user.id).count()
        users = User.objects.count()

        max_setup = 5
        setup = 0
        if user.username != "":
            setup += 1
        if user.is_active:
            setup += 1
        if user.email != "":
            setup += 1
        if user.first_name != "":
            setup += 1
        if user.last_name != "":
            setup += 1
        profile_setup = round((setup / max_setup) * 100)


        data = {"polls": polls, "questions": questions, "answers": answers, "user_answers": user_answers, "profile_setup": profile_setup, "users": users}
        return data


    def adminEditUser(request, id):
        user = User.objects.get(id=id)
        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        chekboxes = request.POST.getlist('checkbox')
        is_active = False
        is_staff = False
        is_superuser = False

        user.username = username
        user.email = email
        user.first_name = first_name
        user.last_name = last_name

        if 'is_active' in chekboxes:
            is_active = True
        if 'is_staff' in chekboxes:
            is_staff = True
        if 'is_superuser' in chekboxes:
            is_superuser = True
        
        user.is_active = is_active
        user.is_staff = is_staff
        user.is_superuser = is_superuser
        user.save()


    def profileSetup(request):
        user = User.objects.get(id=request.user.id)
        max_setup = 5
        setup = 0
        if user.username != "":
            setup += 1
        if user.is_active:
            setup += 1
        if user.email != "":
            setup += 1
        if user.first_name != "":
            setup += 1
        if user.last_name != "":
            setup += 1
        profile_setup = round((setup / max_setup) * 100)
        return data


    def getUser(id):
        user = User.objects.filter(id=id).first()
        
        if user == None:
            raise Http404

        return user


    def createUser(request):
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password1')
        if len(password) < 4:
            return messages.error(request, "Password is not correct")
        elif User.objects.filter(username=username).exists():
            return messages.error(request, "Username is busy. Try another")
        else:
            User.objects.create_user(username, email, password).save()


    def editUsername(request):
        if User.objects.filter(username=request.POST.get('username')).exists():
            return messages.error(request, "Username is busy. Try another")
        else:
            request.user.username = request.POST.get('username')
            request.user.save()


    def editProfile(request):
        request.user.first_name = request.POST.get('first_name')
        request.user.last_name = request.POST.get('last_name')
        request.user.save()


    def editEmail(request):
        request.user.email = request.POST.get('new_email')
        request.user.save()
        

    def editPassword(request):
        request.user.set_password(request.POST.get('password'))
        request.user.save()


    def resetPassword(request):
        username = request.POST.get('username')