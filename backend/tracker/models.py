from django.db import models


class Company(models.Model):
    """
    Represents a company we are targeting in the job search.
    Serves as the central entity — all applications and contacts belong to a company.
    """
    name = models.CharField(max_length=200)
    country = models.CharField(max_length=100)
    website = models.URLField(blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "companies"
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} ({self.country})"


class JobApplication(models.Model):
    """
    Tracks a single job application at a specific company.
    Status follows the typical hiring pipeline stages.
    """
    # Status choices reflect the real stages of a hiring process
    STATUS_CHOICES = [
        ("applied", "Applied"),
        ("phone_screen", "Phone Screen"),
        ("technical", "Technical Interview"),
        ("final_round", "Final Round"),
        ("offer", "Offer"),
        ("rejected", "Rejected"),
    ]

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,  # if a company is deleted, its applications are deleted too
        related_name="applications",
    )
    position = models.CharField(max_length=200)
    date_applied = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="applied")
    job_url = models.URLField(blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["-date_applied"]  # most recent applications first

    def __str__(self):
        return f"{self.position} at {self.company.name} — {self.status}"


class Contact(models.Model):
    """
    A person at a company who is relevant to the job search.
    Could be a recruiter, hiring manager, or technical lead.
    """
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="contacts",
    )
    name = models.CharField(max_length=200)
    linkedin_url = models.URLField(blank=True)
    email = models.EmailField(blank=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.name} @ {self.company.name}"


class InterviewRound(models.Model):
    """
    Represents a single interview round within a job application.
    One application can have multiple rounds (phone screen, technical, final).
    """
    TYPE_CHOICES = [
        ("technical", "Technical"),
        ("hr", "HR / Recruiter"),
        ("final", "Final Round"),
    ]

    RESULT_CHOICES = [
        ("pending", "Pending"),
        ("passed", "Passed"),
        ("failed", "Failed"),
    ]

    application = models.ForeignKey(
        JobApplication,
        on_delete=models.CASCADE,
        related_name="interview_rounds",
    )
    date = models.DateField()
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    result = models.CharField(max_length=20, choices=RESULT_CHOICES, default="pending")
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["date"]

    def __str__(self):
        return f"{self.type} round for {self.application}"