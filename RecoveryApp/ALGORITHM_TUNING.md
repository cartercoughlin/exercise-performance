# Recovery Algorithm Tuning Guide

## Why Your Score Might Be Low

If your recovery scores are "perpetually super low", here are the likely reasons and how to fix them:

### 1. **Not Enough Baseline Data** (Most Common)

The algorithm compares your current metrics to your personal baseline. You need:
- **7 days** of HRV data for HRV score
- **30 days** of resting HR data for RHR score
- At least **1 day** for sleep and training load

**Solution**: Use the app for 7-30 days to establish accurate baselines.

**Temporary Fix**: The algorithm defaults to a score of 50 when there's no baseline. You can adjust this default.

### 2. **Algorithm is Too Strict**

The current algorithm may be calibrated for elite athletes. Here's how to make it more realistic:

## Adjusting the Algorithm

Edit `RecoveryApp/Services/RecoveryCalculator.swift`

### Option 1: Adjust Component Weights

**Current weights** (line 28):
```swift
let overallScore = Int(
    hrvScore * 0.10 +      // HRV: 15%
    rhrScore * 0.30 +      // RHR: 25%
    sleepScore * 0.30 +    // Sleep: 25%
    trainingLoadScore * 0.30  // Load: 25%
)
```

**Recommendations**:
- If you don't have reliable HRV data: Reduce HRV to 0.20, increase Sleep to 0.35
- If you're a recreational athlete: Increase Training Load to 0.25, reduce HRV to 0.25

### Option 2: Make HRV Score More Forgiving

**Current HRV calculation** (lines 41-56):
```swift
let deviation = ((currentHRV - baseline) / baseline) * 100

if deviation >= 0 {
    score = min(100, 50 + deviation * 2)  // 2x multiplier
} else {
    score = max(0, 50 + deviation * 2)
}
```

**Make it more forgiving** - Change multiplier from 2 to 1.5:
```swift
if deviation >= 0 {
    score = min(100, 50 + deviation * 1.5)
} else {
    score = max(0, 50 + deviation * 1.5)
}
```

Or start higher - Change base from 50 to 60:
```swift
if deviation >= 0 {
    score = min(100, 60 + deviation * 2)
} else {
    score = max(20, 60 + deviation * 2)  // Floor at 20 instead of 0
}
```

### Option 3: Make Resting HR Score More Forgiving

**Current RHR calculation** (lines 59-69):
```swift
let deviation = baseline - Double(currentRHR)
let score = 50 + (deviation * 5)  // 5 points per bpm
```

**Make it less sensitive** - Change from 5 to 3 points per bpm:
```swift
let score = 50 + (deviation * 3)
```

### Option 4: Adjust Sleep Score

**Current sleep calculation** considers:
- Duration (50%)
- Deep sleep % (30%)
- REM sleep % (20%)

If you're not getting perfect sleep stages:

**Edit lines 72-95**, change the optimal targets:
```swift
// Current: Optimal = 8 hours
let optimalHours = 8.0

// Make it more forgiving: Optimal = 7 hours
let optimalHours = 7.0
```

Or reduce the weight of sleep stages if your device doesn't track them well:
```swift
// Current weights
qualityScore = durationScore * 0.5 +
              deepScore * 0.3 +
              remScore * 0.2

// New: Focus more on duration
qualityScore = durationScore * 0.7 +
              deepScore * 0.15 +
              remScore * 0.15
```

### Option 5: Adjust Training Load Thresholds

**Current optimal ratio**: 0.8 - 1.3 (strict)

**Make it more forgiving** (lines 104-116):
```swift
// Current
if ratio < 0.8 {
    score = 60 + (ratio - 0.8) * 100
} else if ratio <= 1.3 {
    score = 100
} else {
    score = max(0, 100 - (ratio - 1.3) * 100)
}

// More forgiving: Wider optimal range
if ratio < 0.7 {  // Changed from 0.8
    score = 60 + (ratio - 0.7) * 100
} else if ratio <= 1.5 {  // Changed from 1.3
    score = 100
} else {
    score = max(0, 100 - (ratio - 1.5) * 80)  // Less penalty
}
```

## Recommended Quick Fix for Recreational Athletes

If you're not an elite athlete and scores seem too low, try this combination:

1. **Adjust weights** to prioritize sleep and training load:
```swift
let overallScore = Int(
    hrvScore * 0.25 +           // Reduced from 0.35
    rhrScore * 0.20 +           // Reduced from 0.25
    sleepScore * 0.35 +         // Increased from 0.25
    trainingLoadScore * 0.20    // Increased from 0.15
)
```

2. **Make HRV more forgiving**:
```swift
if deviation >= 0 {
    score = min(100, 60 + deviation * 1.5)  // Start at 60, multiply by 1.5
} else {
    score = max(30, 60 + deviation * 1.5)   // Floor at 30
}
```

3. **Reduce sleep requirement**:
```swift
let optimalHours = 7.0  // Changed from 8.0
```

## How to Test Your Changes

1. Edit `RecoveryApp/Services/RecoveryCalculator.swift`
2. In Xcode: `Cmd + B` (Build)
3. `Cmd + R` (Run)
4. Tap "How is this calculated?" to see the new breakdown
5. Check if scores are more realistic

## Understanding Your Metrics

Use the **"How is this calculated?"** button in the app to see:
- Current values vs baselines
- Exact calculation for each component
- Why your score is what it is

### Typical Score Ranges

After tuning, you should see:
- **90-100**: Perfect recovery (rare, maybe 1-2x/week)
- **70-89**: Good recovery (most days if training moderately)
- **50-69**: Moderate (after hard training or poor sleep)
- **30-49**: Low (after very hard training)
- **0-29**: Very low (sick, injured, or severely overtrained)

If you're consistently below 50 despite feeling good:
→ The algorithm needs adjustment for your personal physiology

## Advanced: Personal Baseline Adjustment

Everyone's physiology is different. You might naturally have:
- Lower HRV than "average"
- Higher resting HR
- Different sleep patterns

The algorithm learns YOUR baseline, but if scores still seem off after 30 days, adjust the multipliers to match how you actually feel.

**Rule of thumb**: If you feel great but score shows 40, the algorithm is too strict. If you feel terrible but score shows 90, it's too lenient.

## Need Help?

The current algorithm is based on sports science research but may need personalization. Track how you feel vs your score for 2 weeks, then adjust accordingly.
