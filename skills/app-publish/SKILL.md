---
name: app-publish
description: |
  A strict release gate and publishing guide for mobile apps (Flutter first, with notes for native iOS, native Android and React Native). Runs the whole pipeline from code review and pre-flight checks to versioning, changelog, Play Store and App Store upload, staged rollout, phased release, TestFlight, forced updates and code-push patches. Use whenever the user wants to publish or release the app, push to the Play Store or App Store, create a release or production build, bump the app version, prepare a store submission, upload to TestFlight, or asks "is my app ready to ship", "let's publish", "push to play store", "push to app store", "release this version", "prepare a release", "time to release", "submit to Apple", "run pre-flight". Also trigger on app versioning, version codes, store compliance, release checklist, changelog or "What's New" text, staged rollout, phased release, forced update, update dialog, Play Console, App Store Connect, privacy or data safety forms. It also owns code-push (Shorebird): it decides whether a change ships as a live over-the-air patch or a full store release, so trigger on "push a patch", "send a live update", "OTA update", "hotfix over the air", "ship this without a store release" or "shorebird patch". Strict by design: every check runs every time, nothing is skippable.
---

# app-publish

The final gate before any version of your app reaches users. Every release, a one-line fix or a major feature, goes through the exact same verified process. No shortcuts. No "just this once." Consistency is the whole point.

> **One line:** it reads what went wrong last time, decides patch or full release, reviews and checks the code, makes you test the app by hand, writes the version notes and store copy, then walks you through the upload, the rollout and the forced-update switch.

It was built and proven on a Flutter app shipped to both stores. Flutter is the main path. Where native iOS, native Android or React Native differ, this skill says so. When it does not know the exact steps for your framework, it tells you to check your framework's docs instead of guessing.

---

## First run: set up your project

Every later step reads from one file in the root of the user's repo: **`.app-publish.json`**. If it does not exist, create it before doing anything else.

1. **Detect what you can.** Read the project to prefill values:
   - Flutter: `pubspec.yaml` (name, version), `android/app/build.gradle(.kts)` (`applicationId`), `ios/Runner.xcodeproj/project.pbxproj` (`PRODUCT_BUNDLE_IDENTIFIER`).
   - Native or React Native: the same Android Gradle file and Xcode project, wherever they live.
   - `shorebird.yaml` in the app folder means Shorebird is set up.
   - A Supabase or Firebase client in the code hints at the forced-update backend. Ask, do not assume.
2. **Ask the user for the rest**, in one short list. Only ask what you could not detect.
3. **Write the file** and show it to the user. It holds no secrets and is safe to commit.
4. **Create the release history file** at the path in the config if it is missing, with an empty `## Release lessons` section at the top.

Example:

```json
{
  "app_name": "My App",
  "framework": "flutter",
  "app_dir": ".",
  "platforms": ["android", "ios"],
  "conventions": "Short note on rules a reviewer should enforce, e.g. state management and design system",
  "release_history_file": "docs/releases/version_history.md",
  "build_guide": "docs/RELEASE_BUILD_GUIDE.md",
  "build_defines_file": ".dart_define.json",
  "privacy_policy_url": "https://example.com/privacy",
  "accounts": {
    "has_user_accounts": true,
    "delete_account_in_app": "Settings > Delete account",
    "delete_account_web_url": "https://example.com/delete-account"
  },
  "android": {
    "package_name": "com.example.myapp",
    "play_console_account": "Example Developer Account",
    "keystore_path": "android/app/upload-keystore.jks",
    "store_url": "https://play.google.com/store/apps/details?id=com.example.myapp"
  },
  "ios": {
    "bundle_id": "com.example.myapp",
    "app_store_connect_team": "Example Team",
    "app_store_id": "",
    "export_options_plist": "ios/exportOptions.plist",
    "supports_ipad": false,
    "store_url": ""
  },
  "manual_test": {
    "main_screens": ["Home", "Settings"],
    "core_flows": ["Sign up", "Create the main item", "Edit it"],
    "extra_checks": ["Dark mode renders correctly", "App lock works if enabled"]
  },
  "forced_update": {
    "backend": "none",
    "supabase_table": "app_version",
    "update_service": "UpdateService",
    "update_dialog": "UpdateDialog"
  },
  "code_push": "none"
}
```

| Field | What it is |
|---|---|
| `app_name` | The name used in reports and store consoles. |
| `framework` | `flutter`, `native` or `react-native`. |
| `app_dir` | Folder with the app code, relative to the repo root. All paths below are relative to it. |
| `platforms` | `["android"]`, `["ios"]` or both. |
| `conventions` | One or two lines on house rules the code review should check. Optional. |
| `release_history_file` | The release record this skill reads first and writes last. |
| `build_guide` | Optional doc with exact release build commands and one-time production auth setup. |
| `build_defines_file` | Optional file of build-time defines (Flutter `--dart-define-from-file`). |
| `privacy_policy_url` | Your public privacy policy. Both stores need one. |
| `accounts` | Whether users can create accounts, and where they delete them (in app and on the web). |
| `android.*` | Package name, Play Console account name, upload keystore path, Play listing URL. |
| `ios.*` | Bundle id, App Store Connect team name, numeric App Store id (blank until Apple assigns it), export options path, iPad support, App Store URL. |
| `manual_test` | The screens and flows you must tap through by hand before every release. |
| `forced_update.backend` | `supabase`, `firebase-remote-config`, `custom` or `none`. `none` skips the forced-update module. |
| `forced_update.*` | Table name (Supabase), and the names of your update check service and dialog in code. |
| `code_push` | `shorebird` or `none`. `none` skips the code-push module. |

**Never store secrets in this file.** Signing passwords, API keys, Apple ID credentials and store tokens stay in the user's keychain, environment or CI secrets. This skill never reads or prints key contents.

Every later step says `config.<field>` when it reads from this file. If a field is missing when a step needs it, stop and ask, then save the answer to the file.

---

## The order (never changes)

1. **Phase 0:** Read what happened last time
2. **Phase 1:** Route the release: live patch or full store release
3. **Phase P:** Code-push patch (only if routed to patch)
4. **Platform selection**
5. **Phase 2:** Code review and security audit
6. **Phase 3:** Pre-flight checks
7. **Phase 4:** Fix, re-verify and manual testing
8. **Phase 5:** Version documentation
9. **Phase 6:** Publish

---

## Phase 0: Read what happened last time (mandatory, before anything else)

Every publish starts by reading the release record, so a past mistake is never repeated. Do this before routing, before review, before any build.

1. Read `config.release_history_file` **in full**, not just the version numbers:
   - the **Release lessons** section at the top. Every lesson there becomes a check in this run and must show as PASS or FAIL in the Pre-Flight Report;
   - the **last two release entries**: status (approved, rejected, in review), any store rejection text, and their *Open follow-ups carried forward*;
   - any follow-up that says "will soon be required", "deprecated" or "warning". If the toolchain changed since the last approved release (new Xcode or iOS SDK, new Flutter, new Android Gradle Plugin or target SDK), such a follow-up is a **BLOCKER**, not a note. It must be done or proven harmless before building.
2. Record the toolchain for this release and compare it with the last approved release. For example `xcodebuild -version`, `xcrun --sdk iphoneos --show-sdk-version`, and your framework's version command (`flutter --version` for Flutter). A changed major SDK means a launch test on the newest OS simulator, iPhone **and** iPad, before upload (see 3.4).
3. Read the build output of this release for warnings. Any warning that matches a carried-forward follow-up fails the check until it is resolved.
4. Show the result at the top of the Phase 2 report:

```
LESSONS FROM PAST RELEASES
  Last release: v{x} ({build}), {status}: {one line on what happened}
  Toolchain: Xcode {a} -> {b}, iOS SDK {a} -> {b}, {framework} {a} -> {b}
  Lessons checked: {N}  passed: {n}  failed: {n}
  Carried follow-ups now blocking: {list or "none"}
```

5. After any store rejection, or a problem found after upload, add a lesson to the **Release lessons** section (date, what happened, root cause, the check that now prevents it). If it is a new kind of check, add it to this skill's checklists too. Record the toolchain in every release entry.

Why this matters: a real app was rejected by Apple for a build warning that had been copied forward, unread, for several releases. The warning said the requirement was coming. Then the new SDK made it real.

---

## Phase 1: Route the release (live patch or full store release)

**Skip this phase if `config.code_push` is `none`.** Every change is then a full store release. Go to Platform selection.

With code-push (Shorebird), a change reaches users one of two ways. Decide which before any other work:

- **Live patch:** Dart-only changes ship **over the air in minutes, with no store review**. Use for bug fixes, UI tweaks, copy changes, logic. Users get it on the next app launch.
- **Full store release:** native changes, new dependencies, a version code bump, or the first release of a version. These must go through the store (AAB or IPA, plus review).

### Decision rule: classify the diff since the last release

Compute the changed files since the last release tag, or the last version in `config.release_history_file`. Route as a **FULL RELEASE** if ANY of these are true:

- `android/**` or `ios/**` changed (native code or config)
- `pubspec.yaml` **dependencies** were added, removed or upgraded (native plugin code cannot be patched)
- the build number (`+N` in `pubspec.yaml`) was bumped
- the Flutter or Dart SDK version changed
- the app icon, name, permissions, entitlements or signing changed
- assets were added or changed that the binary must bundle
- there is **no existing Shorebird release** for the current version (you can only patch a version you already released through Shorebird)

Otherwise, if **only `lib/**` Dart (and docs or tests) changed, on top of an existing Shorebird release of the current version**, the change is **PATCH-eligible**.

**MANDATORY: the user personally approves the route every time.** The classifier only *recommends*. The skill NEVER auto-routes and NEVER proceeds (no build, no patch, no upload) until the user explicitly chooses `patch` or `release` for this change. The user may always override the recommendation, for example to force a full release for a Dart-only change. A patch may **never** carry a native change. **When in doubt, full release.**

```
RELEASE ROUTING: {config.app_name}
==================================
Changed since v{last}: {N} files
  Native (android/ios):     {yes/no}
  Dependencies:             {yes/no}
  Version code bumped:      {yes/no}
  Dart-only (lib/**):       {yes/no}
  Shorebird release exists: {yes/no}

Recommendation: {LIVE PATCH / FULL STORE RELEASE}
Reason: {one line}

Confirm or override? [patch / release]
```

### Routing
- **PATCH:** go to **Phase P** and skip the store phases entirely.
- **FULL RELEASE:** continue to Platform selection and Phases 2 to 6. Build the release with **`shorebird release`** (not plain `flutter build`) so the version stays patchable afterward.

> **Other frameworks.** Shorebird is a Flutter tool, and the patch rules above were written for it. React Native and native apps have their own over-the-air options with their own limits on what can be patched. If you use one, check that tool's docs for what is patchable and write your own rule in this phase. Keep the same two hard rules: the user approves the route every time, and native changes always go through the store.

---

## Phase P: Code-push patch (live update)

Only reached when Phase 1 classified the change as PATCH-eligible and the user chose `patch`. A live patch hits users instantly, so the bar is the **same as a release**. Do not relax it.

### P.1 Pre-patch gate
- `flutter analyze`: zero errors, zero warnings.
- `flutter test`: all green.
- Code review of the changed Dart (Phase 2 review, scoped to the diff).
- **Re-run the Phase 1 classifier.** If native code, dependencies or assets slipped in, STOP. This is not patchable. Switch to a full release.
- Confirm a Shorebird release exists for the current version on each target platform (`shorebird release list` or your Shorebird console). You can only patch a released version.

### P.2 Build and push the patch
Use the same build defines as a release (credentials plus a version stamp):

```bash
shorebird patch android \
  --dart-define-from-file={config.build_defines_file} \
  --dart-define=BUILD_DATE=$(date +%Y-%m-%d) \
  --dart-define=GIT_SHA=$(git rev-parse --short HEAD)
# and/or: shorebird patch ios  (same flags)
```

Drop the `--dart-define-from-file` line if `config.build_defines_file` is not set. Review the patch summary Shorebird prints (which release it patches, how much of the app changed). Confirm before pushing. **Commit first** so `GIT_SHA` is real.

### P.3 Document
- Commit the change and push to your remote (the source of truth). Ask before pushing.
- Append a **PATCH** entry to `config.release_history_file`: which release and version code it patches, the **patch number**, date, commit SHA, and what changed. Patches do **not** bump the version code. Record the patch number instead.
- No forced-update change, no store upload, no git tag, no version code bump.

### P.4 Report
```
PATCH PUSHED: {config.app_name} v{version} (patch {N})
  Patches release: build {code}
  Delivered: over the air, on users' next app launch
  Commit: {sha}
  Note: native changes still require a full store release.
```

---

## Platform selection

Read `config.platforms`. If it lists one platform, use it. If it lists both, ask:

```
Which platform are you publishing to?
  1. Android (Google Play)
  2. iOS (App Store)
  3. Both (Android first, then iOS, one after the other)
```

If the user's message makes the platform clear ("push to play store", "submit to TestFlight"), skip the question.

When publishing to **Both**, run Phase 2 and Phase 3 code checks once (they are shared), then build and verify both the AAB and the IPA. Phase 5 writes store copy for both stores. Phase 6 runs Android first, then iOS.

---

## Phase 2: Code review and security audit

Before any technical checks, review the code that is about to ship. This phase is platform-independent: the same app code ships to both stores.

### 2.1 Scope
- Run `git diff` against the last version tag (or the version in `config.release_history_file`).
- Collect the list of changed files.
- This scope defines what gets reviewed: not the whole codebase, just what is shipping.

### 2.2 Code review
Use a code review agent or skill if your agent has one. Otherwise run a fresh subagent with no prior context. Review all changed code for:

- logic errors and bugs
- code quality issues
- the project's own conventions (`config.conventions`, plus any `CLAUDE.md` or `AGENTS.md` in the repo)
- performance concerns
- accessibility issues

The review must come back clean: no high-severity issues. Medium-severity issues are warnings and do not block. Low-severity issues are noted for later.

### 2.3 Security audit
Scan all changed code for:

| Security check | What to look for |
|---|---|
| **Data exposure** | User data logged, shown in debug views, or sent to analytics without consent |
| **Input validation** | Unvalidated user input that could crash the app or cause unexpected behavior |
| **Storage security** | Sensitive data stored in plain text (for example shared preferences instead of secure storage) |
| **Network security** | HTTP instead of HTTPS, missing certificate pinning for sensitive endpoints |
| **API key handling** | Keys hardcoded in app code instead of build-time config |
| **Deep link injection** | Unvalidated deep link parameters that could open unintended screens |
| **Dependency vulnerabilities** | Outdated packages with known security issues |

Check dependencies for updates and known issues. Flutter: `flutter pub outdated`. Other frameworks: use your package manager's outdated and audit commands.

### 2.4 Phase 2 report

```
CODE REVIEW AND SECURITY AUDIT: {config.app_name} v{version}
============================================================
{Lessons from past releases block from Phase 0}

Scope: {N} files changed since v{previous}

Code Review
  [PASS/FAIL] {N} high-severity issues
  [WARN] {N} medium-severity issues
  [INFO] {N} low-severity issues
  {each high/medium issue with file:line}

Security Audit
  [PASS/FAIL] Data exposure: {result}
  [PASS/FAIL] Input validation: {result}
  [PASS/FAIL] Storage security: {result}
  [PASS/FAIL] Network security: {result}
  [PASS/FAIL] API key handling: {result}
  [PASS/FAIL] Deep link safety: {result}
  [PASS/FAIL] Dependencies: {N} outdated, {N} vulnerable

Result: {ALL CLEAR / BLOCKED: fix {N} issues before proceeding}
```

Any high-severity review issue or any security failure blocks the publish. Fix it and re-run this phase.

---

## Phase 3: Pre-flight checks

Run every check below. Report results as they complete. If ANY check fails, still run all the others before stopping, so the user sees everything to fix at once.

All paths are relative to `config.app_dir`.

### 3.1 Code quality (shared, both platforms)

The commands are Flutter. For other frameworks, use your project's linter, type checker and test runner with the same pass bar.

| Check | Command / method | Pass criteria |
|---|---|---|
| Static analysis | `flutter analyze` | Zero errors, zero warnings |
| Tests | `flutter test` | All tests pass |
| Debug code scan | Grep `lib/` for `print(`, `debugPrint(`, `kDebugMode` (other frameworks: `console.log`, `NSLog`, `Log.d` and similar) | None in production code (ignore `debug/` or `dev/` folders) |
| Secrets scan | Grep the app code for hardcoded keys, passwords, tokens | None found. Look for `sk-`, `key=`, `password=`, `Bearer `, `apiKey:`, base64-encoded credentials |
| TODO/FIXME in changed files | Grep files changed since the last release for `TODO`, `FIXME`, `HACK`, `XXX` | None in files changed for this release |
| Unused imports | Caught by static analysis | Zero |
| Localization | `flutter gen-l10n` if the app is localized | Runs clean, no missing keys |
| Past lessons | Every lesson from Phase 0 | Each one PASS |

### 3.2 Version integrity (shared, both platforms)

Where the version lives:
- **Flutter:** `version: x.y.z+N` in `pubspec.yaml`. The `+N` build number is used for both Android `versionCode` and iOS `CFBundleVersion`.
- **Native Android:** `versionName` and `versionCode` in the app's Gradle file.
- **Native iOS:** the marketing version and build number in the Xcode project (`CFBundleShortVersionString` and `CFBundleVersion`).
- **React Native:** the stores read the native Android and iOS values above, not `package.json`. Check how your project keeps them in sync.

| Check | Method | Pass criteria |
|---|---|---|
| Version bumped | Compare the current version with the last entry in `config.release_history_file` | Strictly higher (semver) |
| Build number bumped | Read the build number | Strictly higher than the last published build number |
| Package name unchanged | Read `applicationId` in the Android Gradle file | Equals `config.android.package_name` |
| Bundle id unchanged (iOS) | Read `PRODUCT_BUNDLE_IDENTIFIER` in the Xcode project | Equals `config.ios.bundle_id` |
| Version is new | Check `config.release_history_file` | This exact version and build were never published on the target platform |

> ### MANDATORY: always bump the build number before an Android build or upload
>
> Google Play **permanently rejects** any AAB whose `versionCode` was already uploaded, even to a closed or internal track, even if that upload was later discarded. Version codes are used up forever and can only go up. The error looks like "Version code N has already been used", and it happens in practice when the build number was not incremented.
>
> **Before building the Android artifact, this skill MUST:**
> 1. Read the current build number.
> 2. Find the highest version code already on Play. Check `config.release_history_file` first. If history is missing or may be stale (uploads made by hand elsewhere), ask the user: "What is the highest version code already uploaded to Play Console (Release > App bundle explorer, any track)?"
> 3. Set the build number to **(highest known version code) + 1**. Never reuse, only increase. Bump it even if the version name (`x.y.z`) stays the same: a re-upload of the "same" version still needs a fresh, higher version code.
> 4. Commit the bump (`release-prep: bump version code to N`) and record the new code so the next release starts from the right number.
>
> If an upload still fails with "version code already used", the real highest code on Play is higher than recorded. Increment again, and update `config.release_history_file` so it stops happening.

### 3.3 Android store compliance

Run when publishing to Android or Both.

| Check | Method | Pass criteria |
|---|---|---|
| Target SDK | Read `targetSdkVersion` (or `targetSdk`) | Meets Google's current minimum. It was API 34 as of 2025; verify the current requirement |
| Permissions audit | Read `android/app/src/main/AndroidManifest.xml` and list all permissions | Each permission is actually used. Flag any that look unnecessary |
| Privacy policy | `config.privacy_policy_url` | URL exists, loads, and is in the Play listing |
| Data safety form | Compare the Play Console data safety answers with what the app actually collects and shares | Declarations match app behavior |
| Account deletion | If `config.accounts.has_user_accounts` is true, check the in-app path and web URL in config | Users can delete their account, and the store listing points to it. Check Play Console's current wording on this |
| Signing key | Check `config.android.keystore_path` (or the configured signing setup) exists | Key file exists. Do NOT read or display key contents |

### 3.4 iOS store compliance

Run when publishing to iOS or Both. Paths are the default Flutter layout (`ios/Runner/...`). For native iOS or React Native, use the matching files in your Xcode project.

| Check | Method | Pass criteria |
|---|---|---|
| Minimum iOS version | Read `ios/Podfile` for `platform :ios` and the Xcode project for `IPHONEOS_DEPLOYMENT_TARGET` | iOS 13.0 or higher (the practical minimum for modern Flutter) |
| Xcode project builds | Flutter: `flutter build ios --release --no-codesign` (a dry run without signing). Native: an Xcode release build | Builds clean. Catches Swift and Objective-C compile issues |
| Distribution certificate | `security find-identity -v -p codesigning` | At least one valid "Apple Distribution" or "iPhone Distribution" certificate, not expired |
| Provisioning profile | Look for `.mobileprovision` files in `~/Library/MobileDevice/Provisioning Profiles/` matching the bundle id (or Xcode automatic signing) | A valid profile exists for `config.ios.bundle_id` |
| Info.plist permissions | Read every `NS*UsageDescription` key in `Info.plist` | Each has a clear, user-facing reason. Apple rejects vague text like "This app needs access"; it must explain WHY |
| Privacy manifest | Check for `PrivacyInfo.xcprivacy` in the app target | Present, and declares `NSPrivacyTracking`, `NSPrivacyCollectedDataTypes`, `NSPrivacyAccessedAPITypes` |
| App Transport Security | Read `NSAppTransportSecurity` in `Info.plist` | No blanket `NSAllowsArbitraryLoads = true`. Each exception is justified |
| App icons | Check `Assets.xcassets/AppIcon.appiconset/` | 1024x1024 icon present, no alpha channel, `Contents.json` references all required sizes |
| Launch screen | Check for `LaunchScreen.storyboard` | Present (Apple requires a storyboard, not a static image) |
| iPad support | Read `UIDeviceFamily` and compare with `config.ios.supports_ipad` | If iPad (2) is included, key screens render on iPad: Apple tests this. If not supporting iPad, `UIDeviceFamily` is iPhone only (1) |
| UIScene lifecycle | Flutter: `Info.plist` has `UIApplicationSceneManifest` with `FlutterSceneDelegate`; `AppDelegate` conforms to `FlutterImplicitEngineDelegate` and registers plugins in `didInitializeImplicitFlutterEngine`. Native and React Native: check your framework's docs for scene support | Present. Apps built with the iOS 27 SDK without a scene are stopped by UIKit at launch, and this caused a real App Store rejection. Also FAILS if the Xcode build prints "UIScene lifecycle support will soon be required" |
| Launch on newest iOS | Run the build on a simulator of the **newest** installed iOS runtime, iPhone **and** iPad (`xcrun simctl list devices`). Confirm it reaches the first screen and that no new crash report for the app appears in `~/Library/Logs/DiagnosticReports/` | Opens to the first screen on both. Apple reviews on an iPad running the newest iPadOS. Testing only on an older runtime is how a launch crash once slipped through |
| Push end to end after a lifecycle change | If `AppDelegate`, `Info.plist` scene keys or plugin registration changed since the last release: check every plugin that hooks app events supports the change. Then on the newest iOS simulator confirm a push token after allowing notifications, a push while the app is open (`xcrun simctl push`), and that a tap from the background opens the app and navigates | All three work. A scene lifecycle change once nearly shipped with push broken |

> **Build commands and one-time production auth.** If `config.build_guide` is set, it is the source of truth for exact release build commands. Key rule: build with `--dart-define-from-file={config.build_defines_file}` (or your framework's equivalent config file), never hand-typed flags, so no credential is left out. A missing iOS OAuth client id once broke iOS Google sign-in in production for exactly this reason.
>
> Before the **first** store release on each platform, finish any one-time production auth setup your sign-in providers need. In the setup this skill was proven on, that meant: registering the Play **App signing** and **Upload key** SHA-1 fingerprints in the Google Cloud project used for Google sign-in, publishing the Google OAuth consent screen, turning on "Skip nonce checks" for Google in Supabase Auth, and re-checking Apple sign-in. Your providers may differ; check their docs. Most of this is one-time and persists across releases.

### 3.5 Android build verification

Run when publishing to Android or Both.

> **If `config.code_push` is `shorebird`, build with `shorebird release android`, NOT `flutter build appbundle`,** so the release stays patchable later. It wraps `flutter build` and takes the same build defines. The AAB lands at the same path. Plain `flutter build` is only acceptable if Shorebird is unavailable, and then no live patches are possible for that version.
>
> If `code_push` is `none`: Flutter uses `flutter build appbundle --release` with your build defines. Native Android and React Native build the AAB with Gradle from the `android/` folder; check your framework's docs for the exact command.

| Check | Command | Pass criteria |
|---|---|---|
| Release build | As above | Builds with no errors |
| AAB size | Check the AAB file size | Report it. Warn if over 150MB (Play limit) or more than 50% larger than the last recorded size |
| AAB location | Report the path | Flutter: `build/app/outputs/bundle/release/app-release.aab` |

### 3.6 iOS build verification

Run when publishing to iOS or Both.

| Check | Command | Pass criteria |
|---|---|---|
| Release build | Flutter: `flutter build ipa --release` (or `shorebird release ios` if `code_push` is `shorebird`). Native and React Native: Xcode archive | Builds with no errors. Produces an `.xcarchive` and an `.ipa` |
| IPA size | Check the IPA size | Report it. Warn if over 200MB or more than 50% larger than the last recorded size. The App Store limit is 4GB, but users on cellular see a warning above 200MB |
| IPA location | Report the path | Flutter: `build/ios/ipa/*.ipa` |
| Export options | Check `config.ios.export_options_plist` exists | Uses the `app-store` method for App Store distribution |

### 3.7 Forced-update module: in-app update system

**Skip this section if `config.forced_update.backend` is `none`.** Show it as `[SKIP] No forced-update backend configured` in the report.

This check makes sure the update dialog users see after this release is correct. The skill owns the full update experience: not just the store upload, but what users see when they open the app after a new version is out.

| Check | Method | Pass criteria |
|---|---|---|
| Update service exists | Grep for `config.forced_update.update_service` (or a version check service) in the app code | Exists and is wired into app startup or your dependency setup |
| Update dialog exists | Grep for `config.forced_update.update_dialog` | Exists, with both forced and soft modes |
| Backend connection | Check the service reads from the configured backend | Fetches `min_version`, `latest_version`, `force_update`, `update_message` (see 6.4 for each backend) |
| Startup check | Check the update check runs on app launch | Runs at startup, with a timeout. Never blocks the app on a network failure |
| Dialog content | Check what the dialog shows | Version number, what's new text, action buttons |
| Forced mode | Check the forced dialog cannot be dismissed | No dismiss button, back button blocked (Flutter: `PopScope`), no tap outside to close |
| Soft mode | Check the soft dialog | Has "Update" and "Later". "Later" saves a timestamp so it does not nag |
| Store link | Check what "Update" opens | The right store URL per platform (`store_url_android` / `store_url_ios` from the backend) |
| Manual check | Check the version row in Settings | Tapping it shows loading, checks the backend, then shows the result (update available, or "up to date") |

**If the update system does not exist yet (first release):** not a blocking failure. Flag it as a required post-first-release task and add it to the version history notes. It must be built before the SECOND release, because that is when users on v1.0.0 need to hear about v1.1.0.

**If it exists:** verify the dialog matches the strategy chosen in Phase 5:
- **Forced update:** forced mode renders with the `update_message` text.
- **Soft nudge:** soft mode renders with "Update" and "Later".
- **Silent:** no dialog appears. Only the backend values change, and store auto-update handles the rest.

### Pre-flight report format

Present results in this exact format:

```
PRE-FLIGHT REPORT: {config.app_name} v{version} (build {buildNumber})
Platform: {Android / iOS / Both}
====================================================================

Past Lessons
  [PASS] {lesson}
  [FAIL] {lesson}: {why}

Code Quality
  [PASS] Static analysis: clean
  [PASS] Tests: 47/47 passed
  [FAIL] Debug code: print() at lib/features/home/widgets/chart.dart:42
  [PASS] Secrets scan: clean
  [PASS] Localization: generated

Version Integrity
  [PASS] Version 1.2.0 > 1.1.0 (previous)
  [PASS] Build number 13 > 12 (previous)
  [PASS] Package name unchanged: {config.android.package_name}
  {If iOS} [PASS] Bundle id unchanged: {config.ios.bundle_id}

{If Android or Both}
Android Store Compliance
  [PASS] Target SDK: API {n}
  [PASS] Permissions: INTERNET (used), POST_NOTIFICATIONS (used)
  [PASS] Privacy policy URL documented
  [PASS] Data safety form matches behavior
  [PASS] Account deletion: in app and web
  [PASS] Signing key exists

{If iOS or Both}
iOS Store Compliance
  [PASS] Minimum iOS: 13.0
  [PASS] Xcode build: clean
  [PASS] Distribution certificate: valid, expires {date}
  [PASS] Provisioning profile: matches {config.ios.bundle_id}
  [PASS] Info.plist permissions: all reasons clear
  [PASS] Privacy manifest: present and complete
  [PASS] App Transport Security: no blanket exceptions
  [PASS] App icons: 1024x1024 present, all sizes referenced
  [PASS] Launch screen storyboard: present
  [PASS] iPad support: {iPhone only / iPad supported and verified}
  [PASS] UIScene lifecycle: present, no warning
  [PASS] Launch on newest iOS: iPhone and iPad
  [PASS/SKIP] Push end to end: {result / no lifecycle change}

{If Android or Both}
Android Build
  [PASS] AAB built
  [INFO] AAB size: 24.3 MB (previous: 23.1 MB, +5.2%)
  [PASS] AAB at: {path}

{If iOS or Both}
iOS Build
  [PASS] IPA built
  [INFO] IPA size: 31.2 MB (previous: 29.8 MB, +4.7%)
  [PASS] IPA at: {path}

In-App Update System
  [PASS] Update service exists and runs at startup
  [PASS] Update dialog found
  [PASS] Forced mode: not dismissable, back button blocked
  [PASS] Soft mode: "Update" and "Later" present
  [PASS] Store link opens the right URL per platform
  [PASS] Settings version tap triggers a manual check
  {OR}
  [SKIP] Update system not built yet (first release, required before v2)
  {OR}
  [SKIP] No forced-update backend configured

Result: {N} FAILURE(S): fix the above before proceeding
```

If everything passes:
```
Result: ALL CHECKS PASSED: ready for Phase 4 (manual testing)
```

---

## Phase 4: Fix, re-verify and manual testing

Two entry points:

- **Issues found in Phase 2 or 3:** start at 4.1 (branch, fix, re-verify, then manual test).
- **Phases 2 and 3 passed clean:** go straight to 4.5 (manual testing gate).

Either way, **the user must run the app by hand and confirm it works** before Phase 5. No exceptions. Automated checks cannot catch everything: a screen that renders wrong, a flow that feels broken, a button that does nothing. Only human eyes catch these.

Think of it as a team workflow: one person finds the issue, another fixes it, a third verifies the fix.

### 4.1 Branch
When issues are found, create a dedicated fix branch:

```bash
git checkout -b release/v{version}-prep
```

All fixes happen here. Nothing is merged back until full re-verification passes.

### 4.2 Fix list

```
ISSUES TO FIX: {config.app_name} v{version}
===========================================

Branch: release/v{version}-prep

{N} blocking issues. Fix each one:

  1. [CODE QUALITY] {description}
     File: {path}:{line}
     Fix: {specific action}

  2. [SECURITY] {description}
     File: {path}:{line}
     Fix: {specific action}

  3. [VERSION] {description}
     Fix: {specific action}
```

The skill can fix some issues directly or hand them to a focused agent:

| Issue type | Who fixes | How |
|---|---|---|
| Debug code removal | This skill | Remove it, or guard it so it only runs in debug builds |
| Version bump | This skill | Update the version file |
| Test failures | A code-fixing agent | Reads the failing tests and fixes them |
| Security issues | A security-focused agent | Applies the secure fix |
| Signing key setup (Android) | Guide the user step by step | Cannot be automated, needs the user |
| Certificate or profile (iOS) | Guide the user step by step | Needs the Apple Developer portal, cannot be automated |
| Info.plist reasons (iOS) | This skill | Write clear permission reasons |
| Privacy manifest (iOS) | This skill | Generate `PrivacyInfo.xcprivacy` with the right declarations |
| Store compliance | Guide the user | Privacy policy, permission reasons, account deletion |

After each fix, commit to the prep branch:

```bash
git commit -m "release-prep: {what was fixed}"
```

### 4.3 Fresh re-verification
After all fixes, re-run the ENTIRE Phase 2 and Phase 3 pipeline with **fresh agents that have no memory of the previous run**.

Why fresh? An agent that found and fixed an issue may assume "that's fixed now" without checking. A fresh agent checks everything from scratch, with no bias.

1. **Run a fresh code review** on ALL code on the prep branch, not just the fixes: everything that will ship.
2. **Re-run every Phase 3 check** from scratch: analysis, tests, all scans, version, compliance, builds, for each target platform.
3. **Compare.** The result must be CLEAN: zero failures. If new issues appear, loop back to 4.2. There is no limit on loops. The code must be clean.

### 4.4 Re-verification report

```
RE-VERIFICATION REPORT: {config.app_name} v{version}
====================================================

Branch: release/v{version}-prep
Round: {N} (fresh agent, no prior context)

Previous issues: {N} blocking
Fixes applied: {N} commits on release/v{version}-prep

Fresh Code Review
  [PASS/FAIL] {result}

Fresh Pre-Flight
  Code Quality:                     [PASS/FAIL]
  Version Integrity:                [PASS/FAIL]
  {If Android} Android Compliance:  [PASS/FAIL]
  {If iOS} iOS Compliance:          [PASS/FAIL]
  {If Android} Android Build:       [PASS/FAIL]
  {If iOS} iOS Build:               [PASS/FAIL]

Result: {ALL CLEAN: ready for manual testing / STILL HAS ISSUES: loop back}
```

Only ALL CLEAN moves on to manual testing.

### 4.5 Manual testing gate

After all automated checks pass, the skill STOPS and hands control to the user. Build the checklist from `config.manual_test` plus the features changed in this release.

```
MANUAL TESTING REQUIRED: {config.app_name} v{version}
=====================================================

All automated checks passed. Before publishing,
run the app and confirm it works.

{If Android or Both}
Android: build and run a release build on a device
  Flutter: flutter run --release
  (or install the AAB on a test device)

{If iOS or Both}
iOS: build and run a release build on a device or simulator
  Flutter: flutter run --release -d {device}
  (or install via Xcode on a test device)

Checklist:
  [ ] App launches without a crash
  [ ] Main screens load: {config.manual_test.main_screens}
  [ ] Core flows work: {config.manual_test.core_flows}
  [ ] {each feature changed in this release, listed by name}
  [ ] No visual glitches, broken icons or misaligned layouts
  [ ] Navigation works (back button, tab switching)
  [ ] {each item in config.manual_test.extra_checks}
  {If iOS}
  [ ] Swipe-back gestures work
  [ ] Safe area and notch display correctly
  [ ] Dynamic Island and status bar do not cover content
  {If Both}
  [ ] Checked on BOTH Android and iOS

  {If forced-update module is on and the update system exists}
  Update dialog:
  {If forced}
  [ ] Forced dialog appears with the right version and message
  [ ] Cannot dismiss: back button and outside tap blocked
  [ ] "Update now" opens the right store page
  {If soft}
  [ ] Soft dialog appears with the right version and what's new
  [ ] "Update" opens the right store page
  [ ] "Later" dismisses cleanly, no crash
  [ ] Dialog does NOT come back right after dismiss
  {If silent}
  [ ] No dialog appears

  Settings version check:
  [ ] Tap version in Settings: shows loading, then a result
  [ ] If an update is available: shows the dialog with "Update"
  [ ] If up to date: says the app is up to date

When done, reply:
  "looks good" to continue to Phase 5
  "found issues" and describe them, to loop back and fix
```

The skill does NOT continue until the user explicitly confirms the app runs correctly. "I'm sure it's fine" is not acceptable. The user must actually run the app.

If the user reports issues:
1. Add them to the fix list.
2. Loop back to 4.2 and fix them.
3. Re-run the automated checks (4.3).
4. Come back to this gate.
5. Repeat until the user confirms everything works.

### 4.6 Merge
Once re-verification passes AND manual testing is confirmed:
1. Merge the prep branch back into the working branch.
2. Confirm the merge is clean (no conflicts).
3. The code is now verified clean, by machines and by human eyes.

---

## Phase 5: Version documentation

Only after Phase 3 passes completely (or Phase 4 re-verification plus manual testing, if fixes were needed).

### 5.1 What changed
1. Read the commits since the last version tag (or the last version in `config.release_history_file`).
2. Sort them into:
   - **Features:** new user-facing functionality
   - **Fixes:** bug fixes
   - **Improvements:** better versions of existing features
   - **Internal:** refactoring, dependency updates, tooling (users do not see these)

### 5.2 Version bump type

| Change type | Expected bump | Example |
|---|---|---|
| Breaking change or major redesign | Major (1.0.0 to 2.0.0) | Complete UI overhaul |
| New feature(s) | Minor (1.1.0 to 1.2.0) | A new screen or flow |
| Bug fix | Patch (1.1.0 to 1.1.1) | Fixed a broken icon |

If the bump does not match the change type, flag a warning, not a failure. The user may have a reason.

### 5.3 Update strategy (forced-update module only)

**Skip if `config.forced_update.backend` is `none`.** Record "Update strategy: none (no backend)" in the history entry.

Recommend one based on the changes:

| Scenario | Strategy | Backend values |
|---|---|---|
| Security fix or breaking API change | **Forced:** blocks old versions | `min_version` = this version, `force_update` = true |
| New feature | **Soft nudge:** dismissable dialog | `latest_version` = this version, `force_update` = false |
| Bug fix | **Silent:** store auto-update only, no dialog | `latest_version` = this version, no nudge |

Present the recommendation and ask the user to confirm or override.

### 5.4 Release track and rollout

**Android (Google Play):**

| Change type | Track | Staged rollout |
|---|---|---|
| Bug fix | Production | 100% right away |
| New feature | Internal testing first | 10%, then 50%, then 100% |
| Major version | Internal testing first | 10%, then 50%, then 100% |

**iOS (App Store):**

| Change type | Track | Phased release |
|---|---|---|
| Bug fix | App Store (direct) | No phased release, immediate |
| New feature | TestFlight internal, then TestFlight external, then App Store | 7-day phased release (1%, 2%, 5%, 10%, 20%, 50%, 100%) |
| Major version | TestFlight internal, then TestFlight external, then App Store | 7-day phased release |

Apple's phased release runs automatically over 7 days. You can pause it, or release to everyone, at any time from App Store Connect.

### 5.5 Store copy ("What's New")

**Google Play:**
- Max 500 characters.
- User-facing words, no jargon.
- Focus on what the user gets.

**App Store:**
- Max 4000 characters, but keep it short. About 500 is ideal.
- Apple review reads this. Do not mention other platforms, pricing, or terms that break the guidelines.
- Do NOT write only "bug fixes and improvements". Apple sometimes rejects that as not enough.

When publishing to Both, write separate copy for each store. The tone can differ slightly; the substance should match.

Show it to the user for approval before moving on.

### 5.6 Release history entry

Append to `config.release_history_file`:

```markdown
## v{version} (build {buildNumber}), {YYYY-MM-DD}, {status}

**Type**: {Feature Release | Patch | Hotfix | Major Release}
**Platform**: {Android | iOS | Both}
**Update strategy**: {Forced | Soft nudge | Silent | None}
**Toolchain**: {Xcode, iOS SDK, framework version, Android target SDK}

### Android
**Release track**: {Internal | Production | N/A}
**Rollout**: {10% | 50% | 100% | N/A}
**AAB size**: {size | N/A}

### iOS
**Release track**: {TestFlight Internal | TestFlight External | App Store | N/A}
**Phased release**: {Yes (7-day) | No (immediate) | N/A}
**IPA size**: {size | N/A}

### Changes
- {category}: {description}

### What's New (Google Play)
{copy}

### What's New (App Store)
{copy}

### Forced update config
- min_version: {value}
- latest_version: {value}
- force_update: {true|false}
- update_message: "{message}"

### Open follow-ups carried forward
- {any warning, deprecation or "will soon be required" note, or "none"}
```

Set status to `PENDING` first. Change it to `PUBLISHED` after a successful upload, or `FAILED` with the reason if rejected.

### Phase 5 report

```
VERSION DOCUMENTATION: {config.app_name} v{version}
Platform: {Android / iOS / Both}
===================================================

Changes: {N} commits since v{previous}
  Features: {list}
  Fixes: {list}

Version bump: {previous} to {new} ({type}, matches changes)
Update strategy: {FORCED / SOFT NUDGE / SILENT / NONE}

{If Android}
  Android track: {Internal / Production}
  Android rollout: {percentage}

{If iOS}
  iOS track: {TestFlight / App Store}
  iOS phased release: {Yes / No}

What's New (Google Play):
  "{copy}"

What's New (App Store):
  "{copy}"

Confirm to proceed to publish? [waiting for confirmation]
```

Do NOT go to Phase 6 until the user explicitly confirms.

---

## Phase 6: Publish

Only after the user confirms the Phase 5 output. For Both, do Android first, then iOS.

### 6.1 Final artifacts
The release builds were made in Phase 3. Confirm they still exist at the expected paths. If anything changed after Phase 3, re-run all of Phase 3 first.

### 6.2 Android upload (Google Play Console)

This skill guides the upload by hand. If you automate it later, keep the same steps and checks.

1. Open Google Play Console (account: `config.android.play_console_account`), select `config.app_name`, then Release, then the track chosen in 5.4.
2. Upload the AAB from the path reported in 3.5.
3. Paste the "What's New" text (give it to the user ready to copy).
4. Set the staged rollout percentage to `{percentage}`.
5. Submit for review.

Ask the user to confirm when the upload is done and whether it succeeded.

### 6.3 iOS upload (App Store Connect)

**Option A: Xcode (recommended for first-time setup)**
1. Open the iOS workspace in Xcode (Flutter: `ios/Runner.xcworkspace`).
2. Choose "Any iOS Device" as the destination.
3. Product, then Archive.
4. In the Organizer, click "Distribute App".
5. Choose "App Store Connect", then "Upload".
6. Follow the signing prompts.
7. Wait for processing in App Store Connect (about 15 to 30 minutes).

**Option B: command line (after first-time setup)**
1. Flutter: `flutter build ipa --release --export-options-plist={config.ios.export_options_plist}`
2. Upload with `xcrun altool --upload-app -f {path to .ipa} -t ios --apiKey {key_id} --apiIssuer {issuer_id}`, reading the key id and issuer id from the user's environment, never from config. Apple changes its upload tools from time to time; check Apple's current docs if this command fails.

**After upload succeeds:**

For TestFlight:
1. App Store Connect, then `config.app_name`, then TestFlight.
2. Wait for build processing to finish.
3. Add the build to the internal testing group.
4. If external: submit for TestFlight review (usually about 24 hours).
5. Distribute to testers.

For App Store submission:
1. App Store Connect, then `config.app_name`, then App Store, then the version.
2. Create version `{version}` if it does not exist.
3. Add the build to the version.
4. Paste the "What's New" text.
5. Set the phased release choice.
6. Fill in or verify:
   - App privacy (nutrition labels): must match `PrivacyInfo.xcprivacy` and what the app really does
   - Screenshots for every required device size (iPhone 6.7", 6.1", and iPad if supported)
   - Description, keywords, support URL, privacy policy URL
   - Account deletion path, if users can create accounts
   - Content rating questionnaire
7. Submit for review.

**Apple review expectations:**
- First submission: 1 to 3 days, sometimes longer.
- Updates: usually 24 to 48 hours.
- Expedited review: available for critical fixes (request it in App Store Connect).
- Common rejection reasons: incomplete metadata, placeholder content, crashes on launch, privacy violations.

Ask the user to confirm when the upload or submission is done.

### 6.4 Forced-update module: set the backend values

**Skip if `config.forced_update.backend` is `none`.**

After the user confirms a successful upload (on either or both platforms), set the values chosen in Phase 5, then confirm they were applied. Changing production values needs the user's go-ahead first.

The keys are the same for every backend:

| Key | Meaning |
|---|---|
| `min_version` | Oldest version allowed to run. Older versions see the forced dialog |
| `latest_version` | Newest version in the stores. Older versions may see the soft dialog |
| `force_update` | `true` or `false` |
| `update_message` | Text shown in the dialog |
| `store_url_android` | `config.android.store_url` |
| `store_url_ios` | `config.ios.store_url` |

**Supabase.** Update the rows in `config.forced_update.supabase_table`. If the table does not exist yet (first release), guide the user through creating it:

```sql
CREATE TABLE app_version (
  key TEXT PRIMARY KEY,
  value TEXT NOT NULL,
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

INSERT INTO app_version (key, value) VALUES
  ('min_version', '{version}'),
  ('latest_version', '{version}'),
  ('force_update', 'false'),
  ('update_message', ''),
  ('store_url_android', '{config.android.store_url}'),
  ('store_url_ios', '{config.ios.store_url}');
```

Use the table name from config if it is not `app_version`. Make sure the app can read this table but users cannot write to it (check your row level security setup).

**Firebase Remote Config.** Set the same keys as Remote Config parameters and publish the change. Check Firebase's docs for the current console steps.

**Custom backend.** Update wherever your app reads these keys from. Ask the user how if it is not documented in the repo.

The App Store URL needs the numeric App Store id, assigned when the app is first created in App Store Connect. On a first iOS release, leave `store_url_ios` as a placeholder, then fill it in (and `config.ios.app_store_id`) once the id is known.

### 6.5 Release history status
Update the entry in `config.release_history_file`:
- Change `PENDING` to `PUBLISHED`, or `FAILED` with the reason.
- Add the real publish date.
- For Both, track each platform on its own. `PUBLISHED (Android)` / `PENDING REVIEW (iOS)` is a valid state. Update iOS when Apple's review finishes.

### 6.6 Git tag

```bash
git tag -a v{version} -m "Release v{version}: {one-line summary}"
```

One tag for both platforms: the version is the same, only the store differs. Ask the user before pushing the tag to the remote.

### Final report

```
PUBLISH COMPLETE: {config.app_name} v{version}
==============================================

Version: {version} (build {buildNumber})
Update type: {Forced / Soft nudge / Silent / None}
Forced-update backend: {Updated / Skipped (none configured)}
Git tag: v{version} created
Release history: updated

{If Android}
Android:
  Track: {Internal / Production}
  Rollout: {percentage}%
  Status: {Submitted / Awaiting review}
  {If internal}: Next step: promote to Production after testing
  {If staged below 100%}: Next step: raise the rollout after monitoring

{If iOS}
iOS:
  Track: {TestFlight Internal / TestFlight External / App Store}
  Phased release: {Yes (7-day) / No (immediate)}
  Status: {Processing / Awaiting review / In review}
  {If TestFlight}: Next step: test, then submit to the App Store
  {If App Store}: Next step: watch review status in App Store Connect
  Expected review time: {24 to 48 hours for updates, 1 to 3 days for a first submission}
```

---

## Rules that never bend

These exist because consistency and safety matter more than speed.

1. **Never skip a check.** Every check runs every time. A "small fix" gets the same scrutiny as a major feature. The user cannot override this: if a check fails, it gets fixed. (Modules turned off in config are skipped by design, not skipped checks.)
2. **Never proceed without explicit confirmation.** Phase 5 to Phase 6 needs a clear "go ahead". Each upload needs the user to confirm it succeeded.
   - **2a. The user approves the route (patch or full release) every time.** Phase 1 only recommends. Stop and get an explicit `patch` or `release` before building, patching or uploading. Never infer it from the diff alone.
3. **Never touch production without asking.** Building is safe. Pushing tags, pushing code, changing forced-update values, or anything else that affects production needs confirmation.
4. **Fail loudly, fail completely.** If something goes wrong mid-process, stop and report. Do not recover silently. Do not continue with partial results.
5. **Document everything.** Every publish attempt, successful or failed, goes in the release history. Six months from now, someone should be able to read it and know exactly what happened with every release.
6. **Be the same every time.** Release #50 follows the exact same process as release #1. No drift. No "we've done this before, let's skip the easy parts."
7. **Orchestrate, do not replace.** This skill is the conductor. It makes sure code review and security checks run. The order is always: review, then checks, then documentation, then publish.
8. **Platform parity.** When publishing to Both, neither platform gets special treatment. An Android-only issue still blocks a Both release, because the codebase is shared.
9. **Learn from every release.** Phase 0 always runs. The Release lessons are permanent checks, and a carried-forward follow-up is re-judged every release, never copied forward unread.

---

## Dry run mode

If the user asks "is my app ready to publish?", "check if we can publish" or "run pre-flight" without asking to publish, run Phase 0, Phase 2 and Phase 3 only (and the first-run setup if there is no config yet). Show the full report. Do NOT enter Phase 4, 5 or 6.

End with:
```
DRY RUN COMPLETE: not publishing, just reporting status

{If all passed}: Ready to publish. Say "publish" when you want to go live.
{If failures}: {N} issues to fix before publishing. See the report above.
```

---

## Files this skill reads and writes

Paths are relative to `config.app_dir` and show the default Flutter layout. Native and React Native projects use the same kinds of files in their own locations.

| File | Read / write | Purpose |
|---|---|---|
| `.app-publish.json` (repo root) | Read + write (first run) | All project settings |
| `config.release_history_file` | Read + write | Release history, lessons and follow-ups |
| `config.build_guide` | Read | Exact build commands and one-time production auth setup |
| `pubspec.yaml` | Read + write (version bump) | Version and build number (Flutter) |
| `android/app/build.gradle(.kts)` | Read | Package name, SDK versions (and version, for native Android) |
| `android/app/src/main/AndroidManifest.xml` | Read | Android permissions audit |
| `ios/Runner.xcodeproj/project.pbxproj` | Read | Bundle id, iOS deployment target, device family |
| `ios/Runner/Info.plist` | Read | Permission reasons, ATS, scene manifest |
| `ios/Runner/PrivacyInfo.xcprivacy` | Read | iOS privacy manifest |
| `ios/Runner/Assets.xcassets/AppIcon.appiconset/` | Read | App icon check |
| `ios/Runner/Base.lproj/LaunchScreen.storyboard` | Read | Launch screen check |
| `ios/Podfile` | Read | Minimum iOS version |
| `config.ios.export_options_plist` | Read | Export and signing setup |
| `lib/**` (or your source folder) | Read | Code quality and security scans |
| `build/app/outputs/bundle/release/` | Read | Built AAB |
| `build/ios/ipa/` | Read | Built IPA |
