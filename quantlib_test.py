import QuantLib as ql

# 2yr benchmark bond parameters from BOC benchmark PDF
face_value = 100
coupon_rate = 0.0225
coupon_frequency = ql.Semiannual  # Canadian govt bonds pay semi-annually

# Settlement is typically T+2 business days
settlement_date = ql.Date(7, 4, 2026)
maturity_date = ql.Date(1, 2, 2028)

ql.Settings.instance().evaluationDate = settlement_date

# Canadian govt bonds use ActualActual (ISMA variant)
day_count = ql.ActualActual(ql.ActualActual.ISMA)
calendar = ql.Canada()

# Build coupon schedule backwards from maturity
schedule = ql.Schedule(
    settlement_date,
    maturity_date,
    ql.Period(ql.Semiannual),
    calendar,
    ql.Unadjusted,
    ql.Unadjusted,
    ql.DateGeneration.Backward,
    False
)

bond = ql.FixedRateBond(
    2,
    face_value,
    schedule,
    [coupon_rate],
    day_count
)

# Yield taken from BOC dataset for BD.CDN.2YR.DQ.YLD
# BOC publishes yields as percentages so divide by 100
yield_from_data = 0.0298

# Calculate clean price from yield
# Using clean price because BOC publishes clean prices (excludes accrued interest)
price_from_quantlib = bond.cleanPrice(
    yield_from_data,
    day_count,
    ql.Compounded,
    ql.Semiannual
)

print(f"Yield from data:       {yield_from_data*100:.4f}%")
print(f"Price from QuantLib:   {price_from_quantlib:.4f}")

# -----------------------------
# Price → Yield (commented out — BOC dataset is yield-only, no price data available)
# -----------------------------
# price_from_data = ???
# yield_from_quantlib = bond.bondYield(
#     price_from_data,
#     day_count,
#     ql.Compounded,
#     ql.Semiannual
# )
# print(f"Price from data:       {price_from_data:.4f}")
# print(f"Yield from QuantLib:   {yield_from_quantlib*100:.4f}%")

# -----------------------------
# DV01: price change for a 1 basis point move in yield
# Calculated numerically by bumping yield up and down by 1bp
# -----------------------------
bump = 0.0001

price_up = bond.cleanPrice(
    yield_from_data + bump,
    day_count,
    ql.Compounded,
    ql.Semiannual
)

price_down = bond.cleanPrice(
    yield_from_data - bump,
    day_count,
    ql.Compounded,
    ql.Semiannual
)

dv01 = (price_down - price_up) / 2

print(f"DV01: {dv01:.4f}")

# -----------------------------
# Compare
# Yield difference commented out — would require price → yield direction to work
# Price difference commented out — no price data available from BOC dataset
# -----------------------------
# print(f"\nYield difference:  {abs(yield_from_data - yield_from_quantlib)*100:.4f}%")
# print(f"Price difference:  {abs(price_from_quantlib - price_from_data):.4f}")