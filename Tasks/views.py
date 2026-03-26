from datetime import timedelta
from uuid import uuid4

from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.utils import timezone
from django.utils.dateparse import parse_datetime


def _get_tasks(request):
    return request.session.get("tasks", [])


def _save_tasks(request, tasks):
    request.session["tasks"] = tasks
    request.session.modified = True


def _decorate_tasks(tasks):
    decorated = []
    for task in tasks:
        dt = parse_datetime(task["created_at"])
        if timezone.is_naive(dt):
            dt = timezone.make_aware(dt, timezone.get_current_timezone())
        item = task.copy()
        item["created_dt"] = dt
        item["created_date"] = dt.date().isoformat()
        item["created_time"] = dt.strftime("%H:%M")
        decorated.append(item)
    return decorated


def index(request):
    tasks = _get_tasks(request)

    if request.method == "POST":
        description = request.POST.get("description", "").strip()
        due_date = request.POST.get("due_date") or None
        due_time = request.POST.get("due_time") or None

        if description:
            tasks.append(
                {
                    "id": str(uuid4()),
                    "description": description,
                    "due_date": due_date,
                    "due_time": due_time,
                    "completed": False,
                    "created_at": timezone.now().isoformat(),
                }
            )
            _save_tasks(request, tasks)
        return redirect("index")

    cutoff = timezone.now() - timedelta(hours=24)
    visible = [
        task
        for task in _decorate_tasks(tasks)
        if not task["completed"] and task["created_dt"] >= cutoff
    ]
    visible.sort(
        key=lambda t: (
            t["due_date"] or "9999-12-31",
            t["due_time"] or "23:59",
            -(t["created_dt"].timestamp()),
        )
    )
    return render(request, "index.html", {"tasks": visible})


def toggle_task(request, task_id):
    tasks = _get_tasks(request)
    for task in tasks:
        if task["id"] == task_id:
            task["completed"] = not task["completed"]
            break
    _save_tasks(request, tasks)
    return redirect(request.META.get("HTTP_REFERER", "index"))


def delete_task(request, task_id):
    tasks = [task for task in _get_tasks(request) if task["id"] != task_id]
    _save_tasks(request, tasks)
    return redirect(request.META.get("HTTP_REFERER", "index"))


def contact_view(request):
    
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        full_message = f"""
        Name: {name}
        Email: {email}

        Message:
        {message}
        """

        send_mail(
            subject="New Contact Message",
            message=full_message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=["shaikhaltaf1176@gmail.com"],
            fail_silently=False
        )

        return render(request, "thankyou.html")

    return render(request, "contact.html")


def thankyou_view(request):
    return render(request, "thankyou.html")


def tasks_done(request):
    completed_tasks = [
        task for task in _decorate_tasks(_get_tasks(request)) if task["completed"]
    ]
    completed_tasks.sort(
        key=lambda t: (
            -(t["created_dt"].timestamp()),
            t["due_date"] or "9999-12-31",
            t["due_time"] or "23:59",
        )
    )
    return render(request, "Ts_Done.html", {"tasks": completed_tasks})


def tasks_not_done(request):
    cutoff = timezone.now() - timedelta(hours=24)
    overdue_tasks = [
        task
        for task in _decorate_tasks(_get_tasks(request))
        if not task["completed"] and task["created_dt"] < cutoff
    ]
    overdue_tasks.sort(
        key=lambda t: (
            t["due_date"] or "9999-12-31",
            t["due_time"] or "23:59",
            -(t["created_dt"].timestamp()),
        )
    )
    return render(request, "Ts_NotDone.html", {"tasks": overdue_tasks})
