from django.shortcuts import render, get_object_or_404, redirect

from .models import Company, JobApplication, Contact, InterviewRound
from .forms import CompanyForm, JobApplicationForm, ContactForm, InterviewRoundForm

from django.contrib.auth.decorators import login_required



@login_required
def dashboard(request):
    # Main dashboard — shows a summary of the entire job search at a glance
    total_companies = Company.objects.count()
    total_applications = JobApplication.objects.count()
    total_contacts = Contact.objects.count()

    # Exclude terminal states to show what's still in play
    active_applications = JobApplication.objects.exclude(
        status__in=["offer", "rejected"]
    ).count()

    # Count applications per status — calculate percentage here in Python
    # because Django templates cannot do division inside style attributes
    status_counts = {}
    for status_value, status_label in JobApplication.STATUS_CHOICES:
        count = JobApplication.objects.filter(status=status_value).count()
        percentage = round((count / total_applications * 100)) if total_applications > 0 else 0
        status_counts[status_value] = {
            "label": status_label,
            "count": count,
            "percentage": percentage,
        }

    # Response rate — % of applications that moved beyond "applied"
    # If total is 0 we avoid division by zero
    moved_forward = JobApplication.objects.exclude(status="applied").count()
    response_rate = round((moved_forward / total_applications * 100)) if total_applications > 0 else 0

    # Get the 5 most recent applications for the activity feed
    recent_applications = JobApplication.objects.select_related("company").order_by(
        "-date_applied"
    )[:5]

    return render(request, "tracker/dashboard.html", {
        "total_companies": total_companies,
        "total_applications": total_applications,
        "total_contacts": total_contacts,
        "active_applications": active_applications,
        "status_counts": status_counts,
        "response_rate": response_rate,
        "recent_applications": recent_applications,
    })


@login_required
def company_list(request):
    # Retrieve all companies ordered alphabetically (defined in model Meta)
    companies = Company.objects.all()
    return render(request, "tracker/company_list.html", {"companies": companies})


@login_required
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


@login_required
def company_detail(request, pk):
    # get_object_or_404 returns 404 page if company doesn't exist instead of crashing
    company = get_object_or_404(Company, pk=pk)
    applications = company.applications.all()
    return render(request, "tracker/company_detail.html", {
        "company": company,
        "applications": applications,
    })


@login_required
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


@login_required
def company_delete(request, pk):
    company = get_object_or_404(Company, pk=pk)
    if request.method == "POST":
        company.delete()
        return redirect("tracker:company_list")
    return render(request, "tracker/company_confirm_delete.html", {"company": company})


@login_required
def application_list(request):
    # Retrieve all applications with their related company in a single query
    # select_related avoids N+1 queries — fetches company data in one JOIN
    applications = JobApplication.objects.select_related("company").all()
    return render(request, "tracker/application_list.html", {"applications": applications})


@login_required
def application_create(request):
    if request.method == "POST":
        form = JobApplicationForm(request.POST)
        if form.is_valid():
            application = form.save()
            return redirect("tracker:application_detail", pk=application.pk)
    else:
        form = JobApplicationForm()
    return render(request, "tracker/application_form.html", {"form": form, "action": "Create"})


@login_required
def application_detail(request, pk):
    application = get_object_or_404(JobApplication, pk=pk)
    interview_rounds = application.interview_rounds.all()
    return render(request, "tracker/application_detail.html", {
        "application": application,
        "interview_rounds": interview_rounds,
    })


@login_required
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


@login_required
def application_delete(request, pk):
    application = get_object_or_404(JobApplication, pk=pk)
    if request.method == "POST":
        application.delete()
        return redirect("tracker:application_list")
    return render(request, "tracker/application_confirm_delete.html", {"application": application})


@login_required
def contact_list(request):
    # List all contacts across all companies
    contacts = Contact.objects.select_related("company").all()
    return render(request, "tracker/contact_list.html", {"contacts": contacts})


@login_required
def contact_create(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("tracker:contact_list")
    else:
        form = ContactForm()
    return render(request, "tracker/contact_form.html", {"form": form, "action": "Create"})


@login_required
def contact_edit(request, pk):
    contact = get_object_or_404(Contact, pk=pk)
    if request.method == "POST":
        form = ContactForm(request.POST, instance=contact)
        if form.is_valid():
            form.save()
            return redirect("tracker:contact_list")
    else:
        form = ContactForm(instance=contact)
    return render(request, "tracker/contact_form.html", {"form": form, "action": "Edit"})


@login_required
def contact_delete(request, pk):
    contact = get_object_or_404(Contact, pk=pk)
    if request.method == "POST":
        contact.delete()
        return redirect("tracker:contact_list")
    return render(request, "tracker/contact_confirm_delete.html", {"contact": contact})


@login_required
def round_create(request, app_pk):
    # InterviewRound is always created in the context of a specific application
    application = get_object_or_404(JobApplication, pk=app_pk)
    if request.method == "POST":
        form = InterviewRoundForm(request.POST)
        if form.is_valid():
            round = form.save(commit=False)
            # Link the round to the application before saving
            round.application = application
            round.save()
            return redirect("tracker:application_detail", pk=application.pk)
    else:
        form = InterviewRoundForm()
    return render(request, "tracker/round_form.html", {
        "form": form,
        "application": application,
    })


@login_required
def round_delete(request, pk):
    round = get_object_or_404(InterviewRound, pk=pk)
    application_pk = round.application.pk
    if request.method == "POST":
        round.delete()
        return redirect("tracker:application_detail", pk=application_pk)
    return render(request, "tracker/round_confirm_delete.html", {"round": round})