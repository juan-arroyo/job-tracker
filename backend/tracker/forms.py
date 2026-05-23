from django import forms

from .models import Company, JobApplication, Contact, InterviewRound


class CompanyForm(forms.ModelForm):
    """
    Form for creating and editing a Company.
    ModelForm automatically generates fields from the model definition.
    """
    class Meta:
        model = Company
        fields = ["name", "country", "website", "notes"]
        widgets = {
            # Use textarea for notes to give the user more space
            "notes": forms.Textarea(attrs={"rows": 3}),
        }


class JobApplicationForm(forms.ModelForm):
    """
    Form for creating and editing a JobApplication.
    The company field is a dropdown populated from the database.
    """
    class Meta:
        model = JobApplication
        fields = ["company", "position", "date_applied", "status", "job_url", "notes"]
        widgets = {
            # Use date input for proper date picker in the browser
            "date_applied": forms.DateInput(attrs={"type": "date"}),
            "notes": forms.Textarea(attrs={"rows": 3}),
        }


class ContactForm(forms.ModelForm):
    """
    Form for creating and editing a Contact person at a company.
    """
    class Meta:
        model = Contact
        fields = ["company", "name", "linkedin_url", "email", "notes"]
        widgets = {
            "notes": forms.Textarea(attrs={"rows": 3}),
        }


class InterviewRoundForm(forms.ModelForm):
    """
    Form for logging an interview round linked to a specific application.
    """
    class Meta:
        model = InterviewRound
        fields = ["date", "type", "result", "notes"]
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
            "notes": forms.Textarea(attrs={"rows": 3}),
        }