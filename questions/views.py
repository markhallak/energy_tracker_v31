from django.shortcuts import render
from questions.models import Question

# Create your views here.
def index(request):
    questions = Question.objects.all()
    context = {
        'questions' : questions
    }
    return render(request, 'index.html', context)
def details(request, id):
    question = Question.objects.get(pk = id)
    context = {
        'question' : question
    }
    return render(request, 'detail.html', context)
