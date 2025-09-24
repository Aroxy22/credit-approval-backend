import pandas as pd
from celery import shared_task
from .models import Customer, Loan
from .utils import calculate_monthly_repayment

@shared_task
def ingest_customers(file_path='customer_data.xlsx'):
    df = pd.read_excel(file_path)
    for _, row in df.iterrows():
        Customer.objects.update_or_create(
            customer_id=row['customer_id'],
            defaults={
                'first_name': row['first_name'],
                'last_name': row['last_name'],
                'phone_number': str(row['phone_number']),
                'monthly_salary': row['monthly_salary'],
                'approved_limit': row['approved_limit'],
                'current_debt': row['current_debt']
            }
        )
    return f"{len(df)} customers ingested."


@shared_task
def ingest_loans(file_path='loan_data.xlsx'):
    df = pd.read_excel(file_path)
    for _, row in df.iterrows():
        customer = Customer.objects.get(customer_id=row['customer id'])
        monthly_repayment = row['monthly repayment'] if not pd.isna(row['monthly repayment']) else calculate_monthly_repayment(
            row['loan amount'], row['interest rate'], row['tenure']
        )
        Loan.objects.update_or_create(
            loan_id=row['loan id'],
            defaults={
                'customer': customer,
                'loan_amount': row['loan amount'],
                'tenure': row['tenure'],
                'interest_rate': row['interest rate'],
                'monthly_repayment': monthly_repayment,
                'emis_paid_on_time': row['EMIs paid on time'],
                'start_date': row['start date'],
                'end_date': row['end date']
            }
        )
    return f"{len(df)} loans ingested."

from datetime import date
date.today()
