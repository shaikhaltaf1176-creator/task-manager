from datetime import timedelta

from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from .models import Task


def index(request):
    if request.method == "POST":
        description = request.POST.get("description", "").strip()
        due_date = request.POST.get("due_date") or None
        due_time = request.POST.get("due_time") or None

        if description:
            Task.objects.create(
                description=description,
                due_date=due_date,
                due_time=due_time,
            )
        return redirect("index")

    cutoff = timezone.now() - timedelta(hours=24)
    tasks = (
        Task.objects.filter(created_at__gte=cutoff, completed=False)
        .order_by("due_date", "due_time", "-created_at")
    )
    return render(request, "index.html", {"tasks": tasks})


def toggle_task(request, pk):
    task = get_object_or_404(Task, pk=pk)
    task.completed = not task.completed
    task.save()
    return redirect("index")


def delete_task(request, pk):
    task = get_object_or_404(Task, pk=pk)
    task.delete()
    return redirect("index")


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
    completed_tasks = Task.objects.filter(completed=True).order_by(
        "-created_at", "due_date", "due_time"
    )
    return render(request, "Ts_Done.html", {"tasks": completed_tasks})


def tasks_not_done(request):
    cutoff = timezone.now() - timedelta(hours=24)
    overdue_tasks = Task.objects.filter(created_at__lt=cutoff, completed=False).order_by(
        "due_date", "due_time", "-created_at"
    )
    return render(request, "Ts_NotDone.html", {"tasks": overdue_tasks})
