import json

from django.contrib.postgres.fields import JSONField
from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Question(models.Model):
    title = models.CharField(max_length=130)
    body = JSONField()
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
        owned = User.objects.get(username=request.user.username)
        option = list(filter(None, request.POST.getlist('option')))
        right_answer = request.POST.getlist('right')
        is_several = request.POST.get('is_several')
        body = {"option": option, "right_answer": right_answer, "is_several": is_several}
        Question(title=title, body=json.dumps(body), owned=owned).save()


    def deleteQuestion(id):
        Question.objects.filter(id=id).delete()


    def editQuestion(request, id):
        title = request.POST.get('title')
        option = list(filter(None, request.POST.getlist('option')))
        right_answer = request.POST.getlist('right')
        is_several = request.POST.get('is_several')
        body = {"option": option, "right_answer": right_answer, "is_several": is_several}
        model = Question.objects.get(id=id)
        model.title = title
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


    def getAllPolls():
        polls = Poll.objects.all()
        return polls

    
    def createPoll(request):
        title = request.POST.get('title')
        questions = request.POST.getlist('questions')
        owned = User.objects.get(username=request.user.username)
        Poll(title=title, questions=questions.set(), owned=owned).save()