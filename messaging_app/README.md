# 📨 Messaging App (Django + Django REST Framework)

This project is a messaging system built with Django and Django REST Framework. It enables users to start conversations, send messages, and manage chat interactions via a RESTful API.

---

## 📌 Project Objectives

By completing this project, you will learn to:

- Scaffold a Django project using an industry-standard layout
- Define and implement scalable data models with Django ORM
- Establish one-to-one, one-to-many, and many-to-many relationships
- Build modular and clean Django apps
- Configure REST API routing using Django REST Framework
- Implement clean serializers with nested relationships
- Build maintainable APIs and test them using Postman or Swagger

---

## 🚀 Features

- User model extending Django’s `AbstractUser`
- UUID primary keys for all models
- Many-to-many relationships for conversations (multiple participants)
- Nested serialization of messages inside conversations
- Endpoints to:
  - List/create conversations
  - Send/list messages

---

## 🏗️ Tech Stack

- Python 3.10+
- Django 4.x
- Django REST Framework
- SQLite (default, can be replaced with PostgreSQL)
- Postman (for API testing)

---

## 🔧 Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/alx-backend-python.git
cd alx-backend-python/messaging_app
```

### 2. Set up vertual enviroment
```bash
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Start development server
```bash
python manage.py runserver
```

Visit http://127.0.0.1:8000/api/ to access the API.


---

## 🧪 API Endpoints

| Method | Endpoint	| Description |
|--|--|--|
| GET | /api/conversations/	| List all conversations |
| POST | /api/conversations/ |	Create a new conversation |
| GET | /api/messages/ | List all messages |
| POST | /api/messages/ | Send message to conversation |
