# 🚀 SubpixelSync

*Eliminate OLED text fringing with per-monitor subpixel rendering profiles*

## The problem
Windows ClearType assumes RGB stripe subpixels, but WOLED (WRGB) and QD-OLED (triangular) monitors produce visible chromatic aberration on text edges. No OS-level fix exists for per-display subpixel configuration.

## The solution
A lightweight Windows tray utility that detects each monitor's subpixel layout, applies custom gamma/sharpening per RGBW channel via DirectWrite interception, and persists per-display profiles. Works without admin rights, survives reboots, and includes test patterns for visual calibration.

## Features (v1)
- Auto-detect monitor subpixel layout via EDID + community database
- Per-monitor rendering profiles (WOLED WRGB, QD-OLED triangular, RGB stripe, BGR)
- Real-time test pattern overlay (color fringes, line pairs, text samples)
- Independent gamma/contrast per subpixel channel (R/G/B/W)
- System tray control with global hotkeys (Win+Alt+S to toggle)
- CLI for CI/CD and multi-machine deployment (subpixelsync apply --profile coding)
- Export/import JSON profiles for team sharing
- Low-overhead DirectWrite hook (~15MB RAM, <1% CPU)
- Startup persistence via Task Scheduler (no UAC prompt)
- Open-source core with paid pro features (multi-monitor, CLI, auto-update)

## MVP scope
Build a C# .NET 8 WinUI 3 tray app that enumerates displays, reads EDID for panel type, lets user pick from 4 presets (WOLED, QD-OLED, RGB, BGR), applies a per-monitor ICC-style gamma LUT via SetDeviceGammaRamp, and persists settings. Ship with a built-in test pattern window. Target 30-day build.

## Tech stack
C# .NET 8, WinUI 3 (Windows App SDK), DirectWrite / Direct2D via SharpDX or Silk.NET, Windows.Devices.Display.Core API for EDID parsing, Microsoft.Win32.TaskScheduler for startup, System.CommandLine for CLI, GitHub Actions + msix packaging, Winget/Chocolatey + GitHub Releases for distribution

## Build estimate: 35 days

## Competitors & gaps
- **Windows ClearType Tuner** — gap: Assumes RGB stripe only; no per-monitor control; no WRGB/triangular support
- **BetterClearType (GitHub)** — gap: Unmaintained since 2018; no OLED presets; requires manual registry edits
- **DisplayCAL / ArgyllCMS** — gap: Full color calibration suite; overkill for subpixel fringing; no per-subpixel gamma
- **macOS Font Smoothing** — gap: Global only; no subpixel layout awareness; not on Windows
- **PowerToys (requested)** — gap: Issue open since 2023; no implementation; would still need per-monitor EDID detection

## Landing page copy
- **Headline:** Sharp text on every OLED. No registry hacks.
- **Subheadline:** SubpixelSync detects your monitor's true subpixel layout and applies per-display rendering correction — so code, docs, and UI stay crisp on WOLED and QD-OLED.
- Bullet: Auto-detects WRGB, triangular, RGB, BGR layouts via EDID
- Bullet: Per-monitor gamma per subpixel channel (R/G/B/W)
- Bullet: Test patterns for visual calibration in seconds
- Bullet: Tray app + CLI + portable — no admin, no install
- Bullet: Open-source core, free for single monitor
- **CTA:** Download for Windows (free)

## WhatsApp-first bot
- **Flow:** User messages bot with monitor model (e.g., 'AW3423DWF'). Bot replies with preset name + one-click .reg file or winget install link. User runs file, restarts app, fringing gone.
- **Commands:** /detect — reply with EDID parse guide, /preset <model> — returns JSON profile + install command, /test — sends test pattern image for phone review, /help — lists supported panels
- **Pricing:** Free bot. Pro features (multi-monitor sync, team profile sharing) $5/mo via Stripe link in bot.

## Pricing model: Freemium: Free forever for 1 monitor. Pro $19 one-time (unlimited monitors, CLI, auto-update, profile export). Team $49/yr (shared profile repo, SSO).
