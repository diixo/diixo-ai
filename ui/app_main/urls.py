
from django.urls import path
from . import views

app_name = "app_main"

urlpatterns = [
    path("", views.main, name="main"),
    path("models", views.models, name="models"),
    path("instructions", views.instructions, name="instructions"),
    path("datasets", views.datasets, name="datasets"),
    path("prompt-templates", views.templates, name="prompt_templates"),
    path("configs", views.configs, name="configs"),
    path("trainers", views.trainers, name="trainers"),
    path("trainings", views.trainings, name="trainings"),
    path("evaluators", views.evaluators, name="evaluators"),
    path("evaluations", views.evaluations, name="evaluations"),
    path("dashboard", views.dashboard, name="dashboard"),
    path("report", views.report, name="report"),
]
