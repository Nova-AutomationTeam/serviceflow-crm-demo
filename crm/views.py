import json
from collections import OrderedDict
from decimal import Decimal

from django.db.models import Count, Q, Sum
from django.db.models.functions import TruncMonth
from django.shortcuts import render
from django.utils import timezone

from .models import Client, Deal, Lead, Task


def money(value):
    return value or Decimal("0.00")


def group_by_choices(queryset, choices):
    grouped = OrderedDict((value, []) for value, _label in choices)
    for item in queryset:
        grouped[item.status].append(item)
    return grouped


def landing(request):
    return render(request, "crm/landing.html")


def dashboard(request):
    today = timezone.localdate()
    current_month_revenue = Deal.objects.filter(
        status=Deal.Status.WON,
        created_at__year=today.year,
        created_at__month=today.month,
    ).aggregate(total=Sum("value"))["total"]

    leads_by_month = (
        Lead.objects.annotate(month=TruncMonth("created_at"))
        .values("month")
        .annotate(total=Count("id"))
        .order_by("month")
    )
    deal_status_counts = dict(
        Deal.objects.values("status").annotate(total=Count("id")).values_list("status", "total")
    )

    pipeline_deals = Deal.objects.select_related("lead", "lead__client").order_by(
        "status", "expected_close_date"
    )

    context = {
        "total_leads": Lead.objects.count(),
        "active_clients": Client.objects.filter(is_active=True).count(),
        "open_deals": Deal.objects.exclude(
            status__in=[Deal.Status.WON, Deal.Status.LOST]
        ).count(),
        "monthly_revenue": money(current_month_revenue),
        "recent_leads": Lead.objects.select_related("client")[:6],
        "pipeline": group_by_choices(pipeline_deals, Deal.Status.choices),
        "upcoming_tasks": Task.objects.select_related("lead")
        .exclude(status=Task.Status.DONE)
        .filter(due_date__gte=today)[:6],
        "leads_month_labels_json": json.dumps(
            [row["month"].strftime("%b") for row in leads_by_month]
        ),
        "leads_month_counts_json": json.dumps([row["total"] for row in leads_by_month]),
        "deal_status_labels_json": json.dumps([label for _value, label in Deal.Status.choices]),
        "deal_status_counts_json": json.dumps(
            [deal_status_counts.get(value, 0) for value, _label in Deal.Status.choices]
        ),
    }
    return render(request, "crm/dashboard.html", context)


def leads(request):
    query = request.GET.get("q", "").strip()
    lead_list = Lead.objects.select_related("client")
    if query:
        lead_list = lead_list.filter(
            Q(title__icontains=query)
            | Q(description__icontains=query)
            | Q(status__icontains=query)
            | Q(priority__icontains=query)
            | Q(client__name__icontains=query)
            | Q(client__company__icontains=query)
        )
    return render(request, "crm/leads.html", {"leads": lead_list, "query": query})


def clients(request):
    return render(
        request,
        "crm/clients.html",
        {"clients": Client.objects.prefetch_related("leads")},
    )


def deals(request):
    deal_list = Deal.objects.select_related("lead", "lead__client").order_by(
        "status", "expected_close_date"
    )
    return render(
        request,
        "crm/deals.html",
        {"pipeline": group_by_choices(deal_list, Deal.Status.choices)},
    )


def tasks(request):
    task_list = Task.objects.select_related("lead", "lead__client")
    return render(
        request,
        "crm/tasks.html",
        {"task_groups": group_by_choices(task_list, Task.Status.choices)},
    )
