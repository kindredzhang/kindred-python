# Python Web Application

A simple web application built with Python, migrated from a Java Spring Boot project. This project demonstrates how to build a RESTful API using FastAPI and SQLAlchemy, following similar patterns to Spring Boot but with Python's simplicity.

## Key Features

- FastAPI for high-performance API development
- SQLAlchemy ORM for database operations
- PostgreSQL database
- Repository pattern implementation
- Pydantic models for data validation
- Automatic API documentation with Swagger UI

## Quick Start

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure database in `.env` file

3. Run development server:
```bash
./dev.sh start
```

4. Generate database models:
```bash
./dev.sh gen
```

## Project Structure

```
app/
├── api/            # API endpoints
├── models/         # SQLAlchemy models
├── repositories/   # Repository layer
├── schemas/        # Pydantic models
└── utils/          # Utility functions
```

## Development

- `./dev.sh start` - Start development server
- `./dev.sh gen` - Generate database models
- `./dev.sh help` - Show available commands