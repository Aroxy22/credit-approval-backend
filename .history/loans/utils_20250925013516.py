def calculate_approved_credit_limit(credit_score):
    if credit_score >= 750:
        return 1_000_000
    elif credit_score >= 700:
        return 500_000
    elif credit_score >= 650:
        return 200_000
    else:
        return 0


def calculate_emi(principal, annual_rate, tenure_months):
    r = annual_rate / (12 * 100)
    n = tenure_months
    if r == 0:
        return principal / n
    emi = principal * r * (1 + r)**n / ((1 + r)**n - 1)
    return round(emi, 2)
