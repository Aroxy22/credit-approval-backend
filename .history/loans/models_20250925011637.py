from django.db import models
from decimal import Decimal


class Customer(models.Model):
    customer_id = models.IntegerField(unique=True)  # from Excel dataset
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    age = models.IntegerField(null=True, blank=True)
    monthly_income = models.DecimalField(max_digits=12, decimal_places=2)
    approved_limit = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    current_debt = models.DecimalField(max_digits=15, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.customer_id} - {self.first_name} {self.last_name}"


class Loan(models.Model):
    STATUS_CHOICES = (
        ('current', 'current'),
        ('repaid', 'repaid'),
        ('default', 'default'),
    )

    loan_id = models.IntegerField(unique=True)  # from Excel dataset
    customer = models.ForeignKey(Customer, related_name='loans', on_delete=models.CASCADE)
    loan_amount = models.DecimalField(max_digits=15, decimal_places=2)
    tenure_months = models.IntegerField()
    interest_rate = models.DecimalField(max_digits=6, decimal_places=2)  # annual percentage
    monthly_installment = models.DecimalField(max_digits=15, decimal_places=2)
    emis_paid_on_time = models.IntegerField(default=0)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='current')

    def __str__(self):
        return f"Loan {self.loan_id} for Customer {self.customer.customer_id}"
