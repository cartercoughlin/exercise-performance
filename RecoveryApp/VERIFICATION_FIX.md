# Fix "App Not Verified" on iPhone

## The Issue
When you tap "Verify App" on iPhone, it loads but stays "Not Verified". This is usually a signing or Apple ID issue.

## Solutions (Try in Order)

### Solution 1: Check Internet Connection
1. Make sure your iPhone is connected to **Wi-Fi or Cellular Data**
2. Verification requires internet to check with Apple's servers
3. Try again after confirming connection

### Solution 2: Sign Out and Back Into Apple ID on iPhone
1. On iPhone: **Settings → [Your Name] at top**
2. Scroll down and tap **"Sign Out"**
3. Sign back in with your Apple ID
4. Go back to Settings → General → VPN & Device Management
5. Try to verify again

### Solution 3: Change Bundle Identifier in Xcode

The bundle ID might conflict with an existing app. Let's make it unique:

1. In Xcode, select **"RecoveryApp"** project → **"RecoveryApp"** target
2. Go to **"Signing & Capabilities"** tab
3. Find **"Bundle Identifier"**
4. Change from `com.yourcompany.RecoveryApp` to:
   - `com.carter.RecoveryApp` (use your name)
   - Or `com.[yourname].[uniquename]`
5. Press `Cmd + Shift + K` (Clean)
6. Press `Cmd + R` (Run)
7. Try to verify on iPhone again

### Solution 4: Use a Different Apple ID

If you're using a free Apple Developer account:

1. In Xcode: **Xcode → Settings (or Preferences)**
2. Go to **"Accounts"** tab
3. Click **"+"** to add another Apple ID (if you have one)
4. OR remove and re-add your current Apple ID:
   - Select your Apple ID
   - Click **"-"** to remove
   - Click **"+"** to add it back
   - Sign in again
5. Go back to your project:
   - **Signing & Capabilities** tab
   - Change **Team** to the newly added account
6. Clean and Run again

### Solution 5: Delete App from iPhone and Reinstall

1. On iPhone: **Long press the RecoveryApp icon**
2. Tap **"Remove App" → "Delete App"**
3. In Xcode: Press `Cmd + R` to install fresh
4. Try to verify again

### Solution 6: Reset Location & Privacy Settings

Sometimes iOS blocks verification due to privacy settings:

1. On iPhone: **Settings → General → Transfer or Reset iPhone**
2. Tap **"Reset"**
3. Select **"Reset Location & Privacy"**
4. Enter passcode
5. Confirm reset
6. Try to verify the app again

### Solution 7: Use Paid Apple Developer Account

**Free accounts have limitations:**
- Apps expire after 7 days
- Limited number of apps
- Verification can be flaky

If nothing works and you're serious about this app:
- Sign up for **Apple Developer Program** ($99/year)
- Go to: https://developer.apple.com/programs/
- With a paid account, you get:
  - Proper code signing
  - No 7-day expiration
  - App Store distribution
  - TestFlight beta testing

## Alternative: Run Without Verification

If you just want to test quickly and verification keeps failing:

### Option A: Keep Phone Connected
- Keep iPhone plugged into Mac
- Run directly from Xcode (Cmd + R)
- App will run while connected, even without verification

### Option B: Disable Developer Mode Verification (iOS 16+)

1. On iPhone: **Settings → Privacy & Security → Developer Mode**
2. Toggle **Developer Mode** ON
3. Restart iPhone when prompted
4. After restart, you may be able to run apps without manual verification

## What to Check in Xcode

Before trying the solutions above, verify these settings:

1. **Signing & Capabilities** tab shows:
   - ✅ "Automatically manage signing" is checked
   - ✅ Team is selected (your Apple ID)
   - ✅ No red error messages
   - ✅ "Signing Certificate" shows "Apple Development: [Your Name]"

2. **Build Settings** → Search "Code Signing":
   - "Code Signing Identity" = "Apple Development"
   - "Code Signing Style" = "Automatic"

## Common Error Messages

### "Unable to verify app - An internet connection is required"
→ iPhone needs internet connection (Wi-Fi or cellular)

### "Unable to verify app - This app cannot be installed"
→ Bundle ID conflict or Apple ID issue. Try Solution 3 or 4.

### "Untrusted Developer"
→ This is normal! Follow the verification steps.

### "Could not launch RecoveryApp"
→ Developer certificate not trusted yet. Keep trying to verify.

## Still Not Working?

If none of these work, you can still test the app:

1. **Keep iPhone connected to Mac**
2. **Run from Xcode** (Cmd + R)
3. App will work while connected
4. When unplugged, it will stop working until you reconnect

OR

Consider getting a paid Apple Developer account for reliable testing.

---

**Most Common Fix:** Solution 3 (Change Bundle Identifier) + Solution 1 (Check Internet)
