# loans/tasks.py
import pandas as pd
from celery import shared_task, chain
from .models import Customer, Loan
from .utils import calculate_monthly_repayment
from django.db import transaction

@shared_task
def ingest_customers(file_path):
    df = pd.read_excel(file_path)

    customers_to_create = []
    for _, row in df.iterrows():
        customers_to_create.append(
            Customer(
                customer_id=row['Customer ID'],
                first_name=row['First Name'],
                last_name=row['Last Name'],
                monthly_salary=row['Monthly Salary'],
                approved_limit=row['Approved Limit']
            )
        )

    # Bulk create avoids multiple DB hits and reduces locks
    Customer.objects.bulk_create(customers_to_create, ignore_conflicts=True)
    return "customers_done"

@shared_task
def ingest_loans(file_path):
    df = pd.read_excel(file_path)

    loans_to_create = []
    for _, row in df.iterrows():
        try:
            customer = Customer.objects.get(customer_id=row['Customer ID'])
        except Customer.DoesNotExist:
            # Skip loans if customer is missing
            continue

        monthly_repayment = calculate_monthly_repayment(
            row['Loan Amount'], row['Interest Rate'], row['Tenure']
        )

        loans_to_create.append(
            Loan(
                loan_id=row['Loan ID'],
                customer=customer,
                loan_amount=row['Loan Amount'],
                tenure=row['Tenure'],
                interest_rate=row['Interest Rate'],
                monthly_repayment=monthly_repayment,
                emis_paid_on_time=row.get('EMIs paid on Time', True),
                start_date=row.get('Date of Approval'),
                end_date=row.get('End Date'),
            )
        )

    Loan.objects.bulk_create(loans_to_create, ignore_conflicts=True)
    return "loans_done"

@shared_task
def ingest_all(customer_file, loan_file):
    """
    Chain customer ingestion first, then loan ingestion.
    """
    workflow = chain(
        ingest_customers.s(customer_file),
        ingest_loans.s(loan_file)
    )
    workflow.apply_async()
