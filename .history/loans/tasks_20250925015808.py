import pandas as pd
from celery import shared_task
from .models import Customer, Loan
from .utils import calculate_monthly_repayment

@shared_task
def ingest_customers(file_path):
    df = pd.read_excel(file_path)
    for _, row in df.iterrows():
        Customer.objects.create(
            customer_id=row['customer_id'],  # match exact Excel header
            first_name=row['first_name'],
            last_name=row['last_name'],
            phone_number=row['phone_number'],
            monthly_salary=row['monthly_salary'],
            approved_limit=row['approved_limit'],
            current_debt=row['current_debt'],
        )

@shared_task
def ingest_loans(file_path):
    df = pd.read_excel(file_path)
    for _, row in df.iterrows():
        customer = Customer.objects.get(customer_id=row['customer id'])  # match Excel
        Loan.objects.create(
            loan_id=row['loan id'],
            customer=customer,
            loan_amount=row['loan amount'],
            interest_rate=row['interest rate'],
            tenure=row['tenure'],
            monthly_repayment=row['monthly repayment'],
            emis_paid_on_time=row['EMIs paid on time'],
            start_date=row['start date'],
            end_date=row['end date'],
        )

from datetime import date
date.today()
