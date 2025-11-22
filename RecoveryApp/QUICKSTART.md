# Quick Start Guide

## 🚀 Get Running in 5 Minutes

### Step 1: Open Xcode Project
```bash
cd RecoveryApp/RecoveryApp
open RecoveryApp.xcodeproj
```

### Step 2: Enable HealthKit
1. Click on "RecoveryApp" project in Navigator (top left)
2. Select "RecoveryApp" under TARGETS
3. Click "Signing & Capabilities" tab
4. Click "+ Capability" button
5. Search for and add "HealthKit"

### Step 3: Configure Signing
1. Still in "Signing & Capabilities"
2. Under "Signing", select your Team
3. Xcode will automatically configure the rest

### Step 4: Connect iPhone & Run
1. Connect iPhone to Mac with cable
2. Unlock iPhone
3. Trust computer if prompted
4. In Xcode, select your iPhone from device dropdown (top toolbar)
5. Click ▶️ Run button (or press Cmd+R)

### Step 5: Grant Permissions
1. App will open on your iPhone
2. Grant HealthKit permissions when prompted
3. Select "Allow All" for best experience

## ✅ That's It!

The app should now display your recovery score based on data from Apple Health.

## 📊 Data Requirements

### For Best Results
Make sure your iPhone has health data from:
- **Garmin Connect** (sync to Apple Health)
- **Strava** (sync to Apple Health)
- **Apple Watch** (automatic)

### Minimum Data Needed
- At least 1 day of sleep data
- At least 1 resting heart rate measurement
- At least 1 HRV measurement

The app needs 7 days of data for optimal baseline calculations.

## 🔧 Troubleshooting

**"No data available"**
- Open Apple Health app and verify data exists
- Check Garmin/Strava sync settings
- Wait 24 hours after enabling sync

**Build errors**
- Make sure HealthKit capability was added
- Clean build folder: Product → Clean Build Folder (Cmd+Shift+K)
- Restart Xcode

**Can't select iPhone**
- Try unplugging and reconnecting
- Check cable is data-capable (not just charging)
- Update iPhone to latest iOS

## 📱 What You'll See

### Dashboard Tab
- Large recovery score (0-100)
- Color-coded category (Peak, Good, Moderate, Low)
- Score breakdown by component
- Today's recommended workout

### History Tab
- Coming soon: Charts and trends

### Settings Tab
- HealthKit authorization status
- App version info

## 🏋️ Understanding Your Score

**90-100** (Green) → Go hard! High-intensity training
**70-89** (Light Green) → Good to go. Moderate training
**50-69** (Yellow) → Take it easy. Light work
**30-49** (Orange) → Active recovery only
**0-29** (Red) → Rest day!

## 📈 Next Steps

After testing the app:
1. Use it for 7 days to establish baselines
2. Adjust algorithm weights if needed (`Services/RecoveryCalculator.swift`)
3. Check out `README.md` for customization options
4. Consider adding features from `DEV.md` roadmap

## 📚 Full Documentation

- **This guide**: Quick setup
- **README.md**: Complete instructions and troubleshooting
- **../TECH_SPEC.md**: Technical details and algorithms
- **../DEV.md**: Development roadmap

Happy training! 💪
