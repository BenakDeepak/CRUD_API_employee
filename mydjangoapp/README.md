# CRUD API for Employee Management

## Overview
This project is a **CRUD API** for employee management using **FastAPI** and **Django ORM**. It allows users to perform operations such as creating, reading, updating, and deleting employee records stored in a database. The project also supports CSV-based bulk import of employee data.

## Installation

### Steps to Install
1. Clone the repository:
   ```bash
   git clone https://github.com/benakdeepak.git
   ```
2. Create a virtual environment:
   ```bash
   python -m venv env
   env\Scripts\activate
   
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run database migrations:
   ```bash
   python manage.py migrate
   ```

## Running the Application
Start the FastAPI server using Uvicorn:
```bash
uvicorn fastapi_app:app --host 0.0.0.0 --port 8000 --reload
```

## API Endpoints
| Method | Endpoint             | Description                |
|--------|----------------------|----------------------------|
| GET    | `/employees`         | Get all employees          |
| GET    | `/employees/{id}`    | Get employee by ID         |
| POST   | `/employees`         | Create a new employee      |
| PUT    | `/employees/{id}`    | Update employee by ID      |
| DELETE | `/employees/{id}`    | Delete employee by ID      |
