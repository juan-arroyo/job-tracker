# Job Tracker — Local Setup Guide

This file documents every secret and file you need to create before working on this project.
None of these files are in Git — they contain credentials and must never be committed.

---

## Scenario 1 — Local development (day to day)

**Goal:** Run the app locally with Docker Compose.

### Files needed

#### `backend/.env`
Copy from Vaultwarden → **".env job-tracker"**
Create at: `backend/.env`

```
SECRET_KEY=
DB_NAME=
DB_USER=
DB_PASSWORD=
DB_HOST=db
DB_PORT=5432
```

> For local development, DB values can be anything — they just need to match `docker-compose.yml`.
> `DB_HOST` must always be `db` (the Docker Compose service name).

### Start the app

```bash
docker compose up --build

# In a separate terminal — only needed the first time
docker compose exec web python manage.py migrate
docker compose exec web python manage.py loaddata tracker/fixtures/initial_data.json
docker compose exec web python manage.py createsuperuser
```

Open `http://localhost:8000`

---

## Scenario 2 — Manual provisioning (Disaster Recovery)

**Goal:** Rebuild the entire K3s cluster from scratch by running `provision.yml`.
Only needed after a full DR or when setting up a new machine for the first time.

### Files needed

#### `ansible/vars/provision_secrets.yml`
Copy from Vaultwarden → **"provision_secrets.yml"** (stored as plaintext note)
Create at: `ansible/vars/provision_secrets.yml`
Then encrypt it:

```bash
ansible-vault encrypt ansible/vars/provision_secrets.yml
```

> Store the vault password in Vaultwarden → **"ansible-vault password"**
> The file contains:
> - `github_pat` — GitHub Personal Access Token to register the Actions runner
> - `k3s_server_ip` — Hetzner k3s-server public IP
> - `k3s_agent1_ip` — Hetzner k3s-agent-1 public IP
> - `k3s_agent2_ip` — Hetzner k3s-agent-2 public IP
> - `storagebox_host` — Storage Box hostname
> - `storagebox_user` — Storage Box username
> - `storagebox_port` — Storage Box SSH port

#### `manifests/secret.yaml`
Copy from Vaultwarden → **"Secret.yml"**
Create at: `manifests/secret.yaml`

> Contains Base64-encoded production credentials for Django and PostgreSQL:
> - `SECRET_KEY`
> - `DB_NAME`
> - `DB_USER`
> - `DB_PASSWORD`

#### `~/.job-tracker-secrets/storagebox_key`
Copy from Vaultwarden → **"Clave k3s-server - Storage"**
Create the directory and file:

```bash
mkdir -p ~/.job-tracker-secrets
# paste the private key content into the file
nano ~/.job-tracker-secrets/storagebox_key
chmod 600 ~/.job-tracker-secrets/storagebox_key
```

> SSH private key to connect to the Hetzner Storage Box for backups.
> Must be outside the repo — SSH keys never live inside a project directory.

### Run provisioning

```bash
ansible-playbook -i ansible/inventory-provision.ini ansible/provision.yml --ask-vault-pass
```

---

## Quick reference — where does each secret live?

| File | Location | In Git | Source |
|---|---|---|---|
| `backend/.env` | `backend/.env` | ❌ | Vaultwarden → ".env job-tracker" |
| `provision_secrets.yml` | `ansible/vars/provision_secrets.yml` | ❌ | Vaultwarden → "provision_secrets.yml" |
| `secret.yaml` | `manifests/secret.yaml` | ❌ | Vaultwarden → "Secret.yml" |
| `storagebox_key` | `~/.job-tracker-secrets/storagebox_key` | ❌ | Vaultwarden → "Clave k3s-server - Storage" |
