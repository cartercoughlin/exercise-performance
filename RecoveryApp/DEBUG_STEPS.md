# Debug: App Won't Run on iPhone

## Step 1: Check Build Output in Xcode

When you press `Cmd + R`, what happens?

1. **Open Debug Console** in Xcode:
   - Press `Cmd + Shift + Y` (or View → Debug Area → Show Debug Area)
   - This shows at the bottom of Xcode

2. **Press `Cmd + R` to run**

3. **Look for errors in the console**. Common messages:

### Scenario A: "Build Succeeded" but app doesn't launch
```
Build succeeded
Installing...
[iPhone Name]
```
Then nothing happens or shows error.

**Solution:** Developer Mode might be off

### Scenario B: "Failed to install app"
```
error: Failed to install the requested application
An application bundle was not found at the provided path.
```

**Solution:** Build didn't complete properly

### Scenario C: "Code signing error"
```
error: Signing for "RecoveryApp" requires a development team.
```

**Solution:** Need to select Team in Signing & Capabilities

### Scenario D: "AMDeviceSecureStartService"
```
error: AMDeviceSecureStartService(device, CFSTR("com.apple.debugserver")...
```

**Solution:** iPhone needs Developer Mode enabled

## Step 2: Enable Developer Mode on iPhone (iOS 16+)

**This is probably your issue!**

1. On iPhone: **Settings → Privacy & Security**
2. Scroll down to **Developer Mode**
3. Toggle it **ON**
4. iPhone will ask to restart - tap **Restart**
5. After restart, you'll see a warning - tap **Turn On** to confirm
6. Enter your passcode

Then in Xcode:
- Press `Cmd + R` again
- App should install and launch!

## Step 3: Check Signing & Capabilities

1. In Xcode: Select "RecoveryApp" project → "RecoveryApp" target
2. **"Signing & Capabilities"** tab
3. Take a screenshot or tell me what you see:
   - Is "Automatically manage signing" checked?
   - What does "Team" show?
   - Are there any red error messages?
   - What is the "Bundle Identifier"?
   - Does it show "Signing Certificate: Apple Development: [name]"?

## Step 4: Check Your iPhone is Recognized

1. In Xcode, at the top toolbar, what does the device dropdown show?
   - Should show your iPhone name (e.g., "Carter's iPhone")
   - NOT "iPhone 16" or "Any iOS Device (arm64)"

2. If it shows "Unavailable" or has a warning icon:
   - Unplug iPhone
   - Unlock iPhone
   - Plug back in
   - Wait for "Preparing iPhone for Development..." to finish

## Step 5: Check Build Logs

1. After pressing `Cmd + R`, press `Cmd + 9` to open **Report Navigator**
2. Click the latest build (top of the list)
3. Look for any errors marked with ⛔️ or ⚠️
4. Tell me what errors you see

## Step 6: Fresh Start

Try a complete reset:

```bash
# In Xcode:
1. Press Cmd + Shift + K (Clean Build Folder)
2. Product → Clean Build Folder (wait to complete)

# Close Xcode completely
3. Quit Xcode (Cmd + Q)

# Delete derived data:
4. Open Terminal
5. Run this command:
```

```bash
rm -rf ~/Library/Developer/Xcode/DerivedData/RecoveryApp-*
```

```bash
6. Open Xcode again
7. Open RecoveryApp.xcodeproj
8. Select your iPhone
9. Press Cmd + R
```

## Step 7: Verify Bundle Identifier Uniqueness

Your Bundle ID might conflict. Try a completely unique one:

1. **Signing & Capabilities** tab
2. Change Bundle Identifier to: `com.carter.RecoveryApp-` + random numbers
   - Example: `com.carter.RecoveryApp-20241122`
3. This ensures no conflicts
4. Clean and Run

## Step 8: Check iPhone Storage

1. On iPhone: **Settings → General → iPhone Storage**
2. Make sure you have at least **1GB free**
3. If low on space, delete some apps/photos

## What to Tell Me:

To help you better, please tell me:

1. **What happens when you press Cmd + R in Xcode?**
   - Does it say "Build Succeeded"?
   - Does it say "Installing..."?
   - What's the last message you see?

2. **In Signing & Capabilities tab:**
   - What does "Status" show under Signing?
   - Any red error text?

3. **iOS Version on your iPhone:**
   - Settings → General → About → Software Version
   - Is it iOS 16 or later?

4. **Is Developer Mode enabled on iPhone?**
   - Settings → Privacy & Security → Developer Mode
   - Is it ON?

5. **Do you see RecoveryApp icon on iPhone home screen?**
   - Even if it won't open, is the icon there?

---

## Most Likely Fix:

**Enable Developer Mode on iPhone** (Step 2 above)

iOS 16+ requires Developer Mode to be explicitly enabled. This is the #1 reason apps won't install from Xcode.
