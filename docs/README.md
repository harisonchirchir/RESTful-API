# RESTful API - Library Management System

A Django REST Framework API for managing authors and personal book collections.
Clients authenticate with DRF token authentication. Each user can view and
manage only their own books; authors are shared across users.

## Layout

```
docs/         Documentation (this file, LICENSE)
backend/      Django project: manage.py, library_project/, books/, requirements.txt
frontend/     Client-side app (not yet implemented)
```

## Stack

- Python 3.12 (see `.python-version`)
- Django 5.1+
- Django REST Framework 3.15+
- SQLite
- Token and session authentication
- WhiteNoise + Gunicorn for production static serving

## Quick start

```bash
cd backend
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Then visit `http://127.0.0.1:8000/admin` (admin) or `http://127.0.0.1:8000/api/` (API).

## API endpoints

| Method | Path                  | Auth      | Description                          |
|--------|-----------------------|-----------|--------------------------------------|
| POST   | `/api/register/`      | none      | Create user + return token           |
| POST   | `/api/login/`         | none      | Login existing user + return token  |
| GET    | `/api/authors/`       | token     | List authors                         |
| POST   | `/api/authors/`       | token     | Create author                        |
| GET    | `/api/books/`         | token     | List your books (?is_read=true)     |
| POST   | `/api/books/`         | token     | Create book                          |
| GET    | `/api/books/{id}/`    | token     | Get book detail                      |
| PUT    | `/api/books/{id}/`    | token     | Update book                          |
| DELETE | `/api/books/{id}/`    | token     | Delete book                          |

## Usage examples

```bash
# Register (returns token)
curl -X POST -H "Content-Type: application/json" \
  -d '{"username":"alice","password":"secret123"}' \
  http://127.0.0.1:8000/api/register/

# Login existing user
curl -X POST -H "Content-Type: application/json" \
  -d '{"username":"alice","password":"secret123"}' \
  http://127.0.0.1:8000/api/login/

# Add a book (replace <TOKEN>)
curl -X POST -H "Authorization: Token <TOKEN>" -H "Content-Type: application/json" \
  -d '{"title":"Dune","author_id":1,"is_read":false}' \
  http://127.0.0.1:8000/api/books/

# Delete a book
curl -X DELETE -H "Authorization: Token <TOKEN>" \
  http://127.0.0.1:8000/api/books/1/
```

## Tests

```bash
cd backend
python manage.py test
```

## Production deployment

### Python version
Tested on **Python 3.12** (see `.python-version`). Django 5.1.x is
incompatible with Python 3.14 — its template context copy logic raises
`AttributeError: 'super' object has no attribute 'dicts'`. Run on a supported
interpreter (3.10–3.13); the runtime shim in
`backend/library_project/settings.py` is a no-op there.

### Static files
WhiteNoise collects and serves static assets into `STATIC_ROOT`.

```bash
cd backend
pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py migrate
gunicorn library_project.wsgi:application --bind 0.0.0.0:8000
```

Set `DEBUG=False` in `backend/.env` for production.
