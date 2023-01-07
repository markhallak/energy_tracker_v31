from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from diagnosis.models import Diagnosis
from django.db.models import Max
from django.utils.timezone import now
from datetime import datetime, timedelta
import pandas as pd
import json
from django.db.models import DateField, Sum, Count,IntegerField,CharField,Subquery,OuterRef
from django.db.models.functions import Cast
from users.models import User


@login_required()
def index(request):
    #last_date = Diagnosis.objects.filter(user_id = request.user.id).aggregate(Max('date'))['date__max']
    #last_date.values_list('date', flat=True)
    try:
        last_diagnosis = Diagnosis.objects.filter(user_id=request.user.id).latest('date')
    except:
       last_diagnosis = None

    #Data for historic graph: last data from x days
    date_range = [now() - timedelta(days=30), now()]
    try:
        data = Diagnosis.objects.filter(user_id = request.user.id, date__range = date_range).values()
        dataDF = pd.DataFrame(list(data))
        date_values = dataDF['date'].dt.strftime("%Y-%M-%D%HH%ii%ss.000Z").astype("string").to_list()
        score_values = dataDF['score'].to_list()
    except :
        data = None
        date_values = None
        score_values= None
    
    

    #Data for leaderboard
    #leaderboard = Diagnosis.objects.filter(date__range = now()).values()
    try:
        last = Diagnosis.objects.filter(user_id=request.user.id).latest('date')
        last_score = last.score
    except:
        last= None
        last_score = None
    #Last diagnosis per user
    try:
        q_leaderboards = Diagnosis.objects.raw('''Select d.id, d.user_id, u.name as username, score from diagnosis_diagnosis d join(
                                    SELECT id,user_id,  
                                    MAX("diagnosis_diagnosis"."date") AS "max_date" 
                                    FROM "diagnosis_diagnosis" GROUP BY "diagnosis_diagnosis"."user_id") latest_d 
                                    on d.id =latest_d.id 
                                    join users_user u on u.id=d.user_id
                                    order by score desc''')           
    except:
        q_leaderboards =None
    leaders_list =[]
    
    for a in Diagnosis.objects.raw('''Select d.id as id, d.user_id as user_id,u.name as username, score as score from diagnosis_diagnosis d join(
                                    SELECT id,user_id,  
                                    MAX("diagnosis_diagnosis"."date") AS "max_date" 
                                    FROM "diagnosis_diagnosis" GROUP BY "diagnosis_diagnosis"."user_id") latest_d on d.id =latest_d.id 
                                    join users_user u on u.id=d.user_id
                                    order by score desc'''):
        leaders_list.append(a)
    
    # Max date per user 
    query2 = Diagnosis.objects.annotate(
                    user_t=Cast('user', CharField())
                ).values('user_t').annotate(
                    max_date=Max('date')
                ).order_by('user')
    context = {
        'actual_index': last_diagnosis,
        'date_range': date_range,
        'data': data,
        'date_values': date_values,
        'score_values': score_values,
        'last':last_score,
        'users_list': leaders_list,
        's': q_leaderboards
    }
    return render(request, 'dashboard.html', context)
