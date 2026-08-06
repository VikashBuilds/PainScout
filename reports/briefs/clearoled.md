# 🚀 ClearOLED

*Eliminate color fringing on WOLED and QD-OLED monitors*

## The problem
Windows ClearType assumes RGB stripe subpixels, causing severe color fringing on WOLED (WRGB) and QD-OLED (triangular) displays with no native fix.

## The solution
A lightweight Windows utility that applies custom pixel shaders to correct subpixel rendering per panel type, replacing ClearType's faulty assumptions with display-aware anti-aliasing.

## Features (v1)
- Auto-detect monitor panel type (WOLED/QD-OLED/standard) via EDID and display enumeration
- Per-monitor HLSL shader profiles for WRGB stripe, RGB triangular, and RGB stripe layouts
- Real-time preview with configurable test patterns (text, lines, color edges)
- System-wide toggle with per-application exclusion list (e.g., disable for games)
- ClearType replacement: disables ClearType, injects shader via Desktop Window Manager hook
- Calibration wizard with visual fringe measurement and automatic profile selection
- Low-resource background service (<1% GPU, ~15MB RAM) with startup persistence
- Open-source shader library (GitHub) for community-contributed panel profiles
- Hotkey (Win+Alt+C) for instant A/B comparison between corrected and raw output
- Export/import JSON profiles for sharing across machines or monitor upgrades

## MVP scope
Build a WinUI 3 desktop app with Direct3D 11/HLSL shader pipeline that hooks DWM via Windows Magnification API, applies per-monitor pixel shaders, and persists three built-in profiles (WOLED, QD-OLED, Standard). Include calibration wizard with fringe test patterns and system-wide enable/disable. Ship as MSIX via GitHub Releases and Winget.

## Tech stack
.NET 8 / C#, WinUI 3 (Windows App SDK 1.5+), Direct3D 11 / HLSL (Shader Model 5.0), Windows Magnification API (MagSetWindowTransform), SQLite (local profile storage), GitHub Actions (CI/CD, MSIX packaging), Winget / Chocolatey (distribution), EDID parsing via Windows.Devices.Display.Core

## Build estimate: 35 days

## Competitors & gaps
- **BetterClearTypeTuner** — gap: Only tweaks ClearType registry values; cannot change subpixel geometry assumption
- **MacType** — gap: Replaces font rasterizer globally; doesn't address panel subpixel layout mismatch
- **Windows ClearType Tuner (built-in)** — gap: Assumes RGB stripe only; no WOLED/QD-OLED awareness
- **DisplayCAL** — gap: ICC color calibration only; no runtime subpixel rendering correction
- **Custom ICC profiles** — gap: Fixes color accuracy, not subpixel geometry or text fringing

## Landing page copy
- **Headline:** Sharp Text on Any OLED. Finally.
- **Subheadline:** Stop color fringing on WOLED and QD-OLED monitors with display-aware pixel shaders — no ClearType hacks.
- Bullet: Auto-detects your panel type and applies the correct subpixel shader
- Bullet: Works system-wide or per-app; zero latency, <1% GPU
- Bullet: Calibrate in 60 seconds with visual fringe test patterns
- Bullet: Open-source shaders — community profiles for new panels
- **CTA:** Download Free for Windows 10/11

## WhatsApp-first bot
- **Flow:** User messages bot with monitor model → bot replies with EDID lookup guide → sends test pattern image → user replies with photo of screen → bot analyzes fringe via CV → sends optimal shader profile file → user imports in app
- **Commands:** /detect <model>, /testpattern, /profile <panel_type>, /calibrate, /help
- **Pricing:** Free companion bot; Pro users get priority analysis and auto-profile updates

## Pricing model: Free personal use / $19 one-time Pro license (per-app exclusions, auto-profile updates, priority support)
