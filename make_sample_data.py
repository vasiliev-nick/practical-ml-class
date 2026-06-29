"""
make_sample_data.py
-------------------
Generates a small, realistic NYC-taxi-style trip dataset for the TaxiFlow course.

WHY THIS EXISTS
    The real NYC TLC trip records are huge (multiple GB per month). For a course
    we want something small (a few MB), offline, and instantly runnable, but with
    the SAME schema and the SAME "feel" as the real data — including realistic
    correlations, messy values, and natural anomalies.

    To use the REAL data instead, download a monthly Parquet file from:
        https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page
    and adapt the column names to match the schema documented below.

OUTPUT
    data.csv  (~30,000 rows, a few MB)

This script is deterministic (fixed seed) so every student gets identical data.
"""

import numpy as np
import pandas as pd

RNG = np.random.default_rng(20240101)
N = 30000

# ----------------------------------------------------------------------
# Base trip attributes
# ----------------------------------------------------------------------
vendor_id = RNG.choice([1, 2], size=N, p=[0.45, 0.55])

# Pickups spread across January 2023, with more trips in evening hours.
start = pd.Timestamp("2023-01-01")
day_offsets = RNG.integers(0, 31, size=N)
# hour distribution: busier 7-9am and 5-11pm
hour_weights = np.array([
    2, 1, 1, 1, 1, 2, 4, 7, 8, 6, 5, 5,      # 0-11
    5, 5, 5, 6, 7, 9, 9, 8, 7, 6, 5, 3,      # 12-23
], dtype=float)
hour_weights /= hour_weights.sum()
pickup_hour = RNG.choice(np.arange(24), size=N, p=hour_weights)
pickup_minute = RNG.integers(0, 60, size=N)
pickup_dt = (start
             + pd.to_timedelta(day_offsets, unit="D")
             + pd.to_timedelta(pickup_hour, unit="h")
             + pd.to_timedelta(pickup_minute, unit="m"))

passenger_count = RNG.choice([1, 2, 3, 4, 5, 6], size=N,
                             p=[0.70, 0.15, 0.06, 0.04, 0.03, 0.02]).astype(float)

# Trip distance (miles) — log-normal-ish, most trips short.
trip_distance = np.round(RNG.lognormal(mean=0.9, sigma=0.6, size=N), 2)

# NYC TLC taxi zones are 1..265. A couple of "airport" zones tip better.
AIRPORT_ZONES = {132, 138}  # JFK, LaGuardia
pickup_zone = RNG.integers(1, 266, size=N)
dropoff_zone = RNG.integers(1, 266, size=N)

# Payment type: 1=card, 2=cash, 3=no charge, 4=dispute
payment_type = RNG.choice([1, 2, 3, 4], size=N, p=[0.66, 0.30, 0.02, 0.02])

# ----------------------------------------------------------------------
# Fare model
# ----------------------------------------------------------------------
base_fare = 3.0
per_mile = 2.6
trip_minutes = trip_distance * RNG.uniform(2.5, 4.5, size=N)  # rough
fare_amount = np.round(base_fare + per_mile * trip_distance
                       + 0.4 * trip_minutes
                       + RNG.normal(0, 1.5, size=N), 2)
fare_amount = np.clip(fare_amount, 2.5, None)

# ----------------------------------------------------------------------
# Tip model  (THE SIGNAL the course's classifier will learn)
#   - card payers tip; cash tips are essentially never recorded (real quirk!)
#   - airport pickups, late-night trips, and longer trips tip more
# ----------------------------------------------------------------------
is_card = (payment_type == 1)
is_airport = np.isin(pickup_zone, list(AIRPORT_ZONES))
is_late_night = (pickup_hour >= 22) | (pickup_hour <= 5)

tip_rate = (
    0.12
    + 0.06 * is_airport
    + 0.04 * is_late_night
    + 0.02 * (trip_distance > 5)
    + RNG.normal(0, 0.04, size=N)
)
tip_rate = np.clip(tip_rate, 0, 0.5)
tip_amount = np.where(is_card, np.round(tip_rate * fare_amount, 2), 0.0)

total_amount = np.round(fare_amount + tip_amount, 2)

dropoff_dt = pickup_dt + pd.to_timedelta(trip_minutes, unit="m")

df = pd.DataFrame({
    "vendor_id": vendor_id,
    "pickup_datetime": pickup_dt,
    "dropoff_datetime": dropoff_dt,
    "passenger_count": passenger_count,
    "trip_distance": trip_distance,
    "pickup_location_id": pickup_zone,
    "dropoff_location_id": dropoff_zone,
    "payment_type": payment_type,
    "fare_amount": fare_amount,
    "tip_amount": tip_amount,
    "total_amount": total_amount,
})

# ----------------------------------------------------------------------
# Plant realistic MESS + ANOMALIES (seams for later sessions)
#   These are intentionally left in the raw data.
# ----------------------------------------------------------------------
# 1) Missing passenger_count for ~2% of rows
miss_idx = RNG.choice(N, size=int(0.02 * N), replace=False)
df.loc[miss_idx, "passenger_count"] = np.nan

# 2) A handful of impossible trips (anomaly-detection fodder, Session 6)
anom_idx = RNG.choice(N, size=60, replace=False)
df.loc[anom_idx[:20], "trip_distance"] = RNG.uniform(150, 400, size=20)   # 400-mile taxi ride
df.loc[anom_idx[20:35], "fare_amount"] = -RNG.uniform(5, 50, size=15)     # negative fares
df.loc[anom_idx[35:50], "trip_distance"] = 0.0                            # 0 distance...
df.loc[anom_idx[35:50], "fare_amount"] = RNG.uniform(40, 90, size=15)     # ...but big fare
df.loc[anom_idx[50:], "passenger_count"] = 0                              # ghost passengers

# 3) Some duplicated rows (data-quality smell)
dup = df.sample(50, random_state=7)
df = pd.concat([df, dup], ignore_index=True)

df = df.sample(frac=1, random_state=42).reset_index(drop=True)
df.to_csv("data.csv", index=False)
print(f"Wrote data.csv with {len(df)} rows and {df.shape[1]} columns.")
