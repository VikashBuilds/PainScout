# 🚀 ChromaClear

*Eliminate color fringing on OLED monitors with subpixel-aware text rendering*

## The problem
Windows ClearType assumes RGB stripe subpixels, causing visible color fringing on WOLED (WRGB) and QD-OLED (triangular) displays. No built-in OS option exists to match rendering to actual subpixel layouts.

## The solution
A system-level utility that detects monitor subpixel geometry and applies custom ClearType-compatible rendering profiles. Users select their panel type (WOLED WRGB, QD-OLED triangular, RGB stripe) and the tool injects corrected gamma, contrast, and subpixel weights via DirectWrite overrides. Works globally across all apps without per-app config.

## Features (v1)
- Auto-detect monitor subpixel layout via EDID/panel database
- Preset profiles: WOLED WRGB, QD-OLED triangular, RGB stripe, BGR stripe
- Custom subpixel weight sliders (R/G/B/W intensity per subpixel)
- Real-time preview pane with test strings at multiple sizes
- Per-monitor profiles for multi-monitor mixed setups
- DirectWrite hook for system-wide application (no app restart)
- Gamma/contrast compensation tuned per panel type
- Export/import profile JSON for community sharing
- CLI for automation and CI integration
- Tray app with hotkey toggle for quick A/B comparison

## MVP scope
Build a Windows tray utility that lets users pick from 4 preset subpixel profiles (WOLED WRGB, QD-OLED triangular, RGB stripe, BGR stripe) and applies a DirectWrite rendering override globally. Include a live preview window with standard test strings. Ship as a single signed EXE with no installer.

## Tech stack
C# .NET 8, WPF (WinUI 3 optional), DirectWrite via Vortice.Windows, WMI/SetupAPI for EDID parsing, GitHub Actions CI/CD, Winget/Chocolatey distribution, DigiCert code signing certificate, NSIS installer (optional)

## Build estimate: 18 days

## Competitors & gaps
- **ClearType Tuner (built-in)** — gap: Only offers RGB/BGR stripe tuning; no WRGB or triangular presets
- **BetterClearType (GitHub)** — gap: Open-source but unmaintained; no auto-detect, no per-monitor profiles
- **MacType** — gap: Replaces font rasterizer entirely; heavy, breaks some apps, no OLED-specific profiles
- **DisplayCAL** — gap: Focuses on color calibration, not subpixel text rendering
- **MonitorControl** — gap: Controls brightness/volume, no text rendering hooks

## Landing page copy
- **Headline:** Sharp Text on Any OLED. Finally.
- **Subheadline:** Stop color fringing on WOLED and QD-OLED monitors with the only tool that matches Windows ClearType to your actual subpixel layout.
- Bullet: Auto-detects your panel type via EDID
- Bullet: Presets for WOLED WRGB, QD-OLED triangular, RGB/BGR stripe
- Bullet: System-wide — works in every app, no restarts
- Bullet: Per-monitor profiles for mixed setups
- Bullet: Open-source core, free forever for personal use
- **CTA:** Download for Windows (Free)

## WhatsApp-first bot
- **Flow:** User messages bot with monitor model → bot replies with recommended profile + download link → user installs → bot sends setup verification checklist → optional: submit anonymous fringing screenshot for community database
- **Commands:** /detect <model>, /profiles, /download, /verify, /submit, /help
- **Pricing:** Free bot; core app free for personal use; $19 one-time for commercial license + priority support

## Pricing model: Free for personal use; $19 one-time commercial license (per seat); optional $5/yr for auto-updates & profile cloud sync
