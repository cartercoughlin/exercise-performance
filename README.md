# Recovery & Readiness Score iOS App

An iOS app that calculates a daily recovery/readiness score based on health metrics from Apple Health, and provides personalized strength and mobility workout recommendations.

## Project Status
✅ **MVP Complete** - iOS app foundation built and ready for Xcode deployment

## Overview
This project combines health data from Garmin, Strava, and Apple Watch (via Apple HealthKit) to calculate a comprehensive recovery score. The app suggests appropriate strength training and mobility workouts based on your readiness level and historic training patterns.

### Key Features
- **Daily Recovery Score**: 0-100 score based on HRV, resting heart rate, sleep quality, and training load
- **Personalized Percentile-Based Scoring**: Your scores are relative to YOUR historical performance, not fixed baselines
  - On your best days (low RHR, high HRV, great sleep, minimal strain), you'll see 90-100 scores
  - The algorithm adapts to your unique physiology and training patterns
  - Uses 30-day rolling windows to stay current with your fitness level
- **HRV Estimation**: Automatically estimates HRV from heart rate data if your device doesn't track HRV natively
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

### Repository Structure
This project is split into two repositories:
- **strava-api** (this repo): Python scripts for Strava data analysis and health metrics
- **[RecoveryApp](https://github.com/cartercoughlin/RecoveryApp)**: iOS app located in a sibling directory

### Open the iOS App in Xcode
1. Navigate to `../RecoveryApp/RecoveryApp/` (sibling directory)
2. Double-click `RecoveryApp.xcodeproj`
3. Enable HealthKit in Signing & Capabilities
4. Run on physical iPhone (HealthKit requires real device)

See the [RecoveryApp repository](https://github.com/cartercoughlin/RecoveryApp) for detailed setup instructions.

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

## How the Scoring Works

The recovery score uses a **percentile-based approach** with **linear interpolation** tailored to your personal data:

### Metric Scoring (Each metric scored 0-100)

Scores are calculated using **linear interpolation** within percentile brackets using the formula:
```
score = min_score + (percentile - min_percentile) * multiplier
```

#### Example Calculation
If you're at the **39th percentile** for HRV:
- Falls in bracket: 20-40th percentile → 50-65 score range
- Formula: `score = 50 + (39 - 20) * 0.75`
  - `(39 - 20) = 19` (shift to start at 0)
  - `19 * 0.75 = 14.25` (scale 20-point range to 15-point range)
  - `50 + 14.25 = 64.25` ✓
- Multiplier `0.75 = (65 - 50) / (40 - 20) = 15 / 20`

---

1. **HRV Score (20% weight)**
   - Compares your current HRV to your last 30 days
   - **80-100th percentile** → `85 + (p - 80) * 0.75` = **85-100 score**
   - **60-80th percentile** → `75 + (p - 60) * 0.50` = **75-85 score**
   - **40-60th percentile** → `65 + (p - 40) * 0.50` = **65-75 score**
   - **20-40th percentile** → `50 + (p - 20) * 0.75` = **50-65 score**
   - **0-20th percentile** → `p * 2.5` = **0-50 score**

2. **Resting Heart Rate Score (25% weight)**
   - Inverted scoring: lower RHR = better recovery
   - Your percentile is inverted: `inverse_percentile = 100 - percentile`
   - Then applies same brackets as HRV using inverse percentile
   - **80-100th inverse** (lowest 20% RHR) → `85 + (ip - 80) * 0.75` = **85-100 score**
   - **60-80th inverse** → `75 + (ip - 60) * 0.50` = **75-85 score**
   - **40-60th inverse** → `65 + (ip - 40) * 0.50` = **65-75 score**
   - **20-40th inverse** → `50 + (ip - 20) * 0.75` = **50-65 score**
   - **0-20th inverse** (highest 20% RHR) → `ip * 2.5` = **0-50 score**
   - Requires 7+ days of data to use percentile scoring

3. **Sleep Score (25% weight)**
   - Duration base score using linear interpolation by hours:
     - **8+ hours** → `90 + (hours - 8) * 5` = **90-100** (capped at 100)
     - **7-8 hours** → `75 + (hours - 7) * 15` = **75-90**
     - **6-7 hours** → `55 + (hours - 6) * 20` = **55-75**
     - **5-6 hours** → `35 + (hours - 5) * 20` = **35-55**
     - **<5 hours** → `hours * 7` = **0-35**
   - Quality adjustment (if sleep stage data available):
     - Deep sleep: 18%+ is excellent (scores 85-100)
     - REM sleep: 20%+ is excellent (scores 85-100)
     - Final score: `duration * 0.4 + deep_score * 0.35 + rem_score * 0.25`

4. **Training Load Score (30% weight)** - INVERSELY related to recovery
   - **Lower recent training = better recovery** (inverse relationship)
   - Ratio = (last 7 days avg training stress) / (last 28 days avg training stress)
   - **Ratio < 0.3** → `min(100, 95 + (0.3 - r) * 16.7)` = **95-100 score**
   - **Ratio 0.3-0.6** → `85 + (0.6 - r) * 33.3` = **85-95 score**
   - **Ratio 0.6-1.0** → `70 + (1.0 - r) * 37.5` = **70-85 score**
   - **Ratio 1.0-1.3** → `55 + (1.3 - r) * 50` = **55-70 score**
   - **Ratio 1.3-1.6** → `40 + (1.6 - r) * 50` = **40-55 score**
   - **Ratio 1.6-2.0** → `25 + (2.0 - r) * 37.5` = **25-40 score**
   - **Ratio > 2.0** → `max(0, 25 - (r - 2.0) * 10)` = **0-25 score**

### Overall Score Categories
- **90-100**: Peak Performance - fully recovered, ready for high-intensity work
- **70-89**: Good - handle moderate to high training loads
- **50-69**: Moderate - consider lighter training or active recovery
- **30-49**: Low - focus on mobility and light activity
- **0-29**: Very Low - prioritize rest

### Why This Works Better
The old system had two major flaws:
1. Fixed 50-point baselines meant even your best days only scored marginally better than average
2. Training load was treated as a "fitness" metric rather than a recovery metric

The new system fixes this by:
- **Generous percentile curves**: Being at/near your median values gives you 65-75 scores (not 50)
- **True personalization**: Top 20% of YOUR values = 85-100 (not just top 10%)
- **Inverse training load**: Low recent training = high recovery score (as it should be!)
- **Adaptive baselines**: Uses 30-day rolling windows that adapt to your fitness level

## Documentation
- [RecoveryApp repository](https://github.com/cartercoughlin/RecoveryApp) - iOS app setup and usage
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
