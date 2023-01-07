from django.shortcuts import render
from questions.models import Question,QuestionCategory
import pandas as pd
from diagnosis.forms import DynamicForm
from django.views.decorators.csrf import csrf_exempt
from diagnosis.models import Diagnosis, Answers

# Create your views here.
def diagnosis(request):
    return render(request, 'diagnosis.html', {})

@csrf_exempt
def diagnose(request):
    if request.method=='POST':
        #Get total Score from answers
        score = 0
        for k in request.POST:
            if(k.isnumeric()):
                q = Question.objects.get(pk = int(k))
                bool_val = False if request.POST[k] == '0' else True
                score += q.score_no if bool_val else q.score_yes
        #Save the diagnosis score
        diagnosis = Diagnosis(user = request.user, score =score)
        diagnosis.save()
        for k in request.POST:
            #Save every answer to the questions
            if(k.isnumeric()):
                q = Question.objects.get(pk = int(k))
                bool_val = False if request.POST[k] == '0' else True
                answer = Answers(question = q, answer = bool_val, diagnosis = diagnosis)
                answer.save()
 
    questions = Question.objects.all()
    #qDf = pd.DataFrame(questions)
    uniqueCategories= questions.values_list("category_id",flat=True).distinct()
    categories = QuestionCategory.objects.filter(id__in=uniqueCategories)
    
    #uniqueCategories = qDf.category.unique()
    context = {
        'questions' : questions,
        'cats': categories,
    }
    return render(request, 'make_diagnosis.html', context)

def save(request):
    if request.method=='POST':
        #for k in request.post
        #form = DynamicForm(request.post)
        for k in request.POST:
            print(f"{k} is {k.value}")
        return render(request, 'result_diagnosis.html', context)
    context = {

    }
    return render(request, 'result_diagnosis.html', context)