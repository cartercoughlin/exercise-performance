# Recovery & Readiness Score iOS App

An iOS app that calculates a daily recovery/readiness score based on health metrics from Apple Health, and provides personalized strength and mobility workout recommendations.

## Project Status
✅ **MVP Complete** - iOS app foundation built and ready for Xcode deployment

## Overview
This project combines health data from Garmin, Strava, and Apple Watch (via Apple HealthKit) to calculate a comprehensive recovery score. The app suggests appropriate strength training and mobility workouts based on your readiness level and historic training patterns.

### Key Features
- **Daily Recovery Score**: 0-100 score based on HRV, resting heart rate, sleep quality, and training load
- **HRV Estimation**: Automatically estimates HRV from heart rate data if your device doesn't track HRV natively
- **Personalized Baselines**: Uses your last 90 days of HealthKit data to calculate individualized baselines
- **Smart Workout Recommendations**: Suggests strength or mobility workouts based on recovery status
- **Historic Trend Analysis**: Charts showing recovery trends over 7, 14, 30, or 90 days
- **Workout History**: Detailed timeline of all activities with distance, duration, and heart rate data
- **Statistics Dashboard**: Track average recovery score, total workouts, distance, and duration
- **Diagnostic Logging**: Real-time console output showing what data is being fetched and calculated

## Architecture
- **Data Source**: Apple HealthKit (syncs from Garmin, Strava, Apple Watch)
- **Platform**: Native iOS with SwiftUI
- **Algorithm**: On-device processing for privacy and offline capability
- **Storage**: CoreData for historic data persistence

## Getting Started

### Open in Xcode
1. Navigate to `RecoveryApp/RecoveryApp/`
2. Double-click `RecoveryApp.xcodeproj`
3. Enable HealthKit in Signing & Capabilities
4. Run on physical iPhone (HealthKit requires real device)

See [RecoveryApp/README.md](RecoveryApp/README.md) for detailed setup instructions.

## Troubleshooting

### No HRV, Resting HR, or Sleep Data

If your scores show all 50 (default values), this means HealthKit has no data available:

1. **Check Apple Health app** on your iPhone:
   - Open Health app → Browse → Heart → HRV
   - Verify you have recent HRV data from your Apple Watch or Garmin

2. **Enable diagnostic logging** (already added):
   - Open Xcode and connect your iPhone
   - Run the app and watch the Xcode console
   - Look for messages like:
     - ✅ "HRV: X ms" (data found)
     - ⚠️ "No HRV data available" (no data)

3. **Common causes**:
   - **Apple Watch**: Must wear overnight for HRV and sleep tracking
   - **Garmin sync**: Check Garmin Connect app is syncing to Apple Health (Settings → Permissions)
   - **Insufficient data**: App uses 90 days of historic data for personalized baselines

4. **HRV Estimation**: If your device doesn't track HRV natively, the app will automatically estimate it from heart rate variability during sleep hours

5. **Training load showing negative**: Fixed - algorithm now has floor values (30-50)

### Viewing Diagnostic Logs

Connect your iPhone to Xcode and watch the console output:
```
🔐 Requesting HealthKit authorization...
✅ HealthKit authorization granted
📊 Fetching HRV for 2025-11-22...
   Found 12 HRV samples
   ✅ HRV: 45.2 ms
❤️  Fetching Resting HR for 2025-11-22...
   Found 1 RHR samples
   ✅ Resting HR: 58 bpm
😴 Fetching Sleep data for 2025-11-22...
   Found 8 sleep samples
   ✅ Sleep: 7.5 hrs (Deep: 1.2h, REM: 1.8h, Core: 4.5h)
```

## Documentation
- [RecoveryApp/README.md](RecoveryApp/README.md) - iOS app setup and usage
- [RecoveryApp/ALGORITHM_TUNING.md](RecoveryApp/ALGORITHM_TUNING.md) - Adjust algorithm if scores seem off
- [DEV.md](DEV.md) - Development progress and decisions
- [TECH_SPEC.md](TECH_SPEC.md) - Detailed architecture and algorithms

---

## Legacy: Strava Activity Data Retrieval using Python

This repository also contains Python scripts for retrieving activity data from Strava's API and storing it in a local .csv file

## Installation

1. Clone this repository to your local machine.

```bash
git clone https://github.com/yourusername/strava-activity-retrieval.git
cd strava-activity-retrieval
```


2. Install the required packages using pip.

```bash
pip install -r requirements.txt
```

## Configuration

1. Create a `.env` file in the project directory with the following content:

```
CLIENT_ID=XXXXXXXX
CLIENT_SECRET=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
REFRESH_TOKEN=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
```

Replace every field with your data.


## Usage

Run the Python script to retrieve your Strava activity data:

```bash
python main.py
```

Follow the on-screen instructions to authorize the application and retrieve your activity data. The data will be saved to a CSV file in the **data/** directory with current datetime suffix.


Happy analyzing your Strava activity data!
# exercise-performance
