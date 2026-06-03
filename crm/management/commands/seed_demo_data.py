import os
import random
from datetime import timedelta
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils import timezone

from crm.models import Client, Deal, Lead, Note, Task


class Command(BaseCommand):
    help = "Seed realistic read-only demo data for ServiceFlow CRM."

    def handle(self, *args, **options):
        random.seed(42)
        Note.objects.all().delete()
        Task.objects.all().delete()
        Deal.objects.all().delete()
        Lead.objects.all().delete()
        Client.objects.all().delete()

        clients = self.create_clients()
        leads = self.create_leads(clients)
        self.create_deals(leads)
        self.create_tasks(leads)
        self.create_notes(leads)
        self.ensure_env_superuser()

        self.stdout.write(self.style.SUCCESS("Seeded ServiceFlow CRM demo data."))

    def create_clients(self):
        rows = [
            ("Olivia Harris", "BrightPath Cleaning", "olivia@brightpathclean.com", "+1 312 555 0148", "Website"),
            ("Marcus Reed", "Northside Auto Repair", "marcus@northsideauto.example", "+1 773 555 0182", "Referral"),
            ("Emma Clark", "LuxeGlow Beauty Salon", "emma@luxeglow.example", "+1 646 555 0190", "Instagram"),
            ("Daniel Brooks", "CraftLine Renovations", "daniel@craftline.example", "+1 718 555 0111", "Google Ads"),
            ("Sophia Nguyen", "FreshNest Home Services", "sophia@freshnest.example", "+1 206 555 0133", "Website"),
            ("Noah Patel", "City Dental Care", "noah@citydental.example", "+1 415 555 0177", "LinkedIn"),
            ("Ava Martinez", "Rapid Appliance Repair", "ava@rapidappliance.example", "+1 305 555 0154", "Referral"),
            ("Ethan Wilson", "MetroMove Logistics", "ethan@metromove.example", "+1 212 555 0169", "Cold Outreach"),
            ("Mia Thompson", "Summit HVAC Service", "mia@summithvac.example", "+1 503 555 0188", "Google Ads"),
            ("Liam Carter", "OakBridge Construction", "liam@oakbridge.example", "+1 602 555 0119", "Referral"),
            ("Isabella Scott", "PureSpace Offices", "isabella@purespace.example", "+1 617 555 0198", "Website"),
            ("James Morgan", "FixPro Garage Doors", "james@fixpro.example", "+1 404 555 0171", "Facebook"),
            ("Charlotte Young", "BellaCare Spa", "charlotte@bellacare.example", "+1 702 555 0128", "Instagram"),
            ("Benjamin Lee", "UrbanFit Installers", "ben@urbanfit.example", "+1 213 555 0162", "Partner"),
            ("Amelia Walker", "GreenLeaf Maintenance", "amelia@greenleaf.example", "+1 919 555 0150", "Website"),
        ]
        now = timezone.now()
        clients = []
        for index, (name, company, email, phone, source) in enumerate(rows):
            clients.append(
                Client.objects.create(
                    name=name,
                    company=company,
                    email=email,
                    phone=phone,
                    source=source,
                    is_active=index not in {7, 13},
                    created_at=now - timedelta(days=120 - index * 6),
                )
            )
        return clients

    def create_leads(self, clients):
        service_requests = [
            "Recurring office cleaning contract",
            "Fleet maintenance scheduling",
            "Salon booking workflow cleanup",
            "Kitchen renovation estimate",
            "Move-out cleaning package",
            "Dental recall automation",
            "Emergency refrigerator repair",
            "Delivery route quote",
            "Annual HVAC maintenance plan",
            "New build finishing work",
            "Commercial carpet cleaning",
            "Garage door replacement",
            "Spa membership follow-up",
            "Furniture assembly for apartments",
            "Seasonal lawn maintenance",
            "Post-construction cleanup",
            "Brake service campaign",
            "Beauty package upsell",
            "Bathroom remodel consultation",
            "Washer repair lead",
            "Small warehouse delivery setup",
            "Air conditioner replacement",
            "Roofing repair inquiry",
            "Office disinfection quote",
            "Appliance warranty callback",
        ]
        descriptions = [
            "Client requested a clear quote and timeline before approving the work.",
            "Needs follow-up with service options and a simple proposal.",
            "Owner is comparing vendors and wants a fast response.",
            "High-value opportunity with multiple decision makers involved.",
            "Small job now, but strong potential for recurring work.",
        ]
        statuses = [
            Lead.Status.NEW,
            Lead.Status.IN_PROGRESS,
            Lead.Status.QUALIFIED,
            Lead.Status.WON,
            Lead.Status.LOST,
        ]
        priorities = [Lead.Priority.LOW, Lead.Priority.MEDIUM, Lead.Priority.HIGH]
        now = timezone.now()
        leads = []
        for index, title in enumerate(service_requests):
            leads.append(
                Lead.objects.create(
                    client=clients[index % len(clients)],
                    title=title,
                    description=descriptions[index % len(descriptions)],
                    status=statuses[index % len(statuses)],
                    priority=priorities[(index + 1) % len(priorities)],
                    estimated_budget=Decimal(random.randrange(450, 12500, 50)),
                    created_at=now - timedelta(days=150 - index * 5),
                )
            )
        return leads

    def create_deals(self, leads):
        statuses = [
            Deal.Status.OPEN,
            Deal.Status.PROPOSAL_SENT,
            Deal.Status.NEGOTIATION,
            Deal.Status.WON,
            Deal.Status.LOST,
        ]
        now = timezone.now()
        for index, lead in enumerate(leads[:15]):
            status = statuses[index % len(statuses)]
            created_at = now - timedelta(hours=index + 1)
            if status != Deal.Status.WON:
                created_at = now - timedelta(days=45 - index * 3)

            Deal.objects.create(
                lead=lead,
                title=f"{lead.title} deal",
                value=lead.estimated_budget + Decimal(random.randrange(250, 2400, 50)),
                status=status,
                expected_close_date=timezone.localdate() + timedelta(days=(index - 4) * 4),
                created_at=created_at,
            )

    def create_tasks(self, leads):
        task_titles = [
            "Call client to confirm requirements",
            "Prepare service estimate",
            "Send proposal email",
            "Schedule site visit",
            "Follow up after quote",
            "Review budget details",
            "Confirm decision maker",
            "Update deal stage",
            "Collect missing photos",
            "Prepare monthly report",
        ]
        statuses = [Task.Status.TODO, Task.Status.IN_PROGRESS, Task.Status.DONE]
        for index in range(20):
            Task.objects.create(
                lead=leads[index % len(leads)] if index % 5 != 0 else None,
                title=task_titles[index % len(task_titles)],
                description="Internal task for tracking the next step in the service workflow.",
                status=statuses[index % len(statuses)],
                due_date=timezone.localdate() + timedelta(days=index - 5),
                created_at=timezone.now() - timedelta(days=20 - index),
            )

    def create_notes(self, leads):
        note_texts = [
            "Client prefers email updates and a concise quote.",
            "Potential recurring service if first job goes well.",
            "Asked for examples from similar service businesses.",
            "Budget confirmed; waiting on final schedule.",
            "Needs owner approval before the proposal can move forward.",
        ]
        for index, lead in enumerate(leads[:12]):
            if index % 2 == 0:
                Note.objects.create(
                    lead=lead,
                    text=note_texts[index % len(note_texts)],
                    created_at=timezone.now() - timedelta(days=index + 1),
                )

    def ensure_env_superuser(self):
        username = os.environ.get("DJANGO_SUPERUSER_USERNAME")
        email = os.environ.get("DJANGO_SUPERUSER_EMAIL")
        password = os.environ.get("DJANGO_SUPERUSER_PASSWORD")
        if not all([username, email, password]):
            return

        User = get_user_model()
        if User.objects.filter(username=username).exists():
            return
        User.objects.create_superuser(username=username, email=email, password=password)
        self.stdout.write("Created superuser from environment variables.")
