# Bond Dashboard — Prep Project


## What I Built
A Dash app that pulls live Government of Canada bond yield data from the BOC Valet API.
Select a bond from the dropdown to see its yield, coupon, maturity, and a full yield history chart.


Separate script (quantlib_test.py) uses QuantLib to calculate price from yield and DV01 for the 2-year benchmark bond.


## How to Run
App runs in a Python virtual environment:
source venv/bin/activate
python app.py


QuantLib script runs in base conda (QuantLib incompatible with Python 3.8 venv):
deactivate python quantlib_test.py


Install dependencies: pip install -r requirements.txt
QuantLib (base conda only): pip install QuantLib


## What I Tried / What Worked
- Part 1: Dropdown with bond info panel — working
- Part 2: Time series chart using Plotly Express — working
- Part 3: QuantLib price from yield and DV01 — working


Initially loaded data from a local CSV file, then switched to pulling live from the BOC Valet API


Key results:
- Yield: 2.98%, Price from QuantLib: 98.72, DV01: 0.0174
- Price below par as expected — yield exceeds coupon rate of 2.25%


## What Didn't Work / Limitations
- Price → yield direction not possible, BOC dataset is yield-only
- Bond reference data (coupon, maturity) is hardcoded from the BOC benchmark PDF
- QuantLib couldn't be installed in the venv due to Python 3.8 compatibility,
 ran from base conda instead


## Interesting Things I Noticed
- The BOC API has 27 rows of metadata before the actual data starts
- The data comes in wide format and needs to be melted to long format before use
- The benchmark bond changes periodically — the yield series is stitched together from many different bonds over time
- Small discrepancies between QuantLib and real market prices are expected due to
 day count and settlement conventions specific to Canadian bonds


## Questions
1. Is there a standard way your desk handles Canadian bond convention differences in QuantLib, or does the desk use an internal pricing library?
2. When would you use DV01 vs duration in practice?
3. When the desk looks at a bond, when do you focus on yield vs price and how does that change depending on what you're trying to do?
4. How does the desk actually source price data in practice?
5. The benchmark bond changes periodically; does that create inconsistencies in the yield time series, and how do you handle that for historical analysis?
6. I calculated DV01 numerically by bumping yield. Is this how it's typically done, or is there a preferred method?


Happy to discuss any of this. If there's anything I approached the wrong way or could have done better, I'd love to hear it.

