from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Customer
from .serializers import CustomerSerializer

class RegisterCustomer(APIView):
    def post(self, request):
        data = request.data
        monthly_income = data.get('monthly_salary') or data.get('monthly_income')
        if monthly_income is None:
            return Response({'error': 'monthly_salary is required'}, status=status.HTTP_400_BAD_REQUEST)

        approved_limit = round((float(monthly_income) * 36) / 100000) * 100000  # nearest lakh

        customer = Customer.objects.create(
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            phone_number=data.get('phone_number'),
            monthly_salary=monthly_income,
            approved_limit=approved_limit
        )

        response = {
            'customer_id': customer.customer_id,
            'name': f"{customer.first_name} {customer.last_name}",
            'age': data.get('age'),
            'monthly_salary': monthly_income,
            'approved_limit': approved_limit,
            'phone_number': customer.phone_number
        }
        return Response(response, status=status.HTTP_201_CREATED)

from .models import Loan
from .utils import calculate_monthly_repayment

class CheckEligibility(APIView):
    def post(self, request):
        data = request.data
        customer_id = data.get('customer_id')
        loan_amount = float(data.get('loan_amount'))
        interest_rate = float(data.get('interest_rate'))
        tenure = int(data.get('tenure'))

        try:
            customer = Customer.objects.get(customer_id=customer_id)
        except Customer.DoesNotExist:
            return Response({'error': 'Customer not found'}, status=status.HTTP_404_NOT_FOUND)

        # Simple credit score logic
        past_loans = Loan.objects.filter(customer=customer)
        total_loans = past_loans.count()
        loans_on_time = past_loans.filter(emis_paid_on_time=True).count()

        if customer.monthly_salary * 36 < loan_amount:
            credit_score = 0
        else:
            credit_score = (loans_on_time / total_loans * 50) if total_loans else 50

        approved = False
        if credit_score >= 50:
            approved = True
        elif 30 <= credit_score < 50 and interest_rate > 12:
            approved = True
        elif 10 <= credit_score < 30 and interest_rate > 16:
            approved = True

        emi = calculate_monthly_repayment(loan_amount, interest_rate, tenure)

        return Response({
            'customer_id': customer.customer_id,
            'credit_score': credit_score,
            'approved': approved,
            'corrected_emi': emi
        })
