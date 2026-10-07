# RESTful API - Library Management System

A Django REST Framework API for managing authors and personal book collections. Clients authenticate with DRF token authentication. Each user can view and manage only their own books; authors are shared across users.

## Stack

- Python
- Django 5.1+
- Django REST Framework 3.15+
- SQLite (configured database)
- Token and session authentication

## Project structure

```text
.
├── books/
│   ├── migrations/          # Database schema migrations
│   ├── models.py            # Author and Book models
│   ├── serializers.py       # API serialization and validation
│   ├── tests.py             # API tests
│   ├── urls.py              # Books app routes
│   └── views.py             # API views
├── library_project/
│   ├── settings.py          # Django and REST framework settings
│   └── urls.py              # Project routes
├── .env.example             # Example environment settings
├── manage.py
└── requirements.txt
```

## Data models

**Author** has a unique name, an optional biography, and creation/update timestamps.

**Book** has a title, a read status, creation/update timestamps, an owner, and an optional author. A user cannot have two books with the same title. Books are ordered newest first.

## Setup

```bash
git clone https://github.com/harisonchirchir/RESTful-API.git
cd RESTful-API
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Optionally copy `.env.example` to `.env` and set `SECRET_KEY`, `DEBUG`, and `ALLOWED_HOSTS` for your environment. The project uses SQLite.

Initialize the database and create an administrator:

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

The API is available at `http://localhost:8000/`. The root URL redirects to `/api/books/`.

## Authentication

All API endpoints require authentication. Obtain a token with a Django user's credentials:

```bash
curl -X POST http://localhost:8000/api-token-auth/ \
  -H "Content-Type: application/json" \
  -d '{"username":"your_username","password":"your_password"}'
```

Send the returned token on API requests:

```bash
curl http://localhost:8000/api/books/ \
  -H "Authorization: Token YOUR_TOKEN"
```

## API endpoints

| Method | Endpoint | Description |
| --- | --- | --- |
| `GET` | `/api/books/` | List the authenticated user's books |
| `POST` | `/api/books/` | Add a book to the authenticated user's collection |
| `GET` | `/api/books/{id}/` | Retrieve one of the user's books |
| `PUT` | `/api/books/{id}/` | Replace/update one of the user's books |
| `DELETE` | `/api/books/{id}/` | Delete one of the user's books |
| `GET` | `/api/authors/` | List authors |
| `POST` | `/api/authors/` | Create an author |

The book list accepts `is_read=true` or `is_read=false` as a query parameter, for example `/api/books/?is_read=true`. Book responses include nested author details. When creating or updating a book, provide `author_id` to select an author; `owner` is set from the authenticated user and cannot be supplied by the client.

## Examples

Create an author:

```bash
curl -X POST http://localhost:8000/api/authors/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name":"William Martin","biography":"Software architect and author"}'
```

Create a book (using an existing author's ID):

```bash
curl -X POST http://localhost:8000/api/books/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title":"Django for Beginners","author_id":1,"is_read":false}'
```

Filter your books:

```bash
curl "http://localhost:8000/api/books/?is_read=true" \
  -H "Authorization: Token YOUR_TOKEN"
```

## Development

Run the tests with:

```bash
python manage.py test
```

Create and apply model migrations with:

```bash
python manage.py makemigrations
python manage.py migrate
```

The Django admin is available at `/admin/` after creating a superuser.

## Configuration and deployment

The project defaults to development settings and SQLite. Before deployment, provide a secure `SECRET_KEY`, set `DEBUG=False`, configure `ALLOWED_HOSTS`, and choose an appropriately managed production database. Do not use the development settings as-is for a public deployment.

## License

MIT License. See [LICENSE](LICENSE).
