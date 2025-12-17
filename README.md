# Django API Project

This project implements an API for managing events and user registrations with asynchronous email notifications via
Celery + Redis.

---

## Table of Contents

- [Technologies](#technologies)
- [Repository Cloning](#repository-cloning)
- [Environment Setup](#environment-setup)
- [Running the Project](#running-the-project)
- [Docker](#docker)
- [Database Migrations & Superuser](#database-migrations--superuser)
- [API Endpoints](#api-endpoints)
- [Email Notifications](#email-notifications)
- [Celery + Redis](#celery--redis)

---

## Technologies

- Python 3.13
- Django 6.0
- Django REST Framework
- PostgreSQL
- Redis
- Celery
- Docker / Docker Compose

---

## Repository Cloning

```bash
git clone git@github.com:SydorchukOleksandr21/DjangoApi.git
cd DjangoApi
```

Environment Setup

Create a .env file based on env.example:

```bash
cp env.example .env
```

# Django API Project

## Environment Setup

Create a `.env` file based on `env.example`:

```
POSTGRES_DB=djangoapi_dev
POSTGRES_USER=django_user
POSTGRES_PASSWORD=StrongPass123
POSTGRES_HOST=db
POSTGRES_PORT=5432

DJANGO_SECRET_KEY=your-secret-key
DJANGO_DEBUG=1
```

Install Python dependencies (if needed outside Docker):

```bash
pip install -r requirements.txt
```

## Running the Project

### Using Docker Compose

```bash
docker-compose up --build
```

This command will start all required services:

* **Django API (web)** – the backend application
* **Celery worker** – for asynchronous tasks
* **PostgreSQL** – database
* **Redis** – message broker and cache

The web service is available at `http://localhost:8000/`.

## API Endpoints

| Endpoint                               | Method                 | Description                              |
|----------------------------------------|------------------------|------------------------------------------|
| `/api/events/`                         | GET, POST, PUT, DELETE | Manage events (CRUD)                     |
| `/api/registrations/`                  | GET, POST, PUT, DELETE | Manage event registrations               |
| `/api/users/`                          | GET, POST, PUT, DELETE | Manage users                             |
| `/api/events/{event_id}/registrations` | GET                    | Get all registrations for selected event |

**Notes:**

* Events endpoint supports pagination, filtering, and search.
* Registrations endpoint allows users to register for events and view their registrations.
* Event organizers can view all registrations for their events and delete odd users.

More information can be found at `/api/docs/`

## Email Notifications

* Users receive asynchronous email notifications upon successful event registration.
* Emails include event title, date, and location.
* Local development uses `console.EmailBackend` to display emails in the console.
* Celery ensures that email sending does not block API responses.

## Celery + Redis

* **Celery** is used for asynchronous task processing.
* **Redis** acts as the message broker and task result backend.

