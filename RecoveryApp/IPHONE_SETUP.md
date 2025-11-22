# Running RecoveryApp on Your iPhone

## Why You Need a Real iPhone

**HealthKit does NOT work on the Simulator.** You must use a physical iPhone to test this app because:
- HealthKit requires real hardware
- Apple Watch data syncs only to real devices
- Garmin/Strava sync only works on real devices

## Step-by-Step Guide

### 1. Connect Your iPhone

1. **Plug in your iPhone** to your Mac using a USB cable
2. **Unlock your iPhone**
3. If prompted on iPhone: **Tap "Trust This Computer"**
4. Enter your iPhone passcode

### 2. Configure Xcode Project

#### A. Add Info.plist Reference
1. In Xcode, click **"RecoveryApp"** project (blue icon at top of navigator)
2. Select **"RecoveryApp"** under TARGETS (not the project)
3. Click **"Build Settings"** tab
4. Search for **"Info.plist"**
5. Find **"Info.plist File"** setting
6. Set value to: **`RecoveryApp/Info.plist`**

#### B. Add Entitlements File
1. Still in **Build Settings**
2. Search for **"Code Signing Entitlements"**
3. Set value to: **`RecoveryApp/RecoveryApp.entitlements`**

#### C. Add HealthKit Capability
1. Click **"Signing & Capabilities"** tab
2. Click **"+ Capability"** button (top left)
3. Search for **"HealthKit"**
4. Double-click **"HealthKit"** to add it
5. You should see "HealthKit" appear in the capabilities list

#### D. Configure Signing
1. Still in **"Signing & Capabilities"** tab
2. Under **"Signing"** section:
   - **Automatically manage signing**: ✅ Checked
   - **Team**: Select your Apple ID / Team
   - If you don't have a team, click "Add Account" and sign in with your Apple ID (free)
3. Xcode will automatically create a provisioning profile

### 3. Select Your iPhone as Target

1. At the top of Xcode window, find the **device dropdown**
   - It probably says "iPhone 16" (Simulator) right now
2. Click it and select **your actual iPhone name**
   - It will show under "iOS Device" section
   - Example: "Carter's iPhone"

### 4. Build and Run

1. **Clean Build Folder**: Press `Cmd + Shift + K`
2. **Build**: Press `Cmd + B`
   - Wait for build to complete
   - Fix any errors if they appear
3. **Run**: Press `Cmd + R` (or click ▶️ button)

### 5. First Launch on iPhone

#### On Your iPhone:
1. The app will try to install
2. You may see an error: **"Untrusted Developer"**
3. If so, go to iPhone Settings:
   - **Settings → General → VPN & Device Management**
   - Find your Apple ID or certificate
   - Tap it and tap **"Trust"**
4. Go back to Xcode and run again (`Cmd + R`)

#### Grant Permissions:
1. App will launch on your iPhone
2. You'll see a permission prompt for **HealthKit**
3. Tap **"Turn All Categories On"**
4. Tap **"Allow"**

### 6. Verify Data Sources

For the app to work, you need health data:

#### Apple Health App:
1. Open **Health** app on iPhone
2. Check you have data for:
   - Heart Rate Variability (HRV)
   - Resting Heart Rate
   - Sleep
   - Workouts
   - Steps

#### Sync Garmin:
1. Open **Garmin Connect** app
2. **More → Settings → Health & Fitness Apps → Apple Health**
3. Enable all categories:
   - ✅ Heart Rate
   - ✅ Heart Rate Variability
   - ✅ Sleep
   - ✅ Workouts
   - ✅ Steps
   - ✅ Active Energy

#### Sync Strava:
1. Open **Strava** app
2. **Profile → Settings → Applications, Services and Devices → Health**
3. Enable **"Write Data"** toggle
4. Select all data types

### 7. Test the App

1. App should display your **recovery score** (0-100)
2. Tap around and explore:
   - **Recovery tab**: See your score breakdown
   - **History tab**: (Coming soon)
   - **Settings tab**: Verify HealthKit is authorized

## Troubleshooting

### "No data available"
- Check Apple Health app has data
- Wait 24 hours after enabling Garmin/Strava sync
- Need at least 1 day of sleep + HRV data

### Build errors about signing
- Make sure you selected a Team in Signing & Capabilities
- Try toggling "Automatically manage signing" off and on

### "Could not launch RecoveryApp"
- Check iPhone is unlocked
- Check you trusted the developer certificate
- Try unplugging and reconnecting iPhone

### Low/zero recovery score
- App needs 7 days of data for accurate baselines
- First few days may show inaccurate scores

### "Code Signing Error"
- You need a **paid Apple Developer account** ($99/year) for full deployment
- OR use a **free Personal Team** (limited to 7 days, must reinstall weekly)

## Quick Reference Commands

| Action | Keyboard Shortcut |
|--------|------------------|
| Clean Build | `Cmd + Shift + K` |
| Build | `Cmd + B` |
| Run | `Cmd + R` |
| Stop | `Cmd + .` |
| Show Debug Console | `Cmd + Shift + Y` |

## What You Should See

Once running successfully:
- ✅ App launches on your iPhone
- ✅ Shows recovery score (0-100) with color
- ✅ Displays today's metrics (HRV, RHR, Sleep, Steps)
- ✅ Recommends a workout based on recovery

## Next Steps

After getting it running:
1. Use the app for **7 days** to establish baselines
2. Track how your recovery score correlates with how you feel
3. Adjust algorithm weights if needed (see `Services/RecoveryCalculator.swift`)
4. Consider adding features from the roadmap

---

**Remember:** HealthKit only works on real iPhones, not Simulator!
