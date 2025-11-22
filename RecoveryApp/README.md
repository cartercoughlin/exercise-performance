# Recovery App - iOS Project

## Opening the Project

1. Navigate to: `RecoveryApp/RecoveryApp/`
2. Double-click: `RecoveryApp.xcodeproj`
3. Xcode will open the project

## Project Structure

```
RecoveryApp/
├── RecoveryApp.swift           # App entry point (@main)
├── ContentView.swift            # Main tab navigation
├── Info.plist                   # HealthKit permissions configured
│
├── Models/                      # Data models
│   ├── WorkoutType.swift
│   ├── HealthMetrics.swift
│   ├── WorkoutData.swift
│   ├── RecoveryData.swift
│   └── WorkoutRecommendation.swift
│
├── Services/                    # Business logic
│   ├── HealthKitManager.swift          # Fetches data from Apple Health
│   ├── RecoveryCalculator.swift        # Calculates recovery score
│   └── RecommendationEngine.swift      # Suggests workouts
│
├── ViewModels/                  # State management
│   └── DashboardViewModel.swift
│
└── Views/                       # User interface
    ├── Dashboard/
    │   ├── DashboardView.swift
    │   └── RecoveryScoreCard.swift
    ├── Recommendations/
    │   └── WorkoutDetailView.swift
    ├── History/
    │   └── HistoryView.swift
    └── Settings/
        └── SettingsView.swift
```

## Required Setup in Xcode

### 1. Enable HealthKit
- Select project in Navigator
- Select "RecoveryApp" target
- Go to "Signing & Capabilities" tab
- Click "+ Capability"
- Add "HealthKit"

### 2. Configure Signing
- Select your Development Team
- Xcode will automatically configure code signing

### 3. Info.plist (Already Configured)
The following permissions are already set:
- `NSHealthShareUsageDescription` - Read health data
- `NSHealthUpdateUsageDescription` - Write workout data
- `UIRequiredDeviceCapabilities` - Requires HealthKit

## Running the App

### Requirements
- **Physical iPhone** (iOS 16.0+) - Simulator doesn't support HealthKit
- **Apple Watch** (optional) - For complete health data
- **Garmin/Strava** synced to Apple Health

### Steps
1. Connect your iPhone to your Mac
2. Select your iPhone as the run destination
3. Click Run (▶️) or press Cmd+R
4. Grant HealthKit permissions when prompted
5. App will load and display recovery score

## Data Sources

### Apple Health Metrics Used
- Heart Rate Variability (HRV)
- Resting Heart Rate
- Sleep Analysis (duration, stages)
- Workouts (with heart rate data)
- Steps
- Active Energy

### Syncing Garmin to Apple Health
1. Open Garmin Connect app
2. Settings → Health & Fitness Apps → Apple Health
3. Enable: Heart Rate, HRV, Sleep, Workouts, Steps

### Syncing Strava to Apple Health
1. Open Strava app
2. Profile → Settings → Applications → Health
3. Enable "Write Data" for all metrics

## How It Works

### Recovery Score (0-100)
Calculated using weighted formula:
- **HRV (35%)**: Today's HRV vs 7-day baseline
- **Resting HR (25%)**: Current vs 30-day average
- **Sleep (25%)**: Duration + quality (REM/deep %)
- **Training Load (15%)**: Acute:chronic workload ratio

### Score Categories
- **90-100**: Peak Performance → High-intensity workouts
- **70-89**: Good → Moderate training
- **50-69**: Moderate → Light training
- **30-49**: Low → Active recovery
- **0-29**: Very Low → Complete rest

### Workout Recommendations
Based on score and recent training:
- Strength workouts (full body, upper, lower)
- Mobility/yoga sessions
- Active recovery
- Complete rest

## Troubleshooting

### "HealthKit not available"
- Must test on real iPhone, not Simulator

### "No data available"
- Check Apple Health app has data
- Verify Garmin/Strava sync is enabled
- Need at least 1 day of data to start

### Build errors
- Ensure HealthKit capability is added
- Check all files are in target membership
- Build Phases → Compile Sources should list all .swift files

### Low/inaccurate scores
- Need 7 days of data for accurate HRV baseline
- Algorithm weights may need personal tuning
- Check sleep data is tracking properly

## Customization

### Adjust Algorithm Weights
Edit `Services/RecoveryCalculator.swift` line 28:
```swift
let overallScore = Int(
    hrvScore * 0.35 +      // Change these weights
    rhrScore * 0.25 +
    sleepScore * 0.25 +
    trainingLoadScore * 0.15
)
```

### Add Custom Workouts
Edit `Services/RecommendationEngine.swift`
Add new workout templates in recommendation functions

### Change UI Colors
Edit `Models/RecoveryData.swift`
Modify `RecoveryCategory.color` property

## Next Features to Build

### High Priority
- [ ] History view with trend charts
- [ ] Weekly planning based on trends
- [ ] Apple Watch app

### Medium Priority
- [ ] Workout tracking
- [ ] Custom workout builder
- [ ] Daily notifications

### Low Priority
- [ ] Data export (CSV)
- [ ] AI insights
- [ ] Social sharing

## Documentation

See parent directory for:
- `../DEV.md` - Development log
- `../TECH_SPEC.md` - Technical specification
- `../README.md` - Project overview

## Questions?

The app is fully functional and ready to test!
Open `RecoveryApp.xcodeproj` in Xcode and run on your iPhone.
