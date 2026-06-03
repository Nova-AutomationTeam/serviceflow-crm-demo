from django.db import models
from django.utils import timezone


class Client(models.Model):
    name = models.CharField(max_length=120)
    email = models.EmailField()
    phone = models.CharField(max_length=40)
    company = models.CharField(max_length=160)
    source = models.CharField(max_length=80)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["-created_at", "name"]

    def __str__(self):
        return f"{self.name} - {self.company}"


class Lead(models.Model):
    class Status(models.TextChoices):
        NEW = "New", "New"
        IN_PROGRESS = "In Progress", "In Progress"
        QUALIFIED = "Qualified", "Qualified"
        WON = "Won", "Won"
        LOST = "Lost", "Lost"

    class Priority(models.TextChoices):
        LOW = "Low", "Low"
        MEDIUM = "Medium", "Medium"
        HIGH = "High", "High"

    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="leads")
    title = models.CharField(max_length=180)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.NEW)
    priority = models.CharField(
        max_length=10, choices=Priority.choices, default=Priority.MEDIUM
    )
    estimated_budget = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at", "title"]

    def __str__(self):
        return self.title


class Deal(models.Model):
    class Status(models.TextChoices):
        OPEN = "Open", "Open"
        PROPOSAL_SENT = "Proposal Sent", "Proposal Sent"
        NEGOTIATION = "Negotiation", "Negotiation"
        WON = "Won", "Won"
        LOST = "Lost", "Lost"

    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, related_name="deals")
    title = models.CharField(max_length=180)
    value = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.OPEN)
    expected_close_date = models.DateField()
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["expected_close_date", "-value"]

    def __str__(self):
        return self.title


class Task(models.Model):
    class Status(models.TextChoices):
        TODO = "Todo", "Todo"
        IN_PROGRESS = "In Progress", "In Progress"
        DONE = "Done", "Done"

    lead = models.ForeignKey(
        Lead, on_delete=models.SET_NULL, related_name="tasks", null=True, blank=True
    )
    title = models.CharField(max_length=180)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.TODO)
    due_date = models.DateField()
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["due_date", "status"]

    def __str__(self):
        return self.title


class Note(models.Model):
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, related_name="notes")
    text = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Note for {self.lead}"
