from garminconnect import Garmin
import datetime
import pandas as pd
import matplotlib.pyplot as plt

username = "cocoughlin@me.com"  # Replace with your Garmin Connect username or email
password = "Cocoughlin1"  # Replace with your Garmin Connect password

try:
    api = Garmin(username, password)
    api.login()
    print("Successfully connected to Garmin Connect API.")
except Exception as e:
    print(f"An error occurred during login: {e}")

# Get all activities
# set the start and end date nine months apart
activity_start_date = datetime.date(2025, 1, 1)
activity_end_date = datetime.date(2025, 11, 20)
today = datetime.date.today().isoformat()

# call the api and create a list of activities from that timeframe
activities = api.get_activities_by_date(
                activity_start_date.isoformat(),
                activity_end_date.isoformat()
  )

activity_df = pd.DataFrame(activities)

heart_rates = api.get_heart_rates(today)
resting_hr = heart_rates.get("restingHeartRate", "n/a")

heart_rates_df = pd.DataFrame(heart_rates['heartRateValues'])

#Daily resting HR

def get_daily_resting_hr(num_days=1):
    today = datetime.date.today()
    start_date = today - datetime.timedelta(days=num_days - 1)

    dates = []
    rhr_values = []

    for i in range(num_days):
        d = start_date + datetime.timedelta(days=i)
        day_str = d.strftime("%Y-%m-%d")

        # Option A: use get_heart_rates and read restingHeartRate
        hr_data = api.get_heart_rates(day_str) or {}

        resting = hr_data.get("restingHeartRate")

        # If your library version has get_resting_heart_rate, you can try:
        # rhr_data = client.get_resting_heart_rate(day_str)
        # resting = rhr_data.get("value") if isinstance(rhr_data, dict) else rhr_data

        dates.append(d)
        rhr_values.append(resting)
    
    return dates, rhr_values

def plot_resting_hr(ROLLING=30, NUM_DAYS=300):

    def rolling_average(values, window):
        avg = []
        for i in range(len(values)):
            if i < window - 1 or values[i] is None:
                avg.append(None)
            else:
                window_vals = [v for v in values[i-window+1:i+1] if v is not None]
                avg.append(sum(window_vals) / len(window_vals) if window_vals else None)
        return avg

    # Pull data
    dates, rhr_values = get_daily_resting_hr(NUM_DAYS)

    rhr_roll = rolling_average(rhr_values, ROLLING)

    # Filter missing data
    daily_dates = [d for d, v in zip(dates, rhr_values) if v is not None]
    daily_vals  = [v for v in rhr_values if v is not None]

    roll_dates = [d for d, v in zip(dates, rhr_roll) if v is not None]
    roll_vals  = [v for v in rhr_roll if v is not None]

    # ---- LINE CHART ONLY ----
    plt.figure(figsize=(11, 6))
    plt.scatter(daily_dates, daily_vals, s=60, label="Daily Resting HR")
    plt.plot(roll_dates, roll_vals, linewidth=3,
             label=f"{ROLLING}-Day Rolling Avg", color='orange')

    plt.title(f"Resting Heart Rate – Last {NUM_DAYS} Days")
    plt.xlabel("Date")
    plt.ylabel("Resting HR (bpm)")
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.show()

    # Show on screen
    plt.show()

if __name__ == "__main__":
    plot_resting_hr()