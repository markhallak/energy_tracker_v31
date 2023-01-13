import csv
import math
from datetime import timedelta

import numpy as np
import pandas as pd
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.timezone import now
from django.views.decorators.cache import cache_control
from sklearn.linear_model import LinearRegression
from worldwide_data import linearRegression as lrdata
from diagnosis.models import Diagnosis


@login_required()
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def index(request):
    """ 
    Main view of the dashboard app, it retrieves the data required for the actual score, historic graph, leaderboard

    Returns:
        django View: The django dashboard view
        
    """
     # Retrieve the data for historic graph: last data from x days
    date_range = [now() - timedelta(days=30), now()]
    try:
        data = Diagnosis.objects.filter(user_id=request.user.id, date__range=date_range).values()
        dataDF = pd.DataFrame(list(data))
        date_values = dataDF['date'].dt.strftime("%Y-%M-%D%HH%ii%ss.000Z").astype("string").to_list()
        score_values = dataDF['score'].to_list()
    except:
        data = None
        date_values = None
        score_values = None

    # Retrieve the Data for leaderboard function
    try:
        diffPercent = 0
        increaseOrDecrease = "Increase"
        last_diagnosis = Diagnosis.objects.filter(user_id=request.user.id).latest('date')
        oneBeforeLast = Diagnosis.objects.filter(user_id=request.user.id).order_by('-date')[1]
        if oneBeforeLast is not None:
            diffPercent = round(
                ((int(last_diagnosis.score) - int(oneBeforeLast.score)) / int(oneBeforeLast.score)) * 100, 2)
            if diffPercent < 0:
                increaseOrDecrease = "Decrease"
    except:
        last_diagnosis = None
        increaseOrDecrease = None
        diffPercent = None
     # Retrieve the last diagnosis value from the actual logged user
    try:
        last = Diagnosis.objects.filter(user_id=request.user.id).latest('date')
        last_score = last.score
    except:
        last = None
        last_score = None
    
    # Retrieve the data for leader boards Last diagnosis per user
    try:
        q_leaderboards = Diagnosis.objects.raw('''Select d.id, d.user_id, u.name as username, CAST(score as INT) AS score from diagnosis_diagnosis d join(
                                    SELECT id,user_id,  
                                    MAX("diagnosis_diagnosis"."date") AS "max_date" 
                                    FROM "diagnosis_diagnosis" GROUP BY "diagnosis_diagnosis"."user_id") latest_d 
                                    on d.id =latest_d.id 
                                    join users_user u on u.id=d.user_id
                                    order by score asc''')
    except:
        q_leaderboards = None

    # Get country consumption data from the linear regression
    countries = lrdata.getCountryData()
    country = str(request.user.country).lower()
    countryConsumption = round(countries[country], 2)
    # Set the status to show to the user
    status = "Keep working on improving your energy consumption"

    if last is not None and last.score <= 0.01:
        status = "Your energy consumption appears to be low"
    elif last is not None and last.score >= 20000:
        status = "Your energy consumption appears to be very high"
    elif last_score is None:
        status = "Your energy consumption cannot be assessed"

    context = {
        'actual_index': last_diagnosis,
        "diffPercent": math.fabs(diffPercent) if diffPercent else 0,
        'increaseOrDecrease': increaseOrDecrease,
        'date_range': date_range,
        'data': data,
        'date_values': date_values,
        'score_values': score_values,
        'last': last_score,
        's': q_leaderboards,
        'country': request.user.country,
        'countryConsumption': countryConsumption,
        'status': status,
    }
    return render(request, 'dashboard.html', context)
