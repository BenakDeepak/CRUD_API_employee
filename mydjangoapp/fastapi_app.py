import os
import django

# Set up Django settings before importing models
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mydjangoapp.settings")
django.setup()

from employees.models import Employee  # Django ORM model import
from fastapi import FastAPI, HTTPException
import csv

import asyncio

async def startup_event():
    await load_csv_to_db()  # Call the async wrapped function

app = FastAPI(on_startup=[startup_event])

CSV_FILE = "employees.csv"


from django.db import IntegrityError
from asgiref.sync import sync_to_async

@sync_to_async
def load_csv_to_db():
    with open("employees.csv", "r") as file:
        reader = csv.reader(file)
        next(reader)  # Skip header row if present
        for row in reader:
            try:
                _, created = Employee.objects.get_or_create(
                    first_name=row[0],
                    last_name=row[1],
                    email=row[2],
                    age=row[3],
                    contact_number=row[4],
                    dob=row[5])
            except IntegrityError as e:
                print(f"Skipping duplicate entry: {e}")



def save_db_to_csv():
    """Save database employee records to a CSV file."""
    employees = Employee.objects.all().values(
        "first_name", "last_name", "email", "age", "contact_number", "dob"
    )

    with open(CSV_FILE, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["First", "Last", "Email", "Age", "ContactNumber", "DOB"])
        for emp in employees:
            writer.writerow(emp.values())

    print("✅ MySQL data saved to CSV.")


load_csv_to_db()  # Load CSV data when the app starts


@app.get("/employees/")
def get_all_employees():
    """Retrieve all employees from the database."""
    employees = Employee.objects.all().values()
    
    if not employees:
        return {"message": "No employees found"}

    return list(employees)


@app.post("/employees/")
def add_employee(first_name: str, last_name: str, email: str, age: int, contact_number: str, dob: str):
    """Add a new employee to the database."""
    if Employee.objects.filter(email=email).exists():
        raise HTTPException(status_code=400, detail="Employee with this email already exists")

    Employee.objects.create(
        first_name=first_name,
        last_name=last_name,
        email=email,
        age=age,
        contact_number=contact_number,
        dob=dob
    )

    save_db_to_csv()  # Sync DB with CSV
    return {"message": "Employee added successfully"}


@app.put("/employees/{email}")
def update_employee(email: str, first_name: str = None, last_name: str = None, age: int = None, contact_number: str = None, dob: str = None):
    """Update an employee's details."""
    try:
        employee = Employee.objects.get(email=email)
    except Employee.DoesNotExist:
        raise HTTPException(status_code=404, detail="Employee not found")

    if first_name:
        employee.first_name = first_name
    if last_name:
        employee.last_name = last_name
    if age:
        employee.age = age
    if contact_number:
        employee.contact_number = contact_number
    if dob:
        employee.dob = dob

    employee.save()
    save_db_to_csv()  # Sync DB with CSV
    return {"message": "Employee updated successfully"}


@app.delete("/employees/{email}")
def delete_employee(email: str):
    """Delete an employee by email."""
    deleted, _ = Employee.objects.filter(email=email).delete()
    
    if deleted == 0:
        raise HTTPException(status_code=404, detail="Employee not found")

    save_db_to_csv()  # Sync DB with CSV
    return {"message": "Employee deleted successfully"}
