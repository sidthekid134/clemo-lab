# Placeholder API

A FastAPI application implementing a placeholder service with SQLModel for database operations.

## Features

- RESTful API with CRUD operations for placeholder data
- SQLModel for ORM and data validation
- FastAPI for API creation with automatic documentation
- Database integration with migration support

## Installation

1. Clone the repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## Running the application

```bash
python run.py
```

The API will be available at http://localhost:8000

API documentation is available at:
- http://localhost:8000/docs
- http://localhost:8000/redoc

## API Endpoints

- `GET /placeholders`: List all placeholders
- `POST /placeholders`: Create a new placeholder
- `GET /placeholders/{id}`: Get a specific placeholder
- `PUT /placeholders/{id}`: Update a placeholder
- `DELETE /placeholders/{id}`: Delete a placeholder

## Testing

Run tests using pytest:

```bash
pytest
```