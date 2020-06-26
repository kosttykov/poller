from django.contrib import admin
from app_poller.models import Question

# Register your models here.

@admin.register(Question)
class Question(admin.ModelAdmin):
    list_display=('title', 'owned', 'id')