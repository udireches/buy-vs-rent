/* Buy vs. rent: year-by-year net-worth comparison (JavaScript port of buy_vs_rent.py).

Both scenarios spend the same total each month. Whoever has the cheaper
housing cost that month invests the difference. Each year we compare:

  Buyer net worth  = home value * (1 - selling cost) - mortgage balance + buyer portfolio
  Renter net worth = renter portfolio (starts with down payment + closing costs)

  Advantage of buying = Buyer NW - Renter NW   (> 0 means buying wins)
*/

// ---- Parameters -------------------------------------------------------------
const DEFAULTS = {
  HOME_PRICE:       500000,
  DOWN_PCT:         0.20,     // share of price paid up front
  CLOSING_PCT:      0.03,     // buyer closing costs, share of price
  MORTGAGE_RATE:    0.065,    // annual
  MORTGAGE_YEARS:   30,
  PROPERTY_TAX_PCT: 0.011,    // annual, share of current home value
  INSURANCE_PCT:    0.0035,   // annual, share of current home value
  MAINTENANCE_PCT:  0.01,     // annual, share of current home value
  HOA_MONTHLY:      0,
  APPRECIATION:     0.03,     // yearly change in home value
  SELLING_PCT:      0.06,     // agent and transfer costs when selling
  RENT_MONTHLY:     2500,     // starting rent
  RENT_GROWTH:      0.03,     // yearly rent increase
  RENTERS_INS_MO:   15,
  INVEST_RETURN:    0.07,     // annual return on invested money
};
// -----------------------------------------------------------------------------

// key, label, min, max, step, format ("$" or "%")
const SLIDERS = [
  ["HOME_PRICE",       "House price",        100000, 2000000, 10000,   "$"],
  ["DOWN_PCT",         "Down payment",       0,      1,       0.01,    "%"],
  ["CLOSING_PCT",      "Closing costs",      0,      0.06,    0.0025,  "%"],
  ["MORTGAGE_RATE",    "Mortgage rate",      0.02,   0.12,    0.00125, "%"],
  ["PROPERTY_TAX_PCT", "Property tax",       0,      0.03,    0.0005,  "%"],
  ["INSURANCE_PCT",    "Home insurance",     0,      0.015,   0.0005,  "%"],
  ["MAINTENANCE_PCT",  "Maintenance",        0,      0.03,    0.001,   "%"],
  ["HOA_MONTHLY",      "HOA / month",        0,      1000,    25,      "$"],
  ["APPRECIATION",     "Home appreciation",  -0.02,  0.10,    0.0025,  "%"],
  ["SELLING_PCT",      "Selling costs",      0,      0.10,    0.005,   "%"],
  ["RENT_MONTHLY",     "Rent / month",       500,    10000,   50,      "$"],
  ["RENT_GROWTH",      "Rent growth",        -0.02,  0.10,    0.0025,  "%"],
  ["RENTERS_INS_MO",   "Renter's insurance / month", 0, 100,  5,       "$"],
  ["INVEST_RETURN",    "Investment return",  0,      0.12,    0.0025,  "%"],
].map(([key, label, min, max, step, fmt]) => ({ key, label, min, max, step, fmt }));


function monthlyPayment(principal, annualRate, years) {
  const r = annualRate / 12, n = years * 12;
  if (r === 0) return principal / n;
  return principal * r / (1 - (1 + r) ** -n);
}


function simulate(params = {}) {
  const p = { ...DEFAULTS, ...params };
  const years = Math.trunc(p.MORTGAGE_YEARS);
  const loan = p.HOME_PRICE * (1 - p.DOWN_PCT);
  const pmt = monthlyPayment(loan, p.MORTGAGE_RATE, years);
  const rM = p.MORTGAGE_RATE / 12;
  const invM = (1 + p.INVEST_RETURN) ** (1 / 12) - 1;
  const appM = (1 + p.APPRECIATION) ** (1 / 12) - 1;
  const upkeepPct = p.PROPERTY_TAX_PCT + p.INSURANCE_PCT + p.MAINTENANCE_PCT;

  let balance = loan;
  let homeValue = p.HOME_PRICE;
  let rent = p.RENT_MONTHLY;
  let renterPort = p.HOME_PRICE * (p.DOWN_PCT + p.CLOSING_PCT);
  let buyerPort = 0;
  const rows = [];

  for (let year = 1; year <= years; year++) {
    let ownCostYr = 0, rentCostYr = 0;
    for (let m = 0; m < 12; m++) {
      const interest = balance * rM;
      balance -= pmt - interest;
      const ownership = pmt + p.HOA_MONTHLY + homeValue * upkeepPct / 12;
      const renting = rent + p.RENTERS_INS_MO;
      ownCostYr += ownership;
      rentCostYr += renting;

      renterPort *= 1 + invM;
      buyerPort *= 1 + invM;
      const diff = ownership - renting;
      if (diff > 0) renterPort += diff;   // owning costs more, so the renter invests the gap
      else buyerPort -= diff;             // renting costs more, so the buyer invests the gap
      homeValue *= 1 + appM;
    }
    rent *= 1 + p.RENT_GROWTH;

    balance = Math.max(balance, 0);
    const equity = homeValue * (1 - p.SELLING_PCT) - balance;
    const buyerNw = equity + buyerPort;
    rows.push({
      year, own_cost: ownCostYr, rent_cost: rentCostYr, home_value: homeValue,
      balance, buyer_nw: buyerNw, renter_nw: renterPort, advantage: buyerNw - renterPort,
    });
  }
  return { payment: pmt, rows };
}


/* Buy vs. invest: buy the home as a rental (you live elsewhere) or put the same
money in the market. RENT_MONTHLY is the rent you collect. Each month the
landlord pays owner costs and collects rent; a surplus is invested by the
landlord, a shortfall is paid from pocket and the market investor invests the
same amount. That is the buy-vs-rent cash flow with no renter's insurance, and
where you live yourself costs the same in both cases, so it cancels out.

  Property net worth = home value * (1 - selling cost) - mortgage balance + invested surplus
  Market net worth   = (down payment + closing costs) invested + invested shortfalls
*/
function simulateInvest(params = {}) {
  return simulate({ ...params, RENTERS_INS_MO: 0 });
}


if (typeof module !== "undefined") {
  module.exports = { DEFAULTS, SLIDERS, monthlyPayment, simulate, simulateInvest };

  // Run directly with Node to print the same table as `python3 buy_vs_rent.py`.
  if (require.main === module) {
    const { payment, rows } = simulate();
    const n = (v, w) => Math.round(v).toLocaleString("en-US").padStart(w);
    console.log(`Monthly mortgage payment (P&I): $${Math.round(payment).toLocaleString("en-US")}\n`);
    console.log(["Year", "Own cost/yr", "Rent cost/yr", "Home value", "Loan bal",
                 "Buyer NW", "Renter NW", "Buy - Rent"]
      .map((h, i) => h.padStart([4, 12, 12, 12, 11, 12, 12, 12][i])).join(" "));
    for (const r of rows) {
      const adv = Math.round(r.advantage);
      console.log([String(r.year).padStart(4), n(r.own_cost, 12), n(r.rent_cost, 12),
                   n(r.home_value, 12), n(r.balance, 11), n(r.buyer_nw, 12), n(r.renter_nw, 12),
                   ((adv > 0 ? "+" : adv < 0 ? "-" : "+") + Math.abs(adv).toLocaleString("en-US")).padStart(12)]
        .join(" "));
    }
  }
}
