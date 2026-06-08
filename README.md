# Courier & Package Tracking System

## Objective

A backend system built using FastAPI, SQLAlchemy, Pydantic, and SQLite to manage:

- Customers
- Packages
- Shipments
- Delivery Tracking



## Tech Stack

- Python 3.x
- FastAPI
- SQLAlchemy
- Pydantic
- SQLite

---

## Features

### Level 1 – Customer Management

- Create Customer
- View Customers
- Update Customer
- Delete Customer

### Level 2 – Package Management

- Create Package
- View Packages
- Update Package
- Delete Package

### Level 3 – Shipment Management

- Create Shipment
- View Shipment Details
- Update Shipment Status

Statuses:
- Pending
- In Transit
- Out for Delivery
- Delivered
- Returned

### Level 4 – Tracking System

- Create Tracking Record
- Track Package by Tracking ID
- Update Tracking Location

### Level 5 – Business Rules

- Package cannot be created for a non-existing customer
- Weight must be greater than 0
- Delivered shipments cannot be modified
- Tracking ID must be unique

### Level 6 – SQL Queries

- Highest Shipment Customers
- Total Delivered Packages
- Pending Shipments
- Monthly Shipment Report
- Average Delivery Time
- Customer Ranking using Window Functions

---

## Installation

pip install -r requirements.txt


---

## Run Application

uvicorn main:app 


## Swagger Documentation

Open:

http://127.0.0.1:8000/docs

---

## Database

SQLite Database:

courier.db


## SQL Files

- schema.sql
- queries.sql
