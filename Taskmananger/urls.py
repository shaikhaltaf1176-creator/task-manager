"""
URL configuration for Taskmananger project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from Tasks import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.index, name="index"),
    path("contact/", views.contact_view, name="contact"),
    path("tasks/done/", views.tasks_done, name="tasks_done"),
    path("tasks/not-done/", views.tasks_not_done, name="tasks_not_done"),
    path("tasks/<str:task_id>/toggle/", views.toggle_task, name="toggle_task"),
    path("tasks/<str:task_id>/delete/", views.delete_task, name="delete_task"),
    path("thankyou/", views.thankyou_view, name="thankyou"),
]
