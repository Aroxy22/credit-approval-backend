# loans/tasks.py
import pandas as pd
from celery import shared_task
from .models import Customer, Loan
from .utils import calculate_monthly_repayment
from django.utils import timezone

@shared_task
def ingest_customers(file_path):
    df = pd.read_excel(file_path)
    for _, row in df.iterrows():
        Customer.objects.update_or_create(
            customer_id=row['Customer ID'],
            defaults={
                'first_name': row['First Name'],
                'last_name': row['Last Name'],
                'age': row['Age'],
                'phone_number': row['Phone Number'],
                'monthly_salary': row['Monthly Salary'],
                'approved_limit': row['Approved Limit'],
                'current_debt': 0,  # if not in Excel, default to 0
            }
        )

@shared_task
def ingest_loans(file_path):
    df = pd.read_excel(file_path)
    for _, row in df.iterrows():
        try:
            customer = Customer.objects.get(customer_id=row['Customer ID'])
        except Customer.DoesNotExist:
            continue

        Loan.objects.update_or_create(
            loan_id=row['Loan ID'],
            defaults={
                'customer': customer,
                'loan_amount': row['Loan Amount'],
                'interest_rate': row['Interest Rate'],
                'tenure': row['Tenure'],
                'monthly_repayment': row.get('Monthly payment') or calculate_monthly_repayment(
                    principal=row['Loan Amount'],
                    rate=row['Interest Rate'],
                    tenure=row['Tenure']
                ),
                'emis_paid_on_time': row['EMIs paid on Time'],
                'start_date': row.get('Date of Approval') or timezone.now().date(),
                'end_date': row.get('End Date') or timezone.now().date(),
            }
        )
