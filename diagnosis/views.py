from django.shortcuts import render, redirect
from questions.models import Question,QuestionCategory
import pandas as pd
from diagnosis.forms import DynamicForm
from django.views.decorators.csrf import csrf_exempt
from diagnosis.models import Diagnosis, Answers
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.
def diagnosis(request):
    return render(request, 'diagnosis.html', {})

@login_required()
@csrf_exempt
def diagnose(request):
    """Diagnose view: If the request method is post it save the diagnosis form otherwise show the form to the user

    Args:
        request (http request): _description_

    Returns:
        _type_: The diagnosis view to answer the form or redirects to dashboard if post method
    """    
    if request.method=='POST':
        #Get total Score from answers
        score = 0
        for k in request.POST:
            if(k.isnumeric()):
                q = Question.objects.get(pk = int(k))
                score += q.score_yes if request.POST[k] == '1' else q.score_no

        #Save the diagnosis score
        diagnosis = Diagnosis(user = request.user, score =score)
        diagnosis.save()
        for k in request.POST:
            #Save every answer to the questions
            if(k.isnumeric()):
                q = Question.objects.get(pk = int(k))
                bool_val = request.POST[k] == '0'
                answer = Answers(question = q, answer = bool_val, diagnosis = diagnosis)
                answer.save()
        messages.success(request, 'Your energy consumption has been saved successfully')
        return redirect(to='/dashboard')
 
    questions = Question.objects.all().select_related().order_by("category_id")
    
    context = {
        'questions' : questions,
    }
    return render(request, 'make_diagnosis.html', context)

def save(request):
    if request.method=='POST':
        #for k in request.post
        #form = DynamicForm(request.post)
        for k in request.POST:
            print(f"{k} is {k.value}")
        return render(request, 'result_diagnosis.html', {})
    context = {

    }
    return render(request, 'result_diagnosis.html', context)