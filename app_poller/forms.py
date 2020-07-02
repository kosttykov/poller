from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from app_poller.models import Question


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)
    email = forms.EmailField(max_length=254)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'first_name', 'last_name')

class Question():
    title = forms.CharField(max_length=120)
    text = forms.CharField()
    text2 = forms.CharField()
    text3 = forms.CharField(required=False)
    text4 = forms.CharField(required=False)
    text5 = forms.CharField(required=False)
    text6 = forms.CharField(required=False)
    text7 = forms.CharField(required=False)
    text8 = forms.CharField(required=False)
    text9 = forms.CharField(required=False)
    text10 = forms.CharField(required=False)
    owned = forms.CharField()

    class Meta:
        model = Question
        fields = ('title', 'text', 'owned')