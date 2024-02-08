from django.shortcuts import render
from django.http import HttpResponse
import random
import json

import requests

from .models import Stock


def home(request):
    # get last 32 stock data
    data = Stock.objects.all().order_by('-id')[:32]

    # reverse the list
    data = data[::-1]

    max_amount = max([stock.amount for stock in data])
    min_amount = min([stock.amount for stock in data])
    avg_amount = sum([stock.amount for stock in data]) / len(data)

    return render(request, "core/home.html", {
        "data": data,
        "max": max_amount,
        "min": min_amount,
        "avg": avg_amount,
        "chart_data": json.dumps([{"x": stock.id, "y": stock.amount} for stock in data])
    })


def test_data(request):
    return render(request, "core/test_data.html")


def real_data(request):
    return render(request, "core/real_data.html")


def get_datapoints_test(request):
    default_query_params = { "xstart": 0, "ystart": 0, "length": 1 }
    query_params = { **default_query_params, **request.GET.dict() }
    y = int(query_params["ystart"])
    datapoints = []

    for i in range(int(query_params["length"])):
        y += round(5 + random.random() * (-5-5))
        datapoints.append({ "x": (int(query_params["xstart"]) + i), "y": y})
    
    return HttpResponse(json.dumps(datapoints), content_type="application/json")  


def get_datapoints(request):
    default_query_params = { "xstart": 0, "ystart": 0, "length": 1 }
    query_params = { **default_query_params, **request.GET.dict() }
    y = int(query_params["ystart"])

    data = requests.get("https://api.coinbase.com/v2/prices/BTC-USD/sell", headers={
        'Authorization': 'Bearer abd90df5f27a7b170cd775abf89d632b350b7c1c9d53e08b340cd9832ce52c2c'
    }).json()['data']

    amount = eval(data['amount'])

    Stock.objects.create(base="BTC", currency="USD", amount=amount)

    datapoints = []
 
    for i in range(int(query_params["length"])):
        y = int(amount)
        datapoints.append({ "x": (int(query_params["xstart"]) + i), "y": y})
    
    return HttpResponse(json.dumps(datapoints), content_type="application/json")