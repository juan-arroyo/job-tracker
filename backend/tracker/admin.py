from django.contrib import admin

from .models import Company, Contact, JobApplication, InterviewRound


# Register all models so they are accessible from the Django admin panel.
# This lets us verify data visually during development.
admin.site.register(Company)
admin.site.register(Contact)
admin.site.register(JobApplication)
admin.site.register(InterviewRound)