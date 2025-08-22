# clean_crm — CRM Django/DRF (Clean Architecture + OTP + Import/Export + Campagnes)

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)]()
[![Django](https://img.shields.io/badge/Django-5.x-success.svg)]()
[![DRF](https://img.shields.io/badge/DRF-3.15+-red.svg)]()
[![Celery](https://img.shields.io/badge/Celery-5.x-green.svg)]()
[![Redis](https://img.shields.io/badge/Redis-≥5-orange.svg)]()
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)]()

> **Repository**: https://github.com/daniel10027/clean_crm

## 🧠 Idée & Positionnement

**clean_crm** est un CRM minimaliste mais **production-ready** qui démontre une architecture **Clean/DDD** avec **Django REST Framework** :
- Authentification **JWT** (login/register), **réinitialisation de mot de passe par OTP**,
- Gestion de **répertoires (directories)** et **contacts**,
- **Import** de contacts (Excel/CSV) et **export** (CSV/Excel/PDF),
- **Campagnes** multicanales (**Email / SMS / WhatsApp**) avec **envoi asynchrone Celery**,
- **Documentation d’API** via **Swagger** et **ReDoc**.

L’objectif : un socle clair, modulaire et extensible (multi-tenant, RBAC, planification, intégrations Twilio/Meta, etc.).

---

## ✅ Fonctionnalités implémentées

- **Auth & Sécurité**
  - Register / Login (**JWT** via SimpleJWT)
  - **Password reset** avec **OTP** (génération, validation, expiration)
- **Directories & Contacts**
  - CRUD répertoires
  - CRUD contacts
  - **Import** contacts depuis **CSV/XLSX** (pandas/openpyxl)
  - **Export** contacts en **CSV/XLSX/PDF** (pandas/reportlab)
- **Campagnes**
  - Modèle de campagne (**email/sms/whatsapp**)
  - **Mise en file (queue)** des livraisons vers tous les contacts d’un directory
  - **Envoi asynchrone** via **Celery** (Email Django / SMS & WhatsApp en console)
- **Docs API**
  - Schéma OpenAPI, **Swagger UI** et **ReDoc** (drf-spectacular)
- **Architecture**
  - DDD : `domain/`, `application/`, `infrastructure/`, `interfaces/`
  - Use Cases, DTOs, Repositories, Services
- **Divers**
  - Pagination DRF standard
  - Admin minimal (debug)

---

## 🛣️ Roadmap (À faire / Idées d’évolution)

- **Envois réels** : intégrer **Twilio** (SMS) et **Meta WhatsApp Business** (webhook + templates)
- **Planification des campagnes** : ETA/CRON Celery, récurrence, fenêtres d’envoi
- **Multi-tenant** (Organizations), **RBAC** (rôles/permissions fines)
- **Segmentation/Tags** des contacts, listes dynamiques
- **Rapports d’import** (fichiers volumineux en tâche Celery, suivi & erreurs)
- **Suivi de délivrabilité** (statuts, retries, dead-letter queue, idempotence)
- **Tests** étendus (use cases, tasks, vues), CI (GitHub Actions), coverage
- **Durcissement sécurité** : throttling DRF, CORS/CSRF, rules de mot de passe avancées
- **Observabilité** : structlog, Sentry, métriques Celery/Prometheus

---

## 🏗️ Architecture & Arborescence

**Pattern** : Clean/DDD (séparation claire des responsabilités)
- `domain/` : entités, contrats (repositories/services)
- `application/` : **Use Cases** + **DTOs** (logique métier orchestrée)
- `infrastructure/` : **models Django**, implémentations de repos/services
- `interfaces/` : **serializers**, **views/routers DRF**, endpoints

```text
app/
  settings.py, urls.py, celery.py
accounts/
  domain/ (entities, repositories)
  application/ (use_cases.py, dto.py)
  infrastructure/ (models.py, repositories_impl.py)
  interfaces/ (serializers.py, views.py, routers.py)
directory/
  domain/  application/
  infrastructure/ (models.py)
  interfaces/ (serializers.py, views.py, routers.py)
contacts/
  domain/  application/ (use_cases.py - import/export)
  infrastructure/ (models.py)
  interfaces/ (serializers.py, views.py, routers.py)
campaigns/
  domain/ (entities.py)
  application/ (use_cases.py - create, queue + Celery task)
  infrastructure/ (models.py)
  interfaces/ (serializers.py, views.py, routers.py)
notifications/
  domain/ (services protocols)
  infrastructure/ (email_impl.py, console_sms.py, console_whatsapp.py)
common/
  pagination.py, utils.py
````

---

## ⚙️ Prérequis

* **Python** 3.11+
* **Redis** (broker/back-end Celery)
* **PostgreSQL** (recommandé) ou SQLite (dev)
* Optionnel dev: serveur SMTP local (ex. `python -m smtpd ...` ou MailHog)

---

## 🚀 Installation & Démarrage (Local)

```bash
git clone https://github.com/daniel10027/clean_crm.git
cd clean_crm
python -m venv .venv && source .venv/bin/activate

# Dépendances
pip install -r requirements.txt
```

Créer le fichier **`.env`** à la racine :

```env
DJANGO_DEBUG=True
DJANGO_SECRET_KEY=dev-secret-change-me
DJANGO_ALLOWED_HOSTS=*

# SQLite par défaut ; pour Postgres, mettre une DATABASE_URL adaptée
DATABASE_URL=sqlite:///db.sqlite3

# Email dev
EMAIL_HOST=localhost
EMAIL_PORT=1025
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=
EMAIL_USE_TLS=False
DEFAULT_FROM_EMAIL=no-reply@crm.local

# Celery/Redis
REDIS_URL=redis://localhost:6379/0

# JWT
ACCESS_TOKEN_LIFETIME_MIN=60
REFRESH_TOKEN_LIFETIME_DAYS=7

# Senders (placeholders)
SMS_PROVIDER=console
WHATSAPP_PROVIDER=console
```

Initialiser la base et lancer :

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser

# SMTP de debug (optionnel)
python -m smtpd -c DebuggingServer -n localhost:1025

# Serveur Django
python manage.py runserver

# Worker Celery (dans un autre terminal)
celery -A app worker -l info
```

**Documentation API :**

* Swagger: `http://127.0.0.1:8000/api/docs/`
* ReDoc: `http://127.0.0.1:8000/api/redoc/`
* OpenAPI schema: `/api/schema/`

---

## 🐳 (Optionnel) Docker Compose de dev

Crée un `docker-compose.yml` :

```yaml
version: "3.9"
services:
  web:
    build: .
    command: sh -c "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"
    ports: ["8000:8000"]
    env_file: .env
    depends_on: [redis]
    volumes: [".:/app"]

  worker:
    build: .
    command: celery -A app worker -l info
    env_file: .env
    depends_on: [web, redis]
    volumes: [".:/app"]

  redis:
    image: redis:7
    ports: ["6379:6379"]

  mailhog:
    image: mailhog/mailhog
    ports:
      - "1025:1025"
      - "8025:8025"
```

> Fournis un `Dockerfile` (Python 3.11-slim) si besoin, ou lance directement en local comme décrit plus haut.

---

## 🔐 Auth & OTP — Endpoints clés

* `POST /api/accounts/register/` → `{ email, username, password }`
* `POST /api/accounts/login/` → `{ username, password }` → JWT
* `POST /api/accounts/token/refresh/` → `{ refresh }`
* `POST /api/accounts/password/reset/request/` → `{ email }` (génère OTP)
* `POST /api/accounts/password/reset/confirm/` → `{ user_id, code, new_password }`

**Header protégé :** `Authorization: Bearer <ACCESS_TOKEN>`

---

## 📇 Directories & Contacts — Endpoints clés

* **Directories**

  * `POST /api/directory/directories/` → `{ name }` (owner injecté)
  * `GET /api/directory/directories/`
  * `PUT/PATCH /api/directory/directories/{id}/`

* **Contacts**

  * `GET /api/contacts/contacts/?directory=<id>`
  * `POST /api/contacts/contacts/` → `{ directory, first_name, last_name, email, phone, extra? }`
  * `PUT/PATCH /api/contacts/contacts/{id}/`
  * **Import** : `POST /api/contacts/contacts/import/` (multipart)

    * `directory_id=<id>`, `file=<contacts.xlsx|contacts.csv>`
    * Colonnes attendues : `first_name,last_name,email,phone`
  * **Export** : `GET /api/contacts/contacts/export/?directory_id=<id>&format=csv|xlsx|pdf`

---

## 📣 Campagnes — Endpoints clés

* `POST /api/campaigns/campaigns/`

  ```json
  { "name":"Relance", "channel":"email|sms|whatsapp", "subject":"...", "body":"...", "directory": 3 }
  ```
* `POST /api/campaigns/campaigns/{id}/queue/` → crée des deliveries pour les contacts du directory, lance **Celery**
* `GET /api/campaigns/deliveries/` (statuts: `pending|sent|failed`)

**Email** : envoi via backend Django.
**SMS / WhatsApp** : implémentations **console** par défaut (remplacer par Twilio/Meta).

---

## 🔎 Exemples `curl`

```bash
# Register
curl -X POST http://127.0.0.1:8000/api/accounts/register/ \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","username":"john","password":"Passw0rd!"}'

# Login
curl -X POST http://127.0.0.1:8000/api/accounts/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"john","password":"Passw0rd!"}'
# -> récupère ACCESS_TOKEN

# Créer directory
curl -X POST http://127.0.0.1:8000/api/directory/directories/ \
  -H "Authorization: Bearer <ACCESS_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"name":"Prospects 2025"}'

# Import contacts (multipart)
curl -X POST http://127.0.0.1:8000/api/contacts/contacts/import/ \
  -H "Authorization: Bearer <ACCESS_TOKEN>" \
  -F "directory_id=1" -F "file=@contacts.xlsx"

# Export contacts (CSV)
curl -X GET "http://127.0.0.1:8000/api/contacts/contacts/export/?directory_id=1&format=csv" \
  -H "Authorization: Bearer <ACCESS_TOKEN>" -OJ

# Créer + queue campagne
curl -X POST http://127.0.0.1:8000/api/campaigns/campaigns/ \
  -H "Authorization: Bearer <ACCESS_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"name":"Relance Septembre","channel":"email","subject":"Promo","body":"-20% cette semaine","directory":1}'

curl -X POST http://127.0.0.1:8000/api/campaigns/campaigns/1/queue/ \
  -H "Authorization: Bearer <ACCESS_TOKEN>"
```

---

## 🧪 Tests

* Exemple minimal fourni pour l’auth (`accounts/tests/test_auth.py`).
* Lancer :

  ```bash
  python manage.py test
  ```
* À prévoir : tests pour **use cases**, **tasks Celery**, **vues DRF**, imports/exports et cas d’erreurs (OTP expiré, delivery échoué, etc.).

---

## 🔒 Sécurité & Bonnes pratiques

* JWT avec durées configurables (`.env`)
* OTP 6 chiffres, TTL configurable (par défaut 10min dans le modèle)
* **À ajouter** : rate limiting (DRF throttling), CORS/CSRF selon front, durcissement mots de passe, audit logs

---

## 📈 Scalabilité & Observabilité

* **Celery** pour les envois asynchrones / batch
* Batching & retries (à améliorer), DLQ souhaitable
* Logs structurés, traçage, Sentry/Prometheus recommandés
* Optimiser import/export en streaming pour très gros fichiers

---

## 🤝 Contribuer

1. Fork & branch (`feat/...` / `fix/...`)
2. Respecter l’architecture (DDD, Use Cases, DTOs, Repos)
3. Ajouter des tests
4. PR avec description claire

---

## 📄 Licence

MIT — fais-en bon usage et n’hésite pas à proposer des améliorations ! 🎉# CleanCRM
