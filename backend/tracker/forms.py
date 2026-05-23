from django import forms

from .models import Company, JobApplication


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