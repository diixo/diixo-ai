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
    data_path = settings.BASE_DIR / "data" / "model_cards.json"
    with open(data_path, encoding="utf-8") as f:
        data = json.load(f)

    if request.method == "POST":
        action = request.POST.get("action", "add")
        name = request.POST.get("name", "").strip()
        architecture = request.POST.get("architecture", "").strip()

        if name and architecture:
            items = data.setdefault("models", [])

            if action == "edit":
                model_id = request.POST.get("model_id", "")
                parent_id = request.POST.get("parent_id", "").strip() or None
                config_id = request.POST.get("config_id", "").strip() or None
                dataset_ids = request.POST.getlist("dataset_ids")
                for item in items:
                    if item.get("id") == model_id:
                        item["name"] = name
                        item["architecture"] = architecture
                        item["parent_id"] = parent_id
                        item["config_id"] = config_id
                        item["dataset_ids"] = dataset_ids
                        break
            else:
                existing_ids = {m.get("id") for m in items}
                new_id = f"mod_{slugify(name) or len(items) + 1}"
                while new_id in existing_ids:
                    new_id = f"{new_id}-1"
                items.append({
                    "id": new_id,
                    "name": name,
                    "architecture": architecture,
                    "parent_id": None,
                    "config_id": None,
                    "dataset_ids": [],
                })

            with open(data_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        return redirect("app_main:models")

    configs_path = settings.BASE_DIR / "data" / "configs.json"
    with open(configs_path, encoding="utf-8") as f:
        configs_data = json.load(f)
    datasets_path = settings.BASE_DIR / "data" / "datasets.json"
    with open(datasets_path, encoding="utf-8") as f:
        datasets_data = json.load(f)

    models_list = data.get("models", [])
    configs_map = {c["id"]: c["name"] for c in configs_data.get("configs", [])}
    models_map = {m["id"]: m["name"] for m in models_list}
    datasets_list = datasets_data.get("datasets", [])
    datasets_map = {d["id"]: d["name"] for d in datasets_list}

    for m in models_list:
        m["parent_name"] = models_map.get(m.get("parent_id"), "")
        m["config_name"] = configs_map.get(m.get("config_id"), "")
        m["dataset_names"] = [datasets_map.get(did, did) for did in m.get("dataset_ids", [])]

    return render(request, "app_main/models.html", context={
        "title": "Diixo - Models",
        "description": "Model cards registry",
        "goal": data.get("goal", ""),
        "architectures": data.get("architectures", []),
        "models": models_list,
        "configs": configs_data.get("configs", []),
        "datasets": datasets_list,
    })

def instructions(request):
    data_path = settings.BASE_DIR / "data" / "tasks.json"
    with open(data_path, encoding="utf-8") as f:
        data = json.load(f)
    return render(request, "app_main/instructions.html", context={
        "title": "Diixo - Instructions",
        "description": "Diixo instructions description",
        "goal": data.get("goal", ""),
        "tasks": data.get("tasks", []),
    })

def datasets(request):
    data_path = settings.BASE_DIR / "data" / "datasets.json"
    with open(data_path, encoding="utf-8") as f:
        data = json.load(f)

    if request.method == "POST":
        action = request.POST.get("action", "add")
        name = request.POST.get("name", "").strip()
        task = request.POST.get("task", "").strip()
        tags = request.POST.get("tags", "").strip()
        description = request.POST.get("description", "").strip()
        website = request.POST.get("website", "").strip()

        if name:
            items = data.setdefault("datasets", [])
            task_list = [t.strip() for t in task.split(",") if t.strip()] if task else []
            tag_list = [t.strip() for t in tags.split(",") if t.strip()] if tags else []
            links = {"website": website} if website else {}

            if action == "edit":
                dataset_id = request.POST.get("dataset_id", "")
                for item in items:
                    if item.get("id") == dataset_id:
                        item["name"] = name
                        item["task"] = task_list
                        item["tags"] = tag_list
                        item["description"] = description
                        item["links"] = links
                        break
            else:
                existing_ids = {d.get("id") for d in items}
                new_id = slugify(name) or f"dataset-{len(items) + 1}"
                while new_id in existing_ids:
                    new_id = f"{new_id}-1"
                items.append({
                    "id": new_id,
                    "name": name,
                    "task": task_list,
                    "tags": tag_list,
                    "description": description,
                    "links": links,
                })

            with open(data_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        return redirect("app_main:datasets")

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
    data_path = settings.BASE_DIR / "data" / "configs.json"
    with open(data_path, encoding="utf-8") as f:
        data = json.load(f)

    if request.method == "POST":
        action = request.POST.get("action", "add")
        name = request.POST.get("name", "").strip()
        max_len = request.POST.get("max_len", "").strip()
        learning_rate = request.POST.get("learning_rate", "").strip()
        batch_size = request.POST.get("batch_size", "").strip()
        epochs = request.POST.get("epochs", "").strip()

        if name and max_len and learning_rate and batch_size and epochs:
            items = data.setdefault("configs", [])
            micro_batch_size = request.POST.get("micro_batch_size", "").strip()
            sequence_length = request.POST.get("sequence_length", "").strip()

            if action == "edit":
                config_id = request.POST.get("config_id", "")
                for item in items:
                    if item.get("id") == config_id:
                        item["name"] = name
                        item["max_len"] = int(max_len)
                        item["learning_rate"] = float(learning_rate)
                        item["batch_size"] = int(batch_size)
                        item["epochs"] = int(epochs)
                        if micro_batch_size:
                            item["micro_batch_size"] = int(micro_batch_size)
                        else:
                            item.pop("micro_batch_size", None)
                        if sequence_length:
                            item["sequence_length"] = int(sequence_length)
                        else:
                            item.pop("sequence_length", None)
                        break
            else:
                existing_ids = {c.get("id") for c in items}
                new_id = f"conf_{slugify(name) or len(items) + 1}"
                while new_id in existing_ids:
                    new_id = f"{new_id}-1"
                new_item = {
                    "id": new_id,
                    "name": name,
                    "max_len": int(max_len),
                    "learning_rate": float(learning_rate),
                    "batch_size": int(batch_size),
                    "epochs": int(epochs),
                }
                if micro_batch_size:
                    new_item["micro_batch_size"] = int(micro_batch_size)
                if sequence_length:
                    new_item["sequence_length"] = int(sequence_length)
                items.append(new_item)

            with open(data_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        return redirect("app_main:configs")

    return render(request, "app_main/configs.html", context={
        "title": "Diixo - Configs",
        "description": "Training configuration cards",
        "goal": data.get("goal", ""),
        "configs": data.get("configs", []),
    })

def trainers(request):
    return render(request, "app_main/index.html", context={
        "title": "Diixo - Trainers",
        "description": "Diixo trainers description",
    })

def trainings(request):
    models_path = settings.BASE_DIR / "data" / "model_cards.json"
    configs_path = settings.BASE_DIR / "data" / "configs.json"

    with open(models_path, encoding="utf-8") as f:
        models_data = json.load(f)
    with open(configs_path, encoding="utf-8") as f:
        configs_data = json.load(f)

    if request.method == "POST":
        model_in = request.POST.get("model_in", "").strip()
        config_id = request.POST.get("config_id", "").strip()
        model_out_existing = request.POST.get("model_out_existing", "").strip()
        model_out_name = request.POST.get("model_out_name", "").strip()

        if model_in and config_id and (model_out_existing or model_out_name):
            models_list = models_data.setdefault("models", [])

            if model_out_existing:
                for m in models_list:
                    if m["id"] == model_out_existing:
                        m["parent_id"] = model_in
                        m["config_id"] = config_id
                        break
            else:
                existing_model_ids = {m.get("id") for m in models_list}
                model_out_id = f"mod_{slugify(model_out_name) or len(models_list) + 1}"
                while model_out_id in existing_model_ids:
                    model_out_id = f"{model_out_id}-1"

                parent_model = next((m for m in models_list if m["id"] == model_in), None)
                architecture = parent_model["architecture"] if parent_model else "GPT"

                models_list.append({
                    "id": model_out_id,
                    "name": model_out_name,
                    "architecture": architecture,
                    "parent_id": model_in,
                    "config_id": config_id,
                    "dataset_ids": [],
                })

            with open(models_path, "w", encoding="utf-8") as f:
                json.dump(models_data, f, ensure_ascii=False, indent=2)

        return redirect("app_main:trainings")

    models_list = models_data.get("models", [])
    configs_list = configs_data.get("configs", [])
    models_map = {m["id"]: m["name"] for m in models_list}
    configs_map = {c["id"]: c["name"] for c in configs_list}

    children_map = {}
    for m in models_list:
        pid = m.get("parent_id")
        if pid:
            children_map.setdefault(pid, []).append(m["id"])

    roots = [m for m in models_list if not m.get("parent_id")]

    chains = []
    for root in roots:
        chain = []
        current_id = root["id"]
        while current_id:
            model = next((m for m in models_list if m["id"] == current_id), None)
            if not model:
                break
            chain.append({
                "name": model["name"],
                "config_name": configs_map.get(model.get("config_id"), ""),
            })
            children = children_map.get(current_id, [])
            current_id = children[0] if children else None
        chains.append(chain)

    return render(request, "app_main/trainings.html", context={
        "title": "Diixo - Trainings",
        "description": "Training pipeline",
        "goal": "Training pipeline built from model lineage",
        "chains": chains,
        "models": models_list,
        "configs": configs_list,
    })

def evaluators(request):
    return render(request, "app_main/index.html", context={
        "title": "Diixo - Evaluators",
        "description": "Diixo evaluators description",
    })

def evaluations(request):
    data_path = settings.BASE_DIR / "data" / "evaluations.json"
    models_path = settings.BASE_DIR / "data" / "model_cards.json"
    datasets_path = settings.BASE_DIR / "data" / "datasets.json"

    with open(data_path, encoding="utf-8") as f:
        data = json.load(f)
    with open(models_path, encoding="utf-8") as f:
        models_data = json.load(f)
    with open(datasets_path, encoding="utf-8") as f:
        datasets_data = json.load(f)

    if request.method == "POST":
        action = request.POST.get("action", "add")
        name = request.POST.get("name", "").strip()
        eval_type = request.POST.get("eval_type", "").strip()
        metrics = request.POST.get("metrics", "").strip()
        model_id = request.POST.get("model_id", "").strip()
        dataset_id = request.POST.get("dataset_id", "").strip()

        if name:
            items = data.setdefault("evaluations", [])
            metrics_list = [m.strip() for m in metrics.split(",") if m.strip()] if metrics else []

            if action == "edit":
                eval_id = request.POST.get("eval_id", "")
                for item in items:
                    if item.get("id") == eval_id:
                        item["name"] = name
                        item["eval_type"] = eval_type or None
                        item["metrics"] = metrics_list
                        item["model_id"] = model_id or None
                        item["dataset_id"] = dataset_id or None
                        break
            else:
                existing_ids = {e.get("id") for e in items}
                new_id = f"eval_{slugify(name) or len(items) + 1}"
                while new_id in existing_ids:
                    new_id = f"{new_id}-1"
                items.append({
                    "id": new_id,
                    "name": name,
                    "eval_type": eval_type or None,
                    "metrics": metrics_list,
                    "model_id": model_id or None,
                    "dataset_id": dataset_id or None,
                })

            with open(data_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        return redirect("app_main:evaluations")

    models_list = models_data.get("models", [])
    datasets_list = datasets_data.get("datasets", [])
    models_map = {m["id"]: m["name"] for m in models_list}
    datasets_map = {d["id"]: d["name"] for d in datasets_list}

    evaluations = data.get("evaluations", [])
    for e in evaluations:
        e["model_name"] = models_map.get(e.get("model_id"), "")
        e["dataset_name"] = datasets_map.get(e.get("dataset_id"), "")

    return render(request, "app_main/evaluations.html", context={
        "title": "Diixo - Evaluations",
        "description": "Evaluation cards",
        "goal": data.get("goal", ""),
        "eval_types": data.get("eval_types", []),
        "evaluations": evaluations,
        "models": models_list,
        "datasets": datasets_list,
    })
