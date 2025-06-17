# 🧑‍💼 Job Board API

A Flask-based job board API that allows users to register, login, post jobs, apply for jobs, and manage applications. Built with Flask, SQLAlchemy, and Flask-Login.

## 🔧 Features

- User registration and login with password hashing
- Role-based access (`employer`, `applicant`)
- Employers can post and delete job listings
- Applicants can apply for jobs
- Users can view job listings and application status
- Flask-Login for session management
- SQLite database integration

## 🛠️ Tech Stack

- **Backend:** Flask
- **Database:** SQLite + SQLAlchemy
- **Authentication:** Flask-Login
- **Password Security:** Werkzeug (`generate_password_hash`, `check_password_hash`)
- **Testing:** Postman

## 📬 API Endpoints
## 🔐 Auth
| Method | Endpoint     | Description              |
| ------ | ------------ | ------------------------ |
| POST   | `/register/` | Register a new user      |
| POST   | `/login/`    | Login and create session |
| GET    | `/logout/`   | Logout the current user  |

## 📄 Job Management
| Method | Endpoint           | Description                 |
| ------ | ------------------ | --------------------------- |
| POST   | `/job/`            | Post a new job *(employer)* |
| GET    | `/get_job/`        | View all jobs               |
| GET    | `/single_job/<id>` | View a specific job         |
| DELETE | `/delete_job/<id>` | Delete a job *(employer)*   |


## 📝 Application Management
| Method | Endpoint                   | Description                   |
| ------ | -------------------------- | ----------------------------- |
| POST   | `/application/`            | Apply for a job *(applicant)* |
| GET    | `/get_application/`        | View all applications         |
| GET    | `/single_application/<id>` | View one application          |
| DELETE | `/delete_application/<id>` | Delete an application         |


## 🧪 Sample Postman Requests
- Register
POST /register/
{
  "username": "johndoe",
  "password": "secret123",
  "role": "employer"
 } 

- Login
POST /login/
{
  "username": "johndoe",
  "password": "secret123"
}


- Post Job
POST /job/
{
  "title": "Software Engineer",
  "description": "Build APIs and features",
  "location": "Remote",
  "company": "TechCorp"
}

- Apply for Job
POST /application/
{
  "user_id": 2,
  "job_id": 1,
  "status": "Applied"
}
