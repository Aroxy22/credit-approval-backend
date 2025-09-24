from decimal import Decimal, ROUND_HALF_UP

def round_nearest_lakh(amount: Decimal) -> Decimal:
    lakh = Decimal('100000')
    return (amount / lakh).quantize(Decimal('1'), rounding=ROUND_HALF_UP) * lakh

def calculate_emi(principal: Decimal, annual_rate_percent: Decimal, tenure_months: int) -> Decimal:
    if tenure_months == 0:
        return Decimal('0')
    monthly_rate = annual_rate_percent / Decimal('12') / Decimal('100')
    numerator = principal * monthly_rate * (1 + monthly_rate) ** tenure_months
    denominator = ((1 + monthly_rate) ** tenure_months) - 1
    emi = numerator / denominator
    return emi.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
