# Recovery Score App - Technical Specification

## System Architecture

### Overview
Native iOS app using on-device processing. No backend server required.

```
┌─────────────────────────────────────────┐
│         Apple Health / HealthKit         │
│  (Data from Garmin, Strava, Apple Watch) │
└──────────────────┬──────────────────────┘
                   │
                   ▼
         ┌─────────────────────┐
         │   iOS App (Swift)    │
         │  ┌───────────────┐   │
         │  │ HealthKit API │   │
         │  └───────┬───────┘   │
         │          │           │
         │  ┌───────▼───────┐   │
         │  │  Data Layer   │   │
         │  │  (CoreData)   │   │
         │  └───────┬───────┘   │
         │          │           │
         │  ┌───────▼────────┐  │
         │  │   Recovery     │  │
         │  │   Algorithm    │  │
         │  └───────┬────────┘  │
         │          │           │
         │  ┌───────▼────────┐  │
         │  │ Recommendation │  │
         │  │    Engine      │  │
         │  └───────┬────────┘  │
         │          │           │
         │  ┌───────▼────────┐  │
         │  │  SwiftUI Views │  │
         │  └────────────────┘  │
         └─────────────────────┘
                   │
                   ▼
         ┌─────────────────────┐
         │   Apple Watch App    │
         │   (Complications)    │
         └─────────────────────┘
```

## Data Sources

### HealthKit Metrics Available
All metrics sync automatically from Garmin/Strava to Apple Health:

1. **Heart Rate Variability (HRV)**
   - `HKQuantityTypeIdentifier.heartRateVariabilitySDNN`
   - Measured during sleep
   - Most important recovery metric

2. **Resting Heart Rate**
   - `HKQuantityTypeIdentifier.restingHeartRate`
   - Daily measurement
   - Trend analysis for fatigue

3. **Sleep Analysis**
   - `HKCategoryTypeIdentifier.sleepAnalysis`
   - Duration, in-bed time, asleep time
   - Sleep stages: REM, Core, Deep, Awake
   - `HKQuantityTypeIdentifier.sleepDurationGoal`

4. **Workouts**
   - `HKWorkoutType`
   - Activity type, duration, distance
   - Heart rate data during workout
   - Energy burned
   - Running mileage tracking

5. **Active Energy**
   - `HKQuantityTypeIdentifier.activeEnergyBurned`
   - Daily activity level

6. **Steps**
   - `HKQuantityTypeIdentifier.stepCount`
   - General activity indicator

7. **Respiratory Rate** (optional)
   - `HKQuantityTypeIdentifier.respiratoryRate`
   - Additional recovery indicator

## Recovery Score Algorithm

### Formula (0-100 scale)

```swift
RecoveryScore = (
    HRV_Score * 0.35 +
    RHR_Score * 0.25 +
    Sleep_Score * 0.25 +
    TrainingLoad_Score * 0.15
)
```

### Component Calculations

#### 1. HRV Score (35% weight)
```swift
// Compare today's HRV to 7-day baseline
baseline = average(last_7_days_HRV)
today_hrv_deviation = (today_HRV - baseline) / baseline * 100

// Score based on deviation
if today_hrv_deviation >= 0:
    hrv_score = min(100, 50 + today_hrv_deviation * 2)
else:
    hrv_score = max(0, 50 + today_hrv_deviation * 2)
```

#### 2. Resting HR Score (25% weight)
```swift
// Compare to baseline (lower is better for recovery)
baseline_rhr = average(last_30_days_resting_hr)
rhr_deviation = (baseline_rhr - today_rhr)

// Each 1 bpm below baseline = +5 points
// Each 1 bpm above baseline = -5 points
rhr_score = clamp(50 + (rhr_deviation * 5), 0, 100)
```

#### 3. Sleep Score (25% weight)
```swift
// Sleep quality components
duration_score = (sleep_hours / optimal_hours) * 100  // optimal = 7-9 hours
deep_sleep_pct = deep_sleep_minutes / total_sleep_minutes
rem_sleep_pct = rem_sleep_minutes / total_sleep_minutes

// Weighted sleep score
sleep_score = (
    duration_score * 0.5 +
    deep_sleep_pct * 200 * 0.3 +    // Aim for 15-25% deep sleep
    rem_sleep_pct * 200 * 0.2        // Aim for 20-25% REM
)
```

#### 4. Training Load Score (15% weight)
```swift
// Acute vs Chronic workload ratio
acute_load = sum(last_7_days_training_stress)
chronic_load = sum(last_28_days_training_stress) / 4

ratio = acute_load / chronic_load

// Optimal ratio: 0.8 - 1.3
// < 0.8: detraining
// 0.8-1.3: optimal
// > 1.3: high injury risk
if ratio < 0.8:
    load_score = 60 + (ratio - 0.8) * 100  // Penalize detraining
else if ratio <= 1.3:
    load_score = 100  // Optimal range
else:
    load_score = max(0, 100 - (ratio - 1.3) * 100)  // Penalize overtraining
```

### Readiness Categories
- **90-100**: Peak Performance (green)
- **70-89**: Good (light green)
- **50-69**: Moderate (yellow)
- **30-49**: Low (orange)
- **0-29**: Very Low (red)

## Workout Recommendation Engine

### Recommendation Logic

```swift
func recommendWorkout(recoveryScore: Int, trainingHistory: [Workout]) -> WorkoutRecommendation {

    let lastWorkouts = trainingHistory.last7Days()
    let runningDays = lastWorkouts.filter { $0.type == .running }.count
    let strengthDays = lastWorkouts.filter { $0.type == .strength }.count
    let restDays = lastWorkouts.filter { $0.type == .rest }.count

    // High Recovery
    if recoveryScore >= 80 {
        if strengthDays < 2 {
            return .strength(.fullBody, intensity: .high)
        } else if runningDays < 4 {
            return .running(.tempo, distance: .moderate)
        } else {
            return .strength(.upper, intensity: .moderate)
        }
    }

    // Good Recovery
    else if recoveryScore >= 60 {
        if strengthDays == 0 {
            return .strength(.lower, intensity: .moderate)
        } else {
            return .mobility(.yoga, duration: 30)
        }
    }

    // Moderate Recovery
    else if recoveryScore >= 40 {
        return .mobility(.stretching, duration: 20)
    }

    // Low Recovery
    else {
        return .rest(.active, suggestion: "Light walk or complete rest")
    }
}
```

### Workout Types

#### Strength Workouts
1. **Full Body** (High readiness)
   - Compound movements
   - 45-60 min
   - 3-4 sets, 8-12 reps

2. **Upper Body** (Medium-High readiness)
   - Push/Pull exercises
   - 30-45 min
   - Focus on form

3. **Lower Body** (Medium readiness)
   - Squats, lunges, deadlifts
   - 30-40 min
   - Lighter load if recovering

4. **Core/Stability** (Any readiness)
   - Planks, anti-rotation
   - 20-30 min
   - Low fatigue

#### Mobility Workouts
1. **Yoga Flow** (30-60 min)
2. **Dynamic Stretching** (15-20 min)
3. **Foam Rolling** (10-15 min)
4. **Active Recovery Walk** (20-30 min)

## Data Models (Swift)

```swift
// Core Data Models

struct RecoveryData {
    let date: Date
    let hrvScore: Double
    let restingHR: Int
    let sleepScore: Double
    let trainingLoadScore: Double
    let overallScore: Int
    let category: RecoveryCategory
}

struct HealthMetrics {
    let date: Date
    let hrv: Double?
    let restingHeartRate: Int?
    let sleepDuration: TimeInterval?
    let deepSleepDuration: TimeInterval?
    let remSleepDuration: TimeInterval?
    let workouts: [WorkoutData]
}

struct WorkoutData {
    let id: UUID
    let date: Date
    let type: WorkoutType
    let duration: TimeInterval
    let distance: Double?  // meters
    let averageHeartRate: Int?
    let maxHeartRate: Int?
    let caloriesBurned: Double?
    let trainingStress: Double  // calculated
}

enum WorkoutType {
    case running
    case cycling
    case swimming
    case strength
    case yoga
    case mobility
    case rest
    case other(String)
}

struct WorkoutRecommendation {
    let type: WorkoutType
    let description: String
    let duration: TimeInterval
    let intensity: Intensity
    let exercises: [Exercise]?
}

struct Exercise {
    let name: String
    let sets: Int
    let reps: String  // "8-12" or "30 sec"
    let restPeriod: TimeInterval
    let videoURL: URL?
}

enum Intensity {
    case low, moderate, high
}
```

## iOS App Structure

```
RecoveryApp/
├── App/
│   ├── RecoveryApp.swift          // App entry point
│   └── ContentView.swift           // Main tab view
├── Models/
│   ├── RecoveryData.swift
│   ├── HealthMetrics.swift
│   ├── WorkoutData.swift
│   └── WorkoutRecommendation.swift
├── Services/
│   ├── HealthKitManager.swift     // HealthKit integration
│   ├── RecoveryCalculator.swift   // Score algorithm
│   ├── RecommendationEngine.swift // Workout suggestions
│   └── DataPersistence.swift      // CoreData/SwiftData
├── Views/
│   ├── Dashboard/
│   │   ├── DashboardView.swift    // Main readiness display
│   │   ├── RecoveryScoreCard.swift
│   │   └── MetricsBreakdownView.swift
│   ├── Recommendations/
│   │   ├── WorkoutRecommendationsView.swift
│   │   ├── WorkoutDetailView.swift
│   │   └── ExerciseListView.swift
│   ├── History/
│   │   ├── HistoryView.swift
│   │   ├── TrendChartView.swift
│   │   └── CalendarView.swift
│   └── Settings/
│       ├── SettingsView.swift
│       └── HealthKitPermissionsView.swift
├── ViewModels/
│   ├── DashboardViewModel.swift
│   ├── RecommendationViewModel.swift
│   └── HistoryViewModel.swift
└── Utilities/
    ├── Extensions/
    ├── Constants.swift
    └── Formatters.swift

WatchApp/
├── RecoveryWatchApp.swift
├── Views/
│   ├── ComplicationView.swift
│   └── ScoreGlanceView.swift
└── Models/
    └── SharedModels.swift
```

## HealthKit Permissions Required

```swift
// Read permissions
- HKQuantityType(.heartRateVariabilitySDNN)
- HKQuantityType(.restingHeartRate)
- HKQuantityType(.heartRate)
- HKCategoryType(.sleepAnalysis)
- HKWorkoutType()
- HKQuantityType(.activeEnergyBurned)
- HKQuantityType(.stepCount)
- HKQuantityType(.distanceWalkingRunning)
- HKQuantityType(.respiratoryRate)
```

## Implementation Phases

### Phase 1: Foundation (Week 1)
- [x] Create DEV.md and TECH_SPEC.md
- [ ] Initialize Xcode project with SwiftUI
- [ ] Set up HealthKit integration
- [ ] Request permissions
- [ ] Fetch basic metrics (HRV, RHR, Sleep)

### Phase 2: Core Algorithm (Week 2)
- [ ] Implement RecoveryCalculator
- [ ] Build component scoring (HRV, RHR, Sleep, Training Load)
- [ ] Calculate baseline values
- [ ] Test with sample data

### Phase 3: UI - Dashboard (Week 2-3)
- [ ] Design and build main dashboard
- [ ] Display recovery score with color coding
- [ ] Show metric breakdown
- [ ] Add trend charts

### Phase 4: Recommendations (Week 3-4)
- [ ] Build RecommendationEngine
- [ ] Create workout library
- [ ] Design workout detail views
- [ ] Add exercise instructions

### Phase 5: History & Trends (Week 4-5)
- [ ] Implement data persistence
- [ ] Build historic trend analysis
- [ ] Create calendar view
- [ ] Add weekly planning suggestions

### Phase 6: Apple Watch (Week 5-6)
- [ ] Create Watch app
- [ ] Build complications
- [ ] Quick score glance view
- [ ] Sync with iPhone app

### Phase 7: Polish & Testing (Week 6-7)
- [ ] Test with real data
- [ ] Refine algorithm
- [ ] Performance optimization
- [ ] Bug fixes
- [ ] App Store preparation

## Next Steps
1. Initialize Xcode project
2. Set up HealthKit framework
3. Build HealthKitManager service
4. Implement basic data fetching
5. Create RecoveryCalculator with scoring algorithm
