from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import JsonResponse
from . import linearRegression
from django.conf import settings
from users.models import Country
import operator
from diagnosis.models import Diagnosis

@login_required()
def index(request):
    """The main view from the worlwide data application

    Args:
        request (httprequest): The http request

    Returns:
        _type_: _description_
    """   
    key = settings.GOOGLE_API_KEY
    countries = linearRegression.getCountryData()
    context = {
        'countries': countries,
        'key':key,
    }
    return render(request, 'worldwide_data.html', context)

def mydata(request):
    """Function to send the data to plot in the google maps view

    Args:
        request (httprequest): The http request

    Returns:
        JsonResponse: A Json object as a response to the server request
    """    
    countries = linearRegression.getCountryData()
    result_list = []
    max_cons = max(countries.items(),key=operator.itemgetter(1))[1]
    try:
        last = Diagnosis.objects.filter(user_id=request.user.id).latest('date')
        last_score = last.score
    except:
        last = None
        last_score = None
    for country, energy in countries.items():
        countryObj = Country.objects.filter(name__icontains=country).first()
        result_list.append({
            "name": country,
            "latitude":countryObj.lat if hasattr(countryObj, "lat") else 0,
            "longitude":countryObj.long if hasattr(countryObj, "long") else 0,
            "score": '{:,.1f}'.format(energy) ,
            "scale": float(energy)/float(max_cons)
        })
    context ={
        "result_list": result_list,
        "user": last_score
    }
 
    return JsonResponse(context, safe=False)
