from django.contrib import admin
from app_poller.models import Question, Poll

# Register your models here.

@admin.register(Question)
class Question(admin.ModelAdmin):
    list_display=('title', 'owned', 'id')


@admin.register(Poll)
class Poll(admin.ModelAdmin):
    list_display=('title', 'id')