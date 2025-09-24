import pandas as pd
from celery import shared_task
from .models import Customer, Loan
from .utils import calculate_approved_credit_limit, calculate_emi

@shared_task
def ingest_customers(file_path='customer_data.xlsx'):
    df = pd.read_excel(file_path)
    for _, row in df.iterrows():
        Customer.objects.update_or_create(
            email=row['email'],
            defaults={
                'first_name': row['first_name'],
                'last_name': row['last_name'],
                'dob': row['dob'],
                'credit_score': row['credit_score'],
                'approved_credit_limit': calculate_approved_credit_limit(row['credit_score'])
            }
        )
    return f"{len(df)} customers ingested."


@shared_task
def ingest_loans(file_path='loan_data.xlsx'):
    df = pd.read_excel(file_path)
    for _, row in df.iterrows():
        customer = Customer.objects.get(email=row['customer_email'])
        Loan.objects.update_or_create(
            customer=customer,
            principal_amount=row['principal_amount'],
            interest_rate=row['interest_rate'],
            tenure_months=row['tenure_months'],
            defaults={
                'emi': calculate_emi(row['principal_amount'], row['interest_rate'], row['tenure_months'])
            }
        )
    return f"{len(df)} loans ingested."
