import json
import os

from django.conf import settings
from django.shortcuts import render, redirect


def main(request):
    return render(request, "app_main/index.html", context={
        "title": "Diixo",
        "description": "Diixo description"})


def dashboard(request):
    return render(request, "app_main/dashboard.html", context={
        "title": "Diixo - Dashboard",
        "description": "Diixo dashboard description"})


def report(request):
    return render(request, "app_main/report.html", context={
        "title": "Diixo - Reports",
        "description": "Reports output",
    })


def aispice(request):
    return render(request, "app_main/index.html", context={
        "title": "Diixo - main",
        "description": "Diixo output",
    })

def models(request):
    return render(request, "app_main/index.html", context={
        "title": "Diixo - Models",
        "description": "Diixo models description",
    })

def tasks(request):
    return render(request, "app_main/index.html", context={
        "title": "Diixo - Tasks",
        "description": "Diixo tasks description",
    })

def datasets(request):
    return render(request, "app_main/index.html", context={
        "title": "Diixo - Datasets",
        "description": "Diixo datasets description",
    })

def configs(request):
    return render(request, "app_main/index.html", context={
        "title": "Diixo - Configs",
        "description": "Diixo configs description",
    })

def trainers(request):
    return render(request, "app_main/index.html", context={
        "title": "Diixo - Trainers",
        "description": "Diixo trainers description",
    })

def trainings(request):
    return render(request, "app_main/index.html", context={
        "title": "Diixo - Trainings",
        "description": "Diixo trainings description",
    })

def evaluators(request):
    return render(request, "app_main/index.html", context={
        "title": "Diixo - Evaluators",
        "description": "Diixo evaluators description",
    })

def evaluations(request):
    return render(request, "app_main/index.html", context={
        "title": "Diixo - Evaluations",
        "description": "Diixo evaluations description",
    })
