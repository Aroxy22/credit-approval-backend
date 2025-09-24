# loans/tasks.py
import pandas as pd
from celery import shared_task
from .models import Customer, Loan
from .utils import calculate_monthly_repayment

@shared_task
def ingest_customers(file_path):
    df = pd.read_excel(file_path)

    for _, row in df.iterrows():
        Customer.objects.update_or_create(
            customer_id=row['Customer ID'],
            defaults={
                'first_name': row['First Name'],
                'last_name': row['Last Name'],
                'monthly_salary': row['Monthly Salary'],
                'approved_limit': row['Approved Limit'],
                # remove 'age' if your model doesn't have it
                # 'age': row['Age'],  # optional
                # 'phone_number': row['Phone Number'],  # optional
            }
        )

@shared_task
def ingest_loans(file_path):
    df = pd.read_excel(file_path)

    for _, row in df.iterrows():
        try:
            customer = Customer.objects.get(customer_id=row['Customer ID'])
        except Customer.DoesNotExist:
            # skip if customer not found
            continue

        monthly_repayment = calculate_monthly_repayment(
            row['Loan Amount'], row['Interest Rate'], row['Tenure']
        )

        Loan.objects.update_or_create(
            loan_id=row['Loan ID'],
            defaults={
                'customer': customer,
                'loan_amount': row['Loan Amount'],
                'tenure': row['Tenure'],
                'interest_rate': row['Interest Rate'],
                'monthly_repayment': monthly_repayment,
                'emis_paid_on_time': row.get('EMIs paid on Time', True),
                'start_date': row.get('Date of Approval'),
                'end_date': row.get('End Date'),
            }
        )
