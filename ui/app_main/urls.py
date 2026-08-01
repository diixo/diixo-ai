
from django.urls import path
from . import views

app_name = "app_main"

urlpatterns = [
    path("", views.main, name="main"),
    path("models", views.models, name="models"),
    path("datasets", views.datasets, name="datasets"),
    path("instructions", views.instructions, name="instructions"),
    path("tasks", views.tasks, name="tasks"),
    path("prompt-templates", views.prompt_templates, name="prompt_templates"),
    path("configs", views.configs, name="configs"),
    path("trainers", views.trainers, name="trainers"),
    path("trainings", views.trainings, name="trainings"),
    path("evaluators", views.evaluators, name="evaluators"),
    path("evaluations", views.evaluations, name="evaluations"),
    path("dashboard", views.dashboard, name="dashboard"),
    path("report", views.report, name="report"),
]
