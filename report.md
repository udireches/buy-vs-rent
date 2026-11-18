# Buy vs. Rent Report

With the inputs below, renting comes out ahead every year, starting about $47K ahead in year 1 and ending about $322K ahead in year 30. That result depends heavily on the inputs, as the sensitivity check at the end shows. The numbers come from `buy_vs_rent.py`; edit the parameters at the top and run `python3 buy_vs_rent.py` to reproduce or change them.

## Parameters to consider

Beyond house price, down payment, closing costs, rent, investment return and the 30-year mortgage, these also matter a lot:

1. **Mortgage interest rate.** The most important missing input.
2. **Property tax, home insurance and maintenance** (and HOA fees). These are owner-only costs, roughly 2.5% of the home's value per year.
3. **Home appreciation.** It drives how much equity you build.
4. **Rent increases each year.** The rent you avoid paying goes up over time.
5. **Selling costs** (about 6%). Your equity isn't cash until you sell.
6. **Investing the monthly difference.** Whoever has the cheaper month invests the gap. Without this the comparison is unfair.
7. Not modeled, but worth knowing about: PMI (mortgage insurance if your down payment is under 20%), the mortgage-interest tax deduction, and taxes on investment gains or home-sale gains.

## The formula

Both people spend the same amount each month. Each month:

- **Owner cost** = P&I + (tax% + insurance% + maintenance%) × home value ÷ 12 + HOA
- **Renter cost** = rent + renter's insurance
- If the owner cost is higher, the renter invests the difference. If it's lower, the buyer invests it.
- P&I (the monthly principal and interest payment) is `P·r / (1 − (1+r)^−360)`, where P is the loan amount and r is the annual rate ÷ 12.

At the end of each year:

- **Buyer net worth** = home value × (1 − selling%) − loan balance + buyer's investments
- **Renter net worth** = investments, starting from (down payment + closing costs) and growing at the return rate
- **Advantage of buying** = Buyer net worth − Renter net worth. A positive number means buying wins.

## Values used

| Parameter | Value |
|---|---|
| House price | $500,000 |
| Down payment | 20% |
| Closing costs | 3% |
| Mortgage rate | 6.5% (30 years) |
| Property tax | 1.1% per year |
| Home insurance | 0.35% per year |
| Maintenance | 1% per year |
| Home appreciation | 3% per year |
| Selling costs | 6% |
| Starting rent | $2,500/month |
| Rent growth | 3% per year |
| Renter's insurance | $15/month |
| Investment return | 7% per year |

The monthly payment (principal and interest) comes to **$2,528**.

## Year-by-year results

| Year | Own cost/yr | Rent cost/yr | Home value | Loan bal | Buyer NW | Renter NW | **Buy − Rent** |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 42,757 | 30,180 | 515,000 | 395,529 | 88,571 | 136,023 | **−47,452** |
| 2 | 43,129 | 31,080 | 530,450 | 390,759 | 107,864 | 157,974 | **−50,110** |
| 3 | 43,513 | 32,007 | 546,364 | 385,669 | 127,913 | 180,900 | **−52,988** |
| 4 | 43,908 | 32,962 | 562,754 | 380,238 | 148,751 | 204,855 | **−56,104** |
| 5 | 44,315 | 33,945 | 579,637 | 374,444 | 170,415 | 229,891 | **−59,476** |
| 6 | 44,735 | 34,958 | 597,026 | 368,261 | 192,943 | 256,067 | **−63,124** |
| 7 | 45,166 | 36,002 | 614,937 | 361,665 | 216,376 | 283,444 | **−67,069** |
| 8 | 45,611 | 37,076 | 633,385 | 354,627 | 240,755 | 312,088 | **−71,333** |
| 9 | 46,069 | 38,183 | 652,387 | 347,117 | 266,126 | 342,068 | **−75,942** |
| 10 | 46,541 | 39,323 | 671,958 | 339,105 | 292,536 | 373,457 | **−80,921** |
| 11 | 47,027 | 40,497 | 692,117 | 330,555 | 320,035 | 406,333 | **−86,298** |
| 12 | 47,528 | 41,707 | 712,880 | 321,434 | 348,674 | 440,779 | **−92,105** |
| 13 | 48,044 | 42,953 | 734,267 | 311,701 | 378,510 | 476,882 | **−98,373** |
| 14 | 48,575 | 44,236 | 756,295 | 301,316 | 409,601 | 514,737 | **−105,137** |
| 15 | 49,122 | 45,558 | 778,984 | 290,237 | 442,008 | 554,443 | **−112,435** |
| 16 | 49,685 | 46,919 | 802,353 | 278,415 | 475,797 | 596,105 | **−120,307** |
| 17 | 50,266 | 48,321 | 826,424 | 265,801 | 511,037 | 639,835 | **−128,797** |
| 18 | 50,864 | 49,765 | 851,217 | 252,342 | 547,801 | 685,753 | **−137,952** |
| 19 | 51,479 | 51,253 | 876,753 | 237,983 | 586,171 | 733,991 | **−147,820** |
| 20 | 52,113 | 52,785 | 903,056 | 222,661 | 626,914 | 785,371 | **−158,457** |
| 21 | 52,767 | 54,363 | 930,147 | 206,314 | 670,428 | 840,347 | **−169,918** |
| 22 | 53,440 | 55,989 | 958,052 | 188,871 | 716,903 | 899,171 | **−182,268** |
| 23 | 54,133 | 57,663 | 986,793 | 170,260 | 766,542 | 962,113 | **−195,571** |
| 24 | 54,846 | 59,388 | 1,016,397 | 150,403 | 819,561 | 1,029,461 | **−209,900** |
| 25 | 55,582 | 61,164 | 1,046,889 | 129,217 | 876,192 | 1,101,523 | **−225,331** |
| 26 | 56,339 | 62,993 | 1,078,296 | 106,611 | 936,683 | 1,178,630 | **−241,947** |
| 27 | 57,119 | 64,878 | 1,110,645 | 82,491 | 1,001,299 | 1,261,134 | **−259,835** |
| 28 | 57,922 | 66,819 | 1,143,964 | 56,756 | 1,070,322 | 1,349,413 | **−279,091** |
| 29 | 58,750 | 68,818 | 1,178,283 | 29,298 | 1,144,055 | 1,443,872 | **−299,817** |
| 30 | 59,602 | 70,877 | 1,213,631 | 0 | 1,222,821 | 1,544,943 | **−322,122** |

**Why renting wins here:** owning costs about $12.5K more than renting in year 1, and the renter invests that gap at 7% while the home grows at only 3%. A $500K house that rents for only $2,500/month (a price-to-rent ratio of about 17) favors renting.

## Changing one input at a time

| Change | Year 5 | Year 10 | Year 30 | Buying wins from |
|---|---:|---:|---:|---|
| Rent $3,000 | −21.8K | +15.5K | +480K | year 9 |
| Rent $3,500 | +15.8K | +112K | +1.28M | year 4 |
| Mortgage rate 5% | −25.2K | −2.0K | +123K | year 11 |
| Investment return 5% | −41.6K | −26.5K | +298K | year 15 |
| Appreciation 4% | −34.3K | −26.1K | −152K | never |

Rent relative to price and the gap between investment return and appreciation drive the answer most.

## Not modeled

Taxes and PMI. In the US, the mortgage-interest deduction and the $250K/$500K tax-free allowance on home-sale gains would help buying. Capital-gains tax on the renter's investments would also help buying. Including these would move the result somewhat toward buying.
