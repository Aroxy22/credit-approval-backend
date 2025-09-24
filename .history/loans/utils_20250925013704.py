def calculate_monthly_repayment(principal, annual_rate, tenure_months):
    """
    Calculate EMI using compound interest formula
    """
    r = annual_rate / (12 * 100)
    n = tenure_months
    if r == 0:
        return principal / n
    emi = principal * r * (1 + r)**n / ((1 + r)**n - 1)
    return round(emi, 2)
