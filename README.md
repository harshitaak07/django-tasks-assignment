# Django Task Management System

A RESTful Task Management System built with Django and Django REST Framework that supports full CRUD operations.

## By Harshitaa Kashyap

- Name: Harshitaa Kashyap
- Email: harshitaakashyap@gmail.com

## Overview

This project implements a RESTful API for managing tasks with the following features:

- Create tasks with title and description
- List all tasks with sorting and filtering options
- Update existing tasks
- Delete tasks

## Installation

1. Clone the repository

```bash
git clone https://gitlab.com/your-username/django-tasks-assignment.git
cd django-tasks-assignment
```

2. Create and activate a virtual environment

```bash
python -m venv venv
source venv/bin/activate  # For Linux/Mac
venv/bin/activate     # For Windows
```

3. Install the required dependencies

```bash
pip install -r requirements.txt
```

4. Define a `.env` file at the project root with the following:

```
SECRET_KEY=<SECRET_KEY>
DEBUG=True
DATABASE_URL=<DATABASE_URL>
REDIS_URL=<REDIS_URL> (Rate limit uses local memory cache; tests use Redis.)
```

5. Run migrations

```bash
python manage.py migrate
```

6. Start the development server

```bash
python manage.py runserver
```

## API Endpoints

### Task Management

| Method | Endpoint                         | Description                                  |
| ------ | -------------------------------- | -------------------------------------------- |
| POST   | `/tasks/`                        | Create a new task with title and description |
| GET    | `/tasks/`                        | List all tasks                               |
| GET    | `/tasks/?sort_by_date=true`      | List all tasks sorted by date                |
| GET    | `/tasks/?search_date=YYYY-MM-DD` | Search tasks by date                         |
| GET    | `/tasks/?search=title`           | Search tasks by title                        |
| PATCH  | `/tasks/{id}/`                   | Update a specific task                       |
| DELETE | `/tasks/{id}/`                   | Delete a specific task                       |

## Usage Examples

### Creating a Task

**POST** http://localhost:8000/tasks/

```json body
{
  "id": 1,
  "title": "Sample Task",
  "description": "This is a sample task",
  "created_at": "2025-04-25T12:00:00Z"
}
```

### Listing All Tasks

**GET** http:/url/tasks/

### Searching Tasks by Title

**GET** http:/url/tasks/?search=Sample

### Sorting Tasks by Date

**GET** http:/url/tasks/?sort_by_date=true

### Filtering Tasks by Date Range

**GET** http:/url/tasks/?search_date=YYYY-MM-DD

### Updating a Task

**PATCH** http:/url/tasks/id/

```
json body
{
  "title": "Updated Task Title"
  "description": "Updated Task Description"
  "status": "Updated Task Status"
  "due_date": "Updated Task Due Date"
  "priority": "Updated Task Priority"
}
```

### Deleting a Task

**DELETE** http:/url/tasks/id/

## Implementation Details

### Models

Base Model
The project uses an abstract base model to handle common fields across all models:

- id (AutoField)
- created_at (DateTimeField)
- updated_at (DateTimeField)

Task Model
The Task model inherits from BaseModel and includes:

- title (CharField)
- description (TextField)
- created_at (DateTimeField)
- updated_at (DateTimeField)
- status (Enumeration field: Pending and Completed)
- due_date (DateTimeField)
- priority (IntegerField)

### Serializers

TaskSerializer handles:

- Validation of input data
- Proper representation of Task objects in API responses

### Views

The project uses Django REST Framework ViewSets to implement:

- TaskViewSet - Handles all CRUD operations for tasks

### Filtering and Sorting

Custom filter backends implement:

- Title search functionality
- Date search functionality
- Date-based sorting

## Running Tests

```bash
python manage.py test tasks.tests.folder_name.file_name
```

### Test Coverage

- Unit tests for models, serializers and views
- Integration tests for API endpoints
- Edge case handling for validation and error responses

## Additional Features

- Pagination for list views
- Fuzzy Search via pg_trgm extension
- Rate limiting implemented for delete and patch API endpoints
- Proper Error Handling, Logging and status codes
- Solid Principles of Clean Architecture

## Running the Application with Docker

- Build the Docker image: docker build.
- Build and start the containers: docker-compose up --build
- Apply database migrations: docker-compose exec web python manage.py migrate
- Access the application: http://localhost:8000/
- Stop the containers: docker-compose down
