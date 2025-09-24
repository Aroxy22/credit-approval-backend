# loans/tasks.py
import pandas as pd
from celery import shared_task
from .models import Customer, Loan
from .utils import calculate_monthly_repayment
from django.utils import timezone

# Helper to normalize column names (remove spaces, lowercase)
def normalize_columns(df):
    df.columns = [c.strip().replace(' ', '_').lower() for c in df.columns]
    return df

@shared_task
def ingest_customers(file_path):
    df = pd.read_excel(file_path)
    df = normalize_columns(df)

    for _, row in df.iterrows():
        Customer.objects.update_or_create(
            customer_id=row['customer_id'],
            defaults={
                'first_name': row['first_name'],
                'last_name': row['last_name'],
                'phone_number': row['phone_number'],
                'monthly_salary': row['monthly_salary'],
                'approved_limit': row['approved_limit'],
                'current_debt': row['current_debt'],
            }
        )

@shared_task
def ingest_loans(file_path):
    df = pd.read_excel(file_path)
    df = normalize_columns(df)

    for _, row in df.iterrows():
        try:
            customer = Customer.objects.get(customer_id=row['customer_id'])
        except Customer.DoesNotExist:
            continue  # skip loans if customer not found

        Loan.objects.update_or_create(
            loan_id=row['loan_id'],
            defaults={
                'customer': customer,
                'loan_amount': row['loan_amount'],
                'interest_rate': row['interest_rate'],
                'tenure': row['tenure'],
                'monthly_repayment': row.get('monthly_repayment') or calculate_monthly_repayment(
                    principal=row['loan_amount'],
                    rate=row['interest_rate'],
                    tenure=row['tenure']
                ),
                'emis_paid_on_time': row['emis_paid_on_time'],
                'start_date': row.get('start_date') or timezone.now().date(),
                'end_date': row.get('end_date') or timezone.now().date(),
            }
        )
