# Streaming simulation with the DataCo data (without Kafka for now)
# The orders are read one by one in date order, like live events.
# At the end of each day we calculate the late rate and check the alerts:
# baseline 2 = fixed threshold, baseline 3 = z-score

import time
import pandas as pd

# settings
threshold = 0.65    # fixed threshold (65% late)
z_limit = 2         # z-score limit
warmup = 30         # number of days needed before using the z-score
speed = 0           # pause between events in seconds (0 = no pause)

# load the data
data = pd.read_csv("dataco_clean.csv")
data["order_date"] = pd.to_datetime(data["order_date"])

# remove the data after September 2017 (problem found in the EDA)
data = data[data["order_date"] < "2017-10-01"]

# sort by date
data = data.sort_values("order_date")

# put the columns in lists
days = data["order_date"].dt.date.tolist()
late = data["Late_delivery_risk"].tolist()
print("Number of events:", len(days))

# variables for the current day
day_events = 0
day_late = 0

# list with the late rate of the past days
past_rates = []

# lists to save the results
result_day = []
result_rate = []
result_z = []
result_alert_fixed = []
result_alert_z = []

start = time.time()

# read the events one by one
for i in range(len(days)):
    day_events = day_events + 1
    day_late = day_late + late[i]

    if speed > 0:
        time.sleep(speed)

    # check if this is the last event of the day
    if i == len(days) - 1:
        end_of_day = True
    elif days[i + 1] != days[i]:
        end_of_day = True
    else:
        end_of_day = False

    if end_of_day:
        # late rate of the day
        rate = day_late / day_events

        # baseline 2: fixed threshold
        alert_fixed = False
        if rate > threshold:
            alert_fixed = True

        # baseline 3: z-score (only with the past days)
        z = 0
        alert_z = False
        if len(past_rates) >= warmup:
            past = pd.Series(past_rates)
            mean = past.mean()
            std = past.std()
            z = (rate - mean) / std
            if z > z_limit or z < -z_limit:
                alert_z = True

        if alert_fixed or alert_z:
            print(days[i], "late rate:", round(rate, 3), "z:", round(z, 2),
                  "fixed alert:", alert_fixed, "z alert:", alert_z)

        # save the results of the day
        result_day.append(days[i])
        result_rate.append(round(rate, 4))
        result_z.append(round(z, 3))
        result_alert_fixed.append(alert_fixed)
        result_alert_z.append(alert_z)

        # add this day to the history and start a new day
        past_rates.append(rate)
        day_events = 0
        day_late = 0

end = time.time()

# save the results in a csv file
results = pd.DataFrame()
results["day"] = result_day
results["late_rate"] = result_rate
results["z"] = result_z
results["alert_fixed"] = result_alert_fixed
results["alert_z"] = result_alert_z
results.to_csv("stream_results.csv", index=False)

# summary
both = results[(results["alert_fixed"] == True) & (results["alert_z"] == True)]

print()
print("Summary")
print("Days processed:", len(results))
print("Fixed threshold alerts:", sum(result_alert_fixed))
print("Z-score alerts:", sum(result_alert_z))
print("Days with both alerts:", len(both))
print("Processing time:", round(end - start, 1), "seconds")
