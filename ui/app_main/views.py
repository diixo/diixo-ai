import json

from django.conf import settings
from django.shortcuts import render, redirect
from django.utils.text import slugify


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


def models(request):
    data_path = settings.BASE_DIR / "data" / "models.json"
    with open(data_path, encoding="utf-8") as f:
        data = json.load(f)
    return render(request, "app_main/models.html", context={
        "title": "Diixo - Models",
        "description": "Diixo models description",
        "goal": data.get("goal", ""),
        "model_types": data.get("model_types", []),
    })

def tasks(request):
    data_path = settings.BASE_DIR / "data" / "tasks.json"
    with open(data_path, encoding="utf-8") as f:
        data = json.load(f)
    return render(request, "app_main/tasks.html", context={
        "title": "Diixo - Tasks",
        "description": "Diixo tasks description",
        "goal": data.get("goal", ""),
        "tasks": data.get("tasks", []),
    })

def datasets(request):
    data_path = settings.BASE_DIR / "data" / "datasets.json"
    with open(data_path, encoding="utf-8") as f:
        data = json.load(f)
    return render(request, "app_main/datasets.html", context={
        "title": "Diixo - Datasets",
        "description": "Diixo datasets description",
        "goal": data.get("goal", ""),
        "source": data.get("source", ""),
        "datasets": data.get("datasets", []),
    })

def templates(request):
    data_path = settings.BASE_DIR / "data" / "templates.json"
    with open(data_path, encoding="utf-8") as f:
        data = json.load(f)

    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        description = request.POST.get("description", "").strip()
        template = request.POST.get("template", "").strip()
        if name and template:
            items = data.setdefault("templates", [])
            existing_ids = {t.get("id") for t in items}
            new_id = slugify(name) or f"template-{len(items) + 1}"
            while new_id in existing_ids:
                new_id = f"{new_id}-1"
            items.append({
                "id": new_id,
                "name": name,
                "description": description,
                "template": template,
            })
            with open(data_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        return redirect("app_main:prompt_templates")

    return render(request, "app_main/prompt-templates.html", context={
        "title": "Diixo - Templates",
        "description": "Diixo templates description",
        "goal": data.get("goal", ""),
        "templates": data.get("templates", []),
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
