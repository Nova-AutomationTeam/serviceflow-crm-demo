from django.urls import path

from . import views


app_name = "crm"

urlpatterns = [
    path("", views.landing, name="landing"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("leads/", views.leads, name="leads"),
    path("clients/", views.clients, name="clients"),
    path("deals/", views.deals, name="deals"),
    path("tasks/", views.tasks, name="tasks"),
]
