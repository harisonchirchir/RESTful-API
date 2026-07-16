# RESTful API - Library Management System

A secure, tested RESTful API built with Django and Django REST Framework. This project demonstrates best practices for building production-ready APIs with authentication, permissions, and proper data validation.

## Overview

This is a library management system API that allows authenticated users to manage a personal collection of books and view available authors. The API provides endpoints for creating, reading, updating, and deleting books, as well as managing author information.

## Stack

- **Language:** Python
- **Framework:** Django 5.1.0 + Django REST Framework 3.15.0
- **Database:** SQLite (development)
- **Authentication:** Token-based authentication
- **Validation:** Pydantic 2.0.0

## Project Structure

```
RESTful-API/
├── manage.py                    # Django command-line utility
├── requirements.txt             # Project dependencies
├── db.sqlite3                   # SQLite database
├── library_project/
│   ├── settings.py             # Django configuration
│   ├── urls.py                 # Main URL routing
│   ├── wsgi.py                 # WSGI application
│   └── asgi.py                 # ASGI application
└── books/
    ├── models.py               # Database models (Author, Book)
    ├── views.py                # API views and endpoints
    ├── serializers.py          # DRF serializers
    ├── urls.py                 # Books app URL routing
    └── admin.py                # Django admin configuration
```

## Models

### Author
- `name` (CharField, max_length=200)
- `biography` (TextField, optional)

### Book
- `title` (CharField, max_length=200)
- `author` (ForeignKey to Author)
- `owner` (ForeignKey to User) - Links book to authenticated user
- `is_read` (BooleanField, default=False)

## API Endpoints

### Books
- `GET /api/books/` - List all books for authenticated user
  - Query parameter: `is_read=true|false` to filter by read status
- `POST /api/books/` - Create a new book
- `GET /api/books/{id}/` - Retrieve a specific book
- `PUT /api/books/{id}/` - Update a book
- `DELETE /api/books/{id}/` - Delete a book

### Authors
- `GET /api/authors/` - List all authors
- `POST /api/authors/` - Create a new author

### Authentication
- `POST /api-token-auth/` - Obtain authentication token

## Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/harisonchirchir/RESTful-API.git
cd RESTful-API
```

### 2. Create Virtual Environment
```bash
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Apply Migrations
```bash
python manage.py migrate
```

### 5. Create Superuser
```bash
python manage.py createsuperuser
```

### 6. Run Development Server
```bash
python manage.py runserver
```

The API will be available at `http://localhost:8000/`

## Authentication

The API uses **Token Authentication**. To authenticate:

1. Get your token:
```bash
curl -X POST http://localhost:8000/api-token-auth/ \
  -H "Content-Type: application/json" \
  -d '{"username": "your_username", "password": "your_password"}'
```

2. Include the token in subsequent requests:
```bash
curl -H "Authorization: Token YOUR_TOKEN_HERE" \
  http://localhost:8000/api/books/
```

## Example Usage

### Create a Book
```bash
curl -X POST http://localhost:8000/api/books/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Django for Beginners",
    "author_id": 1,
    "is_read": false
  }'
```

### List Your Books
```bash
curl -H "Authorization: Token YOUR_TOKEN" \
  http://localhost:8000/api/books/
```

### Filter Books by Read Status
```bash
curl -H "Authorization: Token YOUR_TOKEN" \
  'http://localhost:8000/api/books/?is_read=true'
```

### Create an Author
```bash
curl -X POST http://localhost:8000/api/authors/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "William Martin",
    "biography": "Software architect and author"
  }'
```

## Security Features

- Token-based authentication
- User-specific data isolation (books are filtered by owner)
- Default permission requires authentication
- Django built-in password validation
- CSRF protection middleware
- Session authentication fallback

## Configuration Details

### REST Framework Settings
- Authentication: TokenAuthentication + SessionAuthentication
- Default permission: IsAuthenticated
- All endpoints require authentication by default

### Database
- Development database: SQLite (db.sqlite3)
- For production, configure PostgreSQL or MySQL in settings.py

### Settings Security Notes
- `SECRET_KEY` should be moved to environment variables for production
- `DEBUG` should be set to `False` for production
- `ALLOWED_HOSTS` should be configured appropriately for production

## Development

### Admin Interface
Access Django admin at `http://localhost:8000/admin/` with your superuser credentials.

### Database Shell
```bash
python manage.py shell
```

### Create Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

## Project Features

✓ Token-based API authentication
✓ User-owned resource management
✓ Author and Book data models
✓ Filtering capabilities (books by read status)
✓ Proper HTTP status codes
✓ DRF serializers for data validation
✓ Class-based views for clean architecture
✓ Database relationships and constraints

## License

MIT License - See repository for details

## Topics

- Django
- Django REST Framework
- REST API
- Backend Development
