# event\_space 🌟

**event\_space** is a Django REST Framework-based project that provides an environment for users to create events and let others join them. It comes with JWT authentication, filtering capabilities, and comprehensive API documentation via Swagger and Redoc.

---

## 🚀 Features

- User registration and login using JWT tokens
- Create, update, retrieve, and list events
- Join or leave events
- Track your own events as a creator or participant
- Filtering, searching, and ordering on event list
- Fully documented with Swagger and Redoc

---

## 📂 Requirements

- Python 3.10+
- Django 5.1.7
- MySQL

### Python Dependencies

```bash
asgiref==3.8.1
cffi==1.17.1
cryptography==44.0.2
Django==5.1.7
django-filter==25.1
djangorestframework==3.15.2
djangorestframework_simplejwt==5.5.0
drf-yasg==1.21.10
inflection==0.5.1
mysqlclient==2.2.7
packaging==24.2
pycparser==2.22
PyJWT==2.9.0
pytz==2025.2
PyYAML==6.0.2
sqlparse==0.5.3
tzdata==2025.2
uritemplate==4.1.1
```

---

## 🚧 Installation

```bash
git clone https://github.com/caliber24/event_space.git
cd event_space
python -m venv env
source env/bin/activate  # On Windows use `env\Scripts\activate`
pip install -r requirements.txt
```

### Configure `.env` or `settings.py`

Set your MySQL DB credentials and secret keys appropriately.

### Run migrations:

```bash
python manage.py migrate
```

### Create superuser:

```bash
python manage.py createsuperuser
```

### Start the development server:

```bash
python manage.py runserver
```

Access the API at:

- Swagger UI: [http://localhost:8000/swagger/](http://localhost:8000/swagger/)
- Redoc: [http://localhost:8000/redoc/](http://localhost:8000/redoc/)

---

## 🔐 Authentication

JWT-based auth using `/auth/api/token/` and `/auth/api/token/refresh/`. Include the `Authorization: Bearer <access_token>` header for protected endpoints.

---

## 🔍 API Endpoints Overview

### ✉️ Auth

| Method | Endpoint                   | Description          |
| ------ | -------------------------- | -------------------- |
| POST   | `/auth/`                   | Register new user    |
| POST   | `/auth/api/token/`         | Obtain JWT token     |
| POST   | `/auth/api/token/refresh/` | Refresh access token |
| GET    | `/auth/<email>/`           | Retrieve user info   |
| PUT    | `/auth/<email>/`           | Update user info     |

### 🌐 Events

| Method | Endpoint                 | Description                 |
| ------ | ------------------------ | --------------------------- |
| GET    | `/event/`                | List all available events   |
| POST   | `/event/`                | Create a new event          |
| GET    | `/event/{id}/`           | Retrieve event details      |
| PUT    | `/event/{id}/`           | Update event info (partial) |
| POST   | `/event/{event_id}/join` | Join an event               |

### ✉️ User's Events

| Method | Endpoint                                  | Description                      |
| ------ | ----------------------------------------- | -------------------------------- |
| GET    | `/event/my-event-participant`             | List events user has joined      |
| DELETE | `/event/my-event-participant/{id}/remove` | Leave an event                   |
| GET    | `/event/my-event-create`                  | List events created by user      |
| GET    | `/event/my-event-create/{id}`             | Retrieve created event           |
| PUT    | `/event/my-event-create/{id}`             | Update status of a created event |

---

## 📄 Screenshot



---

## 📆 License

This project is open-source and available under the [MIT License](LICENSE).

---

## 🙋 Author

Created by **Caliber24**. Feel free to reach out or contribute!

