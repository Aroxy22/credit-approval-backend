# Credit Approval Backend

A Django-based backend system for credit/loan approval with automated credit scoring, loan management, and background task processing using Celery.

---

## **Features**

- Customer registration and loan eligibility checking.
- Loan creation, tracking, and EMI calculations.
- Automated credit scoring based on past loans and loan history.
- Background task processing using Celery and Redis.
- PostgreSQL database for persistent storage.
- Fully Dockerized for easy deployment.

---

## **Tech Stack**

- **Backend:** Django, Django REST Framework
- **Database:** PostgreSQL
- **Task Queue:** Celery with Redis
- **Containerization:** Docker & Docker Compose

---

## **Requirements**

- Docker Desktop
- Docker Compose
- Git

---

## **Setup Instructions**

### **Clone the repository**
```bash
git clone https://github.com/Aroxy22/credit-approval-backend.git
cd credit-approval-backend
```

Build Docker images
```bash
docker-compose build
```

Run Docker containers
```bash
docker-compose up
```

This will start the following services:
django → Credit Approval Backend
postgres → Database
redis → Celery broker
celery → Worker for background tasks

## **Testing Endpoints**

You can test all API endpoints using **Postman** or `curl`.

###**Register Customer**
```bash
curl -X POST http://localhost:8000/register/ \
-H "Content-Type: application/json" \
-d '{
  "first_name": "Radhe",
  "last_name": "Shyam",
  "age": 25,
  "monthly_income": 50000,
  "phone_number": "9876543210"
}'
```
### **Loan Eligibility**
```bash
curl -X POST http://localhost:8000/check-eligibility/ \
-H "Content-Type: application/json" \
-d '{
  "customer_id": "ff3f02d8-9794-49bb-ba6a-44af84d33bd2",
  "loan_amount": 500000,
  "tenure": 12,
  "interest_rate": 14
}'
```
### **Create Loan**
```bash
curl -X POST http://localhost:8000/create-loan/ \
-H "Content-Type: application/json" \
-d '{
  "customer_id": "ff3f02d8-9794-49bb-ba6a-44af84d33bd2",
  "loan_id": "loan001",
  "loan_amount": 500000,
  "tenure": 12,
  "interest_rate": 14,
  "start_date": "2025-09-25",
  "end_date": "2026-09-25"
}'
```

###**View Loan**
```bash
curl -X GET http://localhost:8000/view-loan/loan001/
```

Change ID based on Registered customer id generated 


Author
Aryan Mehra

