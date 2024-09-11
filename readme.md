
# OneFin Backend Assignment

## Overview

This assignment has Django-based API that allows users to manage collections of movies. It supports user registration, movie management, and collection management with various CRUD (Create, Read, Update, Delete) operations. Additionally, it provides endpoints to monitor and reset request counts.

## Endpoints

| Method | Endpoint                              | Description                                     |
|--------|---------------------------------------|-------------------------------------------------|
| POST   | `/register/`                          | Register a new user                             |
| GET    | `/movies/`                            | Retrieve a list of movies                       |
| GET    | `/collection/`                        | Retrieve a list of movie collections            |
| POST   | `/collection/`                        | Create a new movie collection                   |
| GET    | `/collection/<uuid:collection_uuid>/` | Retrieve a specific collection by UUID          |
| PUT    | `/collection/<uuid:collection_uuid>/` | Update a specific collection by UUID            |
| DELETE | `/collection/<uuid:collection_uuid>/` | Delete a specific collection by UUID            |
| GET    | `/request-count/`                     | Retrieve the current request count              |
| POST   | `/request-count/reset/`               | Reset the request count                         |

## Setup

### Prerequisites

- Python 3.x
- Django 4.x
- Django REST Framework (if using)

### How to Run the Project

1. **Clone the repository:**

    ```bash
    git clone git@github.com:adarshpand3y/OneFin-backend-assignment.git
    ```

2. **Navigate to the project directory:**

    ```bash
    cd OneFin-backend-assignment
    ```

3. **Create a virtual environment and activate it:**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

4. **Install the required packages:**

    ```bash
    pip install -r requirements.txt
    ```

5. **Run migrations:**

    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

6. **Start the redis server on port :**
    
    Make sure that the Redis server is up and running on port 6379. You can start Redis with the following command:

    ```bash
    redis-server --port 6379
    ```

7. **Start the development server:**

    ```bash
    python manage.py runserver
    ```

## Testing

To run tests, use the following command:

```bash
python manage.py test
