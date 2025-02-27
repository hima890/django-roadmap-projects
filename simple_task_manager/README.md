# Simple Task Manager API

This is a simple task manager API built with Django and Django REST framework. It allows users to create, read, update, and delete tasks.

## Features

- Create a new task
- Retrieve all tasks
- Update an existing task
- Delete a task

## Requirements

- Python 3.12
- Django
- Django REST framework

## Installation

1. Clone the repository:

```bash
git clone https://github.com/hima890/django-roadmap-projects.git
cd simple_task_manager
```

2. Create and activate a virtual environment:
django-roadmap-projects
```bash
python3 -m venv env
source env/bin/activate
```

3. Install the required packages:

```bash
pip install -r requirements.txt
```

4. Apply migrations:

```bash
python3 

manage.py

 migrate
```

5. Create a superuser:

```bash
python3 

manage.py

 createsuperuser
```

6. Run the development server:

```bash
python3 

manage.py

 runserver
```

## API Endpoints

### Create a Task

- **URL:** `/api/tasks/`
- **Method:** `POST`
- **Request Body:**

  ```json
  {
    "title": "New Task",
    "description": "This is a new task"
  }
  ```

- **Response:**

  ```json
  {
    "message": "New task has been added",
    "data": {
      "Task": "New Task",
      "Description": "This is a new task"
    }
  }
  ```

### Retrieve All Tasks

- **URL:** `/api/tasks/`
- **Method:** `GET`
- **Response:**

  ```json
  {
    "message": "API Overview",
    "data": [
      {
        "id": 1,
        "title": "Task 1",
        "description": "This is task 1"
      },
      ...
    ]
  }
  ```

### Update a Task

- **URL:** `/api/tasks/`
- **Method:** `PUT`
- **Request Body:**

  ```json
  {
    "id": 1,
    "title": "Updated Task",
    "description": "This is an updated task"
  }
  ```

- **Response:**

  ```json
  {
    "message": "Task has been updated",
    "data": {
      "Task": "Updated Task",
      "Description": "This is an updated task"
    }
  }
  ```

### Delete a Task

- **URL:** `/api/tasks/`
- **Method:** `DELETE`
- **Request Body:**

  ```json
  {
    "id": 1
  }
  ```

- **Response:**

  ```json
  {
    "message": "Task has been deleted"
  }
  ```

## Running Tests

To run the tests, use the following command:

```bash
python3 

manage.py

 test
```

## License

This project is licensed under the MIT License.
