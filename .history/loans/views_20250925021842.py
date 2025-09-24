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
