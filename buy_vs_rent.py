"""Buy vs. rent: year-by-year net-worth comparison.

Both scenarios spend the same total each month. Whoever has the cheaper
housing cost that month invests the difference. Each year we compare:

  Buyer net worth  = home value * (1 - selling cost) - mortgage balance + buyer portfolio
  Renter net worth = renter portfolio (starts with down payment + closing costs)

  Advantage of buying = Buyer NW - Renter NW   (> 0 means buying wins)
"""

# ---- Parameters -------------------------------------------------------------
DEFAULTS = {
    "HOME_PRICE":       500_000,
    "DOWN_PCT":         0.20,     # share of price paid up front
    "CLOSING_PCT":      0.03,     # buyer closing costs, share of price
    "MORTGAGE_RATE":    0.065,    # annual
    "MORTGAGE_YEARS":   30,
    "PROPERTY_TAX_PCT": 0.011,    # annual, share of current home value
    "INSURANCE_PCT":    0.0035,   # annual, share of current home value
    "MAINTENANCE_PCT":  0.01,     # annual, share of current home value
    "HOA_MONTHLY":      0,
    "APPRECIATION":     0.03,     # yearly change in home value
    "SELLING_PCT":      0.06,     # agent and transfer costs when selling
    "RENT_MONTHLY":     2_500,    # starting rent
    "RENT_GROWTH":      0.03,     # yearly rent increase
    "RENTERS_INS_MO":   15,
    "INVEST_RETURN":    0.07,     # annual return on invested money
}
# -----------------------------------------------------------------------------


def monthly_payment(principal, annual_rate, years):
    r, n = annual_rate / 12, years * 12
    if r == 0:
        return principal / n
    return principal * r / (1 - (1 + r) ** -n)


def simulate(params=None):
    p = {**DEFAULTS, **(params or {})}
    years = int(p["MORTGAGE_YEARS"])
    loan = p["HOME_PRICE"] * (1 - p["DOWN_PCT"])
    pmt = monthly_payment(loan, p["MORTGAGE_RATE"], years)
    r_m = p["MORTGAGE_RATE"] / 12
    inv_m = (1 + p["INVEST_RETURN"]) ** (1 / 12) - 1
    app_m = (1 + p["APPRECIATION"]) ** (1 / 12) - 1
    upkeep_pct = p["PROPERTY_TAX_PCT"] + p["INSURANCE_PCT"] + p["MAINTENANCE_PCT"]

    balance = loan
    home_value = p["HOME_PRICE"]
    rent = p["RENT_MONTHLY"]
    renter_port = p["HOME_PRICE"] * (p["DOWN_PCT"] + p["CLOSING_PCT"])
    buyer_port = 0.0
    rows = []

    for year in range(1, years + 1):
        own_cost_yr = rent_cost_yr = 0.0
        for _ in range(12):
            interest = balance * r_m
            balance -= pmt - interest
            ownership = pmt + p["HOA_MONTHLY"] + home_value * upkeep_pct / 12
            renting = rent + p["RENTERS_INS_MO"]
            own_cost_yr += ownership
            rent_cost_yr += renting

            renter_port *= 1 + inv_m
            buyer_port *= 1 + inv_m
            diff = ownership - renting
            if diff > 0:
                renter_port += diff   # owning costs more, so the renter invests the gap
            else:
                buyer_port -= diff    # renting costs more, so the buyer invests the gap
            home_value *= 1 + app_m
        rent *= 1 + p["RENT_GROWTH"]

        balance = max(balance, 0.0)
        equity = home_value * (1 - p["SELLING_PCT"]) - balance
        buyer_nw = equity + buyer_port
        rows.append((year, own_cost_yr, rent_cost_yr, home_value, balance,
                     buyer_nw, renter_port, buyer_nw - renter_port))
    return pmt, rows


if __name__ == "__main__":
    pmt, rows = simulate()
    print(f"Monthly mortgage payment (P&I): ${pmt:,.0f}\n")
    hdr = ("Year", "Own cost/yr", "Rent cost/yr", "Home value", "Loan bal",
           "Buyer NW", "Renter NW", "Buy - Rent")
    print("{:>4} {:>12} {:>12} {:>12} {:>11} {:>12} {:>12} {:>12}".format(*hdr))
    for y, oc, rc, hv, bal, bnw, rnw, adv in rows:
        print(f"{y:>4} {oc:>12,.0f} {rc:>12,.0f} {hv:>12,.0f} {bal:>11,.0f} "
              f"{bnw:>12,.0f} {rnw:>12,.0f} {adv:>+12,.0f}")
