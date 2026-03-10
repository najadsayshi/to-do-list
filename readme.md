# 📝 FastAPI Todo API

A simple **Todo REST API** built with **FastAPI, SQLModel, and JWT Authentication**.
This project allows users to **sign up, log in, and manage their personal todo tasks** securely.

---

## 🚀 Features

* User Authentication (Signup & Login)
* JWT Token-based Authorization
* Create Todos
* View User-specific Todos
* Update Todos
* Delete Todos
* Secure routes using Bearer Token
* CORS enabled for frontend integration

---

## 🛠️ Tech Stack

* **FastAPI** – Backend framework
* **SQLModel** – ORM for database models
* **SQLite / SQLAlchemy Engine** – Database
* **JWT Authentication** – Secure API access
* **Python** – Programming language

---

## 📂 Project Structure

```
.
├── main.py          # FastAPI application
├── models.py        # Database models & schemas
├── auth.py          # JWT token creation & verification
├── db.py            # Database connection
├── requirements.txt # Project dependencies
└── README.md
```

---

## ⚙️ Installation

Clone the repository:

```
git clone https://github.com/yourusername/fastapi-todo-api.git
```

Navigate into the project folder:

```
cd fastapi-todo-api
```

Create a virtual environment:

```
python -m venv venv
```

Activate the virtual environment:

**Windows**

```
venv\Scripts\activate
```

**Mac / Linux**

```
source venv/bin/activate
```

Install dependencies:

```
pip install -r requirements.txt
```

---

## ▶️ Running the Server

Start the FastAPI server with:

```
uvicorn main:app --reload
```

Server will run at:

```
http://127.0.0.1:8000
```

---

## 📖 API Documentation

FastAPI automatically generates interactive API docs.

Swagger UI:

```
http://127.0.0.1:8000/docs
```

ReDoc:

```
http://127.0.0.1:8000/redoc
```

---

## 🔐 Authentication Flow

1️⃣ User signs up
2️⃣ User logs in
3️⃣ Server returns **JWT access token**
4️⃣ Token must be sent in request headers

Example header:

```
Authorization: Bearer <your_token>
```

---

## 📌 API Endpoints

### Auth

| Method | Endpoint  | Description             |
| ------ | --------- | ----------------------- |
| POST   | `/signup` | Register new user       |
| POST   | `/login`  | Login and receive token |

---

### Todos

| Method | Endpoint           | Description        |
| ------ | ------------------ | ------------------ |
| GET    | `/todos`           | Get all user todos |
| POST   | `/todos`           | Create new todo    |
| PATCH  | `/todos/{todo_id}` | Update todo        |
| DELETE | `/todos/{todo_id}` | Delete todo        |

---

## 🧾 Example Todo JSON

```
{
  "description": "Finish FastAPI project",
  "due_date": "2026-03-15",
  "priority": "high"
}
```

---

## 🔒 Protected Routes

The following routes require authentication:

* `/todos`
* `/todos/{todo_id}`

You must provide a **valid JWT token** in the request header.

---

## 📌 Future Improvements

* Password hashing (bcrypt) ,i didnt do this now bc i forget passwords for testing 😭
* Refresh tokens
* Pagination for todos
* User profile management
* Docker support
* Deployment (Render / Railway / AWS)

---

## 👨‍💻 Author

Built with ❤️ by Najad using **FastAPI**

---

## ⭐ Support

If you like this project, please **star the repository** ⭐ on GitHub.
