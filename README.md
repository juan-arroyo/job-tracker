# Job Tracker — The Survivor

A Django application for tracking job applications across the full hiring pipeline.
Built as part of a live infrastructure demo: the app runs on a K3s cluster and can be
destroyed and rebuilt from scratch in under 15 minutes with a single command.

---

## Stack

| Layer | Technology |
|---|---|
| Backend | Django 5 + Gunicorn |
| Database | PostgreSQL 16 |
| Frontend | HTMX + Tailwind CSS + DaisyUI |
| Reverse proxy | Nginx |
| Container runtime | Docker + Docker Compose (local) |
| Orchestration | K3s / Kubernetes (production) |
| CI/CD | GitHub Actions + Ansible |
| Registry | Docker Hub — `juanmnarroyo/job-tracker:v1` |

---

## Features

- Track job applications across 6 pipeline stages: Applied → Phone Screen → Technical Interview → Final Round → Offer → Rejected
- Manage companies, contacts, and interview rounds per application
- Dashboard with live pipeline breakdown and response rate
- Login/logout with Django authentication — all views protected
- Fixtures with 15 real Dutch and German tech companies (Booking.com, ASML, Adyen, Zalando, Hetzner...)

---

## Architecture

```
Local development:
Browser → Nginx :8000 → Gunicorn (Django) → PostgreSQL

Production (K3s on Hetzner):
Internet → Traefik (Ingress) → Service → Django Pod x2 replicas → PostgreSQL Pod
                ↑
         cert-manager (SSL — Let's Encrypt)
```

---

## Local Development

**Requirements:** Docker, Docker Compose

```bash
# Clone the repo
git clone https://github.com/juan-arroyo/job-tracker.git
cd job-tracker

# Start all services
docker compose up --build

# In a separate terminal — run migrations and load sample data
docker compose exec web python manage.py migrate
docker compose exec web python manage.py loaddata tracker/fixtures/initial_data.json
docker compose exec web python manage.py createsuperuser
```

Open `http://localhost:8000` and log in with the superuser credentials.

---

## Project Structure

```
job-tracker/
├── backend/                  # Django application
│   ├── config/
│   │   └── settings/
│   │       ├── base.py       # shared settings
│   │       ├── dev.py        # local development
│   │       └── k3s.py        # production (K3s + PostgreSQL)
│   └── tracker/              # main app — models, views, templates
│       ├── fixtures/         # sample data with real Dutch/German companies
│       └── templates/
├── nginx/
│   └── nginx.conf            # reverse proxy config for local dev
├── manifests/                # Kubernetes manifests (Fase 2)
├── ansible/                  # deployment playbooks (Fase 2)
└── docker-compose.yml
```

---

## Production Deployment

The app is deployed on a 3-node K3s cluster on Hetzner Cloud:

- **k3s-server** — control plane + GitHub Actions self-hosted runner
- **k3s-agent-1** — Django replica 1 + PostgreSQL
- **k3s-agent-2** — Django replica 2

Deployment is fully automated: `git push` to `main` triggers a GitHub Actions workflow
that runs an Ansible playbook applying the K3s manifests. No manual steps.

Docker image: `juanmnarroyo/job-tracker:v1`  
Live URL: `https://demo.jmarroyo.es` *(available during infrastructure demo)*

---

## Part of a Larger Project

This app is **The Survivor** — one component of a larger infrastructure demo.
A separate control panel ([infrastructure-demo-control](https://github.com/juan-arroyo/infrastructure-demo-control))
allows destroying and rebuilding the entire K3s cluster from scratch via a web interface,
demonstrating Ansible provisioning, Kubernetes orchestration, and automated disaster recovery.
