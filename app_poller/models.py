import json

from django.contrib.postgres.fields import JSONField
from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Question(models.Model):
    title = models.CharField(max_length=130)
    body = JSONField()
    owned = models.ForeignKey(User, on_delete=models.CASCADE)


    def save_question(title, body, owned):
        model = Question(title=title, body=json.dumps(body), owned=owned)
        model.save()


    def delete_question(id):
        model = Question.objects.get(id=id)
        model.delete()


    def edit_question(title, body, id):
        model = Question.objects.get(id=id)
        model.title = title
        model.body = json.dumps(body)
        model.save()
