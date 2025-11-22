# Recovery & Readiness iOS App - Development Log

## Project Overview
Building an iOS app that creates a recovery/readiness score based on Garmin, Strava, and Apple Health data. The app will suggest personalized strength and mobility workouts based on recovery status and historic training trends.

## Goals
- Calculate daily recovery/readiness score
- Sync with Apple Watch and/or Apple Health
- Suggest strength/mobility workouts that balance with readiness
- Use historic data to suggest weekly training plans
- Track metrics: heart rate, HRV, sleep, running mileage, activity data, yoga

## Tech Stack (To Be Decided)

### Backend Options
- Python (FastAPI or Flask) for REST API
- Existing Python scripts for Garmin/Strava data
- PostgreSQL or SQLite for historic data
- scikit-learn for ML/trend analysis

### iOS App
- SwiftUI for UI
- HealthKit for Apple Health integration
- WatchKit for Apple Watch companion
- Combine for reactive data flow
- CoreML for on-device predictions (optional)

## Architecture Decisions Needed

### 1. Data Integration Strategy
- **Option A**: Apple Health as primary source (HealthKit)
  - Simpler, native iOS integration
  - Requires Garmin/Strava to sync to Apple Health first
  - Better privacy, works offline

- **Option B**: Direct API integration with Garmin/Strava
  - More complex authentication
  - Requires backend server
  - Direct access to all metrics

- **Option C**: Hybrid approach
  - Primary data from Apple Health
  - Supplemented with direct API calls for missing metrics

### 2. Algorithm Location
- **On-Device (Swift)**: Better privacy, works offline, no server costs, harder to update
- **Server-Side (Python)**: Easier to iterate, can use complex ML models, requires hosting

### 3. MVP Feature Priority
- Daily readiness score calculation
- Workout recommendations (strength/mobility)
- Historic trend analysis for weekly planning
- Apple Watch complications/glance view

## Key Metrics for Recovery Score

### Primary Metrics
1. **Heart Rate Variability (HRV)** - Most important recovery indicator
2. **Resting Heart Rate** - Current vs baseline, trend analysis
3. **Sleep Quality** - Duration, REM/deep sleep percentages
4. **Sleep Duration** - Total hours

### Training Load Metrics
5. **Recent Mileage** - 7-day running volume
6. **Training Intensity** - Heart rate zones, pace
7. **Activity Balance** - Running, strength, yoga, rest days
8. **Acute:Chronic Workload Ratio** - Injury risk indicator

### Optional/Subjective
9. **Soreness Level** - User-reported (1-10 scale)
10. **Perceived Energy** - User-reported

## Workout Recommendation Logic (Draft)

### High Readiness (80-100%)
- Full strength training sessions
- High-intensity intervals
- Long runs
- Max effort workouts

### Medium Readiness (50-79%)
- Moderate strength training
- Tempo runs
- Mobility-focused sessions
- Technique work

### Low Readiness (<50%)
- Active recovery only
- Yoga/stretching
- Easy walking
- Complete rest day

## Development Phases

### Phase 1: Data Collection & Backend
- [ ] Set up backend API infrastructure
- [ ] Build data aggregation from Garmin/Strava/Apple Health
- [ ] Create data models and database schema
- [ ] Implement data sync mechanism

### Phase 2: Recovery Algorithm
- [ ] Research and design recovery scoring algorithm
- [ ] Implement HRV, RHR, sleep analysis
- [ ] Calculate training load metrics
- [ ] Build baseline/trend calculation
- [ ] Test and validate scoring accuracy

### Phase 3: Recommendation Engine
- [ ] Design workout recommendation logic
- [ ] Implement strength/mobility workout library
- [ ] Create historic trend analysis
- [ ] Build weekly planning algorithm
- [ ] Balance recommendations with training schedule

### Phase 4: iOS App Foundation
- [ ] Initialize iOS project with SwiftUI
- [ ] Set up HealthKit integration
- [ ] Implement data fetching from backend/HealthKit
- [ ] Create data models in Swift
- [ ] Build data persistence layer

### Phase 5: UI/UX
- [ ] Design main dashboard with readiness score
- [ ] Build workout recommendation views
- [ ] Create historic data visualization
- [ ] Implement settings and preferences
- [ ] Add user input for subjective metrics

### Phase 6: Apple Watch
- [ ] Create WatchOS companion app
- [ ] Implement watch complications
- [ ] Build quick-glance readiness view
- [ ] Add workout logging from watch

### Phase 7: Testing & Refinement
- [ ] Test with real user data
- [ ] Validate recovery score accuracy
- [ ] Refine recommendation algorithms
- [ ] Performance optimization
- [ ] Bug fixes

## Current Status
**Phase**: MVP Implementation Complete
**Last Updated**: 2025-11-22

### ✅ Completed (MVP v1.0)
- Data models for recovery, health metrics, and workouts
- HealthKit integration with data fetching
- Recovery score calculation algorithm
- Workout recommendation engine
- SwiftUI dashboard with recovery score display
- Workout detail views with exercise instructions
- Settings and permissions management
- Complete app structure ready for Xcode

## Architecture Decisions ✓

### ✓ Data Source: Apple HealthKit
- Using HealthKit as single source of truth
- Garmin and Strava sync to Apple Health automatically
- Native iOS integration, better privacy
- Works offline, no backend server needed

### ✓ Algorithm Location: On-Device (Swift)
- Recovery algorithm runs entirely on iPhone/Watch
- Better privacy - data never leaves device
- Works offline
- No server hosting costs
- Lower latency

### MVP Feature Set
1. **Daily readiness score** - Core feature (Priority 1)
2. **Workout recommendations** - Strength/mobility suggestions (Priority 1)
3. **Historic trend analysis** - Weekly planning (Priority 2)
4. **Apple Watch integration** - Quick glance view (Priority 2)

## Notes & Decisions
- ✓ Data source decided: Apple HealthKit
- ✓ Algorithm location: On-device (Swift)
- Need to verify all required metrics available in HealthKit (HRV, sleep stages, resting HR)
- Garmin and Strava already sync to Apple Health on iOS
- No backend server needed - simplified architecture!

## Xcode Project Structure

The iOS app is located at: `RecoveryApp/RecoveryApp/`

```
RecoveryApp/RecoveryApp/
├── RecoveryApp.xcodeproj/          # Xcode project
├── RecoveryApp/                     # Main app target
│   ├── RecoveryApp.swift            # App entry point
│   ├── ContentView.swift            # Main tab navigation
│   ├── Models/
│   │   ├── WorkoutType.swift
│   │   ├── HealthMetrics.swift
│   │   ├── WorkoutData.swift
│   │   ├── RecoveryData.swift
│   │   └── WorkoutRecommendation.swift
│   ├── Services/
│   │   ├── HealthKitManager.swift
│   │   ├── RecoveryCalculator.swift
│   │   └── RecommendationEngine.swift
│   ├── ViewModels/
│   │   └── DashboardViewModel.swift
│   ├── Views/
│   │   ├── Dashboard/
│   │   │   ├── DashboardView.swift
│   │   │   └── RecoveryScoreCard.swift
│   │   ├── Recommendations/
│   │   │   └── WorkoutDetailView.swift
│   │   ├── History/
│   │   │   └── HistoryView.swift
│   │   └── Settings/
│   │       └── SettingsView.swift
│   └── Assets.xcassets/
├── RecoveryAppTests/                # Unit tests
├── RecoveryAppUITests/              # UI tests
└── Info.plist                       # HealthKit permissions
```

## Resources
- **iOS App**: `RecoveryApp/RecoveryApp/` (Open RecoveryApp.xcodeproj in Xcode)
- **Documentation**:
  - `TECH_SPEC.md` - Technical specification and algorithms
  - `README.md` - Project overview
- **Legacy Python Scripts**:
  - Strava API integration: `main.py`
  - Garmin integration: `garmin.py`
  - Heart rate analysis: `analyze_heart_rate.py`

## Next Steps

### Immediate (Testing & Refinement)
1. Open `RecoveryApp/RecoveryApp/RecoveryApp.xcodeproj` in Xcode
2. Enable HealthKit capability in Signing & Capabilities
3. Run on physical iPhone (Simulator doesn't support HealthKit)
4. Test with real Garmin/Strava data synced to Apple Health
5. Refine algorithm weights based on actual results

### Short-term (Features)
6. Add historic data visualization (charts, trends)
7. Implement weekly planning recommendations
8. Create Apple Watch companion app
9. Add workout tracking functionality
10. Custom workout builder

### Long-term (Enhancements)
11. Machine learning for personalized baselines
12. Push notifications for daily scores
13. Export data functionality
14. Social features for training partners
