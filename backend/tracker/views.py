from django.shortcuts import render, get_object_or_404, redirect

from .forms import CompanyForm, JobApplicationForm
from .models import Company, JobApplication


def dashboard(request):
    # Main dashboard — shows a summary of the entire job search at a glance
    total_companies = Company.objects.count()
    total_applications = JobApplication.objects.count()

    # Count applications by status to show the pipeline overview
    active_applications = JobApplication.objects.exclude(
        status__in=["offer", "rejected"]
    ).count()

    # Get the 5 most recent applications for the activity feed
    recent_applications = JobApplication.objects.select_related("company").order_by(
        "-date_applied"
    )[:5]

    return render(request, "tracker/dashboard.html", {
        "total_companies": total_companies,
        "total_applications": total_applications,
        "active_applications": active_applications,
        "recent_applications": recent_applications,
    })


def company_list(request):
    # Retrieve all companies ordered alphabetically (defined in model Meta)
    companies = Company.objects.all()
    return render(request, "tracker/company_list.html", {"companies": companies})


def company_create(request):
    if request.method == "POST":
        form = CompanyForm(request.POST)
        if form.is_valid():
            company = form.save()
            return redirect("tracker:company_detail", pk=company.pk)
    else:
        # GET request — show empty form
        form = CompanyForm()
    return render(request, "tracker/company_form.html", {"form": form, "action": "Create"})


def company_detail(request, pk):
    # get_object_or_404 returns 404 page if company doesn't exist instead of crashing
    company = get_object_or_404(Company, pk=pk)
    applications = company.applications.all()
    return render(request, "tracker/company_detail.html", {
        "company": company,
        "applications": applications,
    })


def company_edit(request, pk):
    company = get_object_or_404(Company, pk=pk)
    if request.method == "POST":
        form = CompanyForm(request.POST, instance=company)
        if form.is_valid():
            form.save()
            return redirect("tracker:company_detail", pk=company.pk)
    else:
        # Pre-populate form with existing company data
        form = CompanyForm(instance=company)
    return render(request, "tracker/company_form.html", {"form": form, "action": "Edit"})


def company_delete(request, pk):
    company = get_object_or_404(Company, pk=pk)
    if request.method == "POST":
        company.delete()
        return redirect("tracker:company_list")
    return render(request, "tracker/company_confirm_delete.html", {"company": company})


def application_list(request):
    # Retrieve all applications with their related company in a single query
    # select_related avoids N+1 queries — fetches company data in one JOIN
    applications = JobApplication.objects.select_related("company").all()
    return render(request, "tracker/application_list.html", {"applications": applications})


def application_create(request):
    if request.method == "POST":
        form = JobApplicationForm(request.POST)
        if form.is_valid():
            application = form.save()
            return redirect("tracker:application_detail", pk=application.pk)
    else:
        form = JobApplicationForm()
    return render(request, "tracker/application_form.html", {"form": form, "action": "Create"})


def application_detail(request, pk):
    application = get_object_or_404(JobApplication, pk=pk)
    interview_rounds = application.interview_rounds.all()
    return render(request, "tracker/application_detail.html", {
        "application": application,
        "interview_rounds": interview_rounds,
    })


def application_edit(request, pk):
    application = get_object_or_404(JobApplication, pk=pk)
    if request.method == "POST":
        form = JobApplicationForm(request.POST, instance=application)
        if form.is_valid():
            form.save()
            return redirect("tracker:application_detail", pk=application.pk)
    else:
        form = JobApplicationForm(instance=application)
    return render(request, "tracker/application_form.html", {"form": form, "action": "Edit"})


def application_delete(request, pk):
    application = get_object_or_404(JobApplication, pk=pk)
    if request.method == "POST":
        application.delete()
        return redirect("tracker:application_list")
    return render(request, "tracker/application_confirm_delete.html", {"application": application})