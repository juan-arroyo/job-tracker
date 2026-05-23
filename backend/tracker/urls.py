from django.urls import path

from . import views

app_name = "tracker"  # namespace to avoid URL name collisions with other apps

urlpatterns = [
    # Company URLs
    path("", views.dashboard, name="dashboard"),
    path("companies/", views.company_list, name="company_list"),
    path("companies/create/", views.company_create, name="company_create"),
    path("companies/<int:pk>/", views.company_detail, name="company_detail"),
    path("companies/<int:pk>/edit/", views.company_edit, name="company_edit"),
    path("companies/<int:pk>/delete/", views.company_delete, name="company_delete"),

    # JobApplication URLs
    path("applications/", views.application_list, name="application_list"),
    path("applications/create/", views.application_create, name="application_create"),
    path("applications/<int:pk>/", views.application_detail, name="application_detail"),
    path("applications/<int:pk>/edit/", views.application_edit, name="application_edit"),
    path("applications/<int:pk>/delete/", views.application_delete, name="application_delete"),

    # Contact URLs
    path("contacts/", views.contact_list, name="contact_list"),
    path("contacts/create/", views.contact_create, name="contact_create"),
    path("contacts/<int:pk>/edit/", views.contact_edit, name="contact_edit"),
    path("contacts/<int:pk>/delete/", views.contact_delete, name="contact_delete"),

    # InterviewRound URLs — always linked to a specific application
    path("applications/<int:app_pk>/rounds/create/", views.round_create, name="round_create"),
    path("rounds/<int:pk>/delete/", views.round_delete, name="round_delete"),
]