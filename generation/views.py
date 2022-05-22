from django.shortcuts import render
from DataModel.Generation import *


# Create your views here.

def index(request):
    return render(request, 'generation/index.html')


def current(request):
    generation = Generation()
    fig, generation_pie_chart = generation.get_generation_mix().get_pie_chart_mix()
    context = {'generation_pie_chart': generation_pie_chart}
    return render(request, 'generation/current.html', context)


def daterange(request, start_date, end_date):
    generation = Generation(start_date, end_date)
    fig, generation_pie_chart = generation.get_generation_mix().get_pie_chart_mix()
    context = {'generation_pie_chart': generation_pie_chart}
    return render(request, 'generation/current.html', context)


def daterangefromform(request):
    if request.method == "GET":
        req1 = request.GET["start_time"]+'Z'
        req2 = request.GET["end_time"]+'Z'
    return daterange(request, req1, req2)
        # generation = Generation(request.GET["start_time"] + 'Z', request.GET["end_time"] + 'Z')
    # return render(request, 'generation/current.html', context)
