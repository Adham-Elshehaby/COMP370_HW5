# Task 3: Most abundant complaint type in 2024

## Which complaint type?
Running `borough_complaints.py` over all of 2024 (3.39M incidents with a zipcode, created in 2024) and totalling each complaint type across boroughs, **illegal parking** is the most abundant, with 505,546 incidents. The next most common are noise - residential (379,255), heat/hot water (264,715), blocked driveway (170,140) and noise - street/sidewalk (162,990).

## Jan-Feb vs Jun-Jul 2024 (illegal parking)

| Borough | Jan 1 - Feb 29 | Jun 1 - Jul 31 | Change |
|---|---|---|---|
| Bronx | 11,836 | 13,189 | +11.4% |
| Brooklyn | 31,702 | 32,077 | +1.2% |
| Manhattan | 10,872 | 12,366 | +13.7% |
| Queens | 23,255 | 25,861 | +11.2% |
| Staten Island | 2,245 | 2,734 | +21.8% |
| Unspecified | 6 | 10 | n/a (tiny counts) |
| **Total** | **79,916** | **86,237** | **+7.9%** |

## What the comparison shows
- Illegal parking complaints are higher in June-July than in January-February in every borough. Overall the increase is 6,321 complaints (+7.9%).
- The windows are not the same length (60 days vs 61). Per day, the rate goes from about 1,332 to about 1,414 complaints (+6.1%), so most of the increase is real and not an artifact of the extra day.
- Brooklyn has the most complaints in both periods by a wide margin (about 40% of the total in Jan-Feb and 37% in Jun-Jul), followed by Queens. Brooklyn is also nearly flat (+1.2%), so the overall increase comes mainly from the other boroughs.
- Staten Island (+21.8%) and Manhattan (+13.7%) have the largest relative increases, but Staten Island's counts are small, so its percentage is more sensitive to small changes.
- The "Unspecified" borough has almost no complaints and does not affect the conclusions.

## Caveats
- This is one year of data, so it cannot separate seasonality from a one-off 2024 effect.
- Complaint counts measure reports to 311, not actual parking violations. A rise could reflect more violations, more people reporting, or both. Possible reasons (more people out and driving in summer, for example) are hypotheses that this analysis does not test.
- Only incidents created in 2024 that have a zipcode are included, as per the assignment's trimming rules.
