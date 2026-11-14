# app-publish

A strict release gate for mobile apps. Your agent runs the same checks, in the same order, for every release, then walks you through the Play Store and App Store upload.

## What it does

- Reads your release history first, so a past rejection or warning never slips through twice.
- Decides whether a change can ship as a live code-push patch (Shorebird) or needs a full store release. You approve the route every time.
- Reviews the code that is shipping and runs a security audit.
- Runs pre-flight checks: analysis, tests, debug code, secrets, version and build number, Android and iOS store compliance, release builds.
- Makes you test the app by hand before anything is published.
- Writes the version notes, picks the rollout plan and drafts the "What's New" text for each store.
- Guides the upload: Play Console tracks and staged rollout, TestFlight, App Store review and phased release.
- Optionally sets your forced-update switch (Supabase, Firebase Remote Config or your own backend).

Nothing is skippable. A one-line fix gets the same checks as a major release.

## Who it is for

Solo builders and small teams shipping a mobile app to Google Play, the App Store, or both. It was proven on Flutter. Native iOS, native Android and React Native work too; the skill says where the steps differ and points you to your framework's docs where it does not know the exact steps.

## Install

Clone the repo and copy the skill folder into your agent's skills folder:

```bash
git clone https://github.com/FRodman19/curious-builder.git
cp -R curious-builder/skills/app-publish ~/.claude/skills/
```

For Codex, copy it into `~/.codex/skills/` instead.

## First run

Open your app's repo and ask your agent "is my app ready to ship?" or "let's publish".

On the first run the skill creates `.app-publish.json` in your repo root. It detects what it can (package name, bundle id, version, Shorebird) and asks you for the rest:

- app name, framework and platforms
- Play Console and App Store Connect account names
- privacy policy URL and where users delete their account
- the screens and flows you want to test by hand each release
- forced-update backend: `supabase`, `firebase-remote-config`, `custom` or `none`
- code-push tool: `shorebird` or `none`

The file holds no secrets and is safe to commit. Signing keys, passwords and API keys stay in your keychain or environment.

Say "run pre-flight" any time for a dry run that reports without publishing.

---

Made by Frank (Curious Builder), used to ship Rhydle to the App Store and Google Play.
