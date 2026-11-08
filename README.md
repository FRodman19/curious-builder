# Curious Builder

The tools I build and use, shared in the open. I'm Frank, a solo builder shipping real software with AI: [Rhydle](https://apps.apple.com/us/app/rhydle-simple-profit-tracker/id6788178858) on the App Store and Google Play, and [Simplify Edits](https://simplifyedits.com), a Mac video editor. When something I made could help you, it ends up here.

Every step is on YouTube: [@frank-builds](https://www.youtube.com/@frank-builds)

## What's here

| Skill | What it does |
|---|---|
| [ai-video-editor](skills/ai-video-editor) | Takes a raw recording to a finished edit with AI: transcript, paper edit, cuts, motion graphics, render. Bring your own brand colours and fonts. |
| [app-workflow-demo](skills/app-workflow-demo) | Turns your app's real code and UI into faithful product demos and before and after release showcases. Includes 21 synthesized UI sounds and two ambient beds. |

These are agent skills: folders with a `SKILL.md` that Claude Code, Codex and other agents read.

## Install a skill

Clone the repo and copy the skill folder into your agent's skills folder:

```bash
git clone https://github.com/FRodman19/curious-builder.git
cp -R curious-builder/skills/app-workflow-demo ~/.claude/skills/
```

For Codex, copy it into `~/.codex/skills/` instead. Then ask your agent for the task in plain words, for example "make a demo of my app's onboarding".

## Questions

Open an issue, or ask under any of my videos.
