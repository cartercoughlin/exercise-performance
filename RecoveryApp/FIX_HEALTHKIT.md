# Fix HealthKit Permissions - FINAL SOLUTION

Your Xcode project is set to **auto-generate Info.plist**, so it ignores our Info.plist file.

## THE FIX - Add Keys in Build Settings:

### Step 1: Open Build Settings

1. In Xcode: Select **"RecoveryApp"** project → **"RecoveryApp"** target
2. Click **"Build Settings"** tab
3. Click **"All"** at the top (not "Basic")
4. Click **"+"** button (top right, next to search bar)
5. Select **"Add User-Defined Setting"**

### Step 2: Add HealthKit Permission Keys

Add these two settings exactly:

#### First Setting:
- **Key Name**: `INFOPLIST_KEY_NSHealthShareUsageDescription`
- **Value**: `We need access to your health data to calculate your recovery score and provide personalized workout recommendations.`

To add:
1. Click "+" → "Add User-Defined Setting"
2. Double-click "New Setting"
3. Type: `INFOPLIST_KEY_NSHealthShareUsageDescription`
4. Press Tab or Enter
5. Double-click the value column
6. Paste: `We need access to your health data to calculate your recovery score and provide personalized workout recommendations.`

#### Second Setting:
1. Click "+" → "Add User-Defined Setting" again
2. **Key Name**: `INFOPLIST_KEY_NSHealthUpdateUsageDescription`
3. **Value**: `We need permission to save workout data to your Health app.`

### Step 3: Clean and Run

1. Press `Cmd + Shift + K` (Clean Build Folder)
2. Press `Cmd + R` (Run)

**The app should now launch!** 🎉

---

## Alternative: Disable Auto-Generate (More Permanent)

If the above doesn't work, force Xcode to use our Info.plist:

1. **Build Settings** tab
2. Search: `Generate Info`
3. Find: **"Generate Info.plist File"**
4. Change to: **"No"**
5. Clear search
6. Search: `Info.plist File`
7. Find: **"Info.plist File"**
8. If empty, set to: `RecoveryApp/Info.plist`
9. Clean and Run

This makes Xcode use our Info.plist file with all the permissions already set.

---

## Why This Happened

Modern Xcode projects (created with SwiftUI) auto-generate Info.plist and ignore custom Info.plist files unless you:
- Set `GENERATE_INFOPLIST_FILE = NO`, OR
- Add permissions as `INFOPLIST_KEY_` settings in Build Settings

Your project was created with auto-generation enabled, so we need to add the keys the "new" way.
