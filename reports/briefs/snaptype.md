# 🚀 SnapType

*Instant text expansion & crisp OLED rendering for Windows*

## The problem
Windows lacks built-in text replacement and proper subpixel rendering for modern OLED monitors, forcing power users to juggle multiple tools or tolerate blurry text.

## The solution
SnapType combines a lightweight text expander with an OLED-aware font renderer, letting you insert snippets instantly and enjoy sharp, color-fringe-free text on any display.

## Features (v1)
- Global text expansion with custom triggers
- Per-monitor OLED subpixel rendering profiles (WRGB, RGB triangular)
- Cloud sync of snippets across devices
- Rich snippet support (formatted text, images, dynamic fields)
- Auto-detect monitor subpixel layout via EDID
- System-wide hotkey for snippet search
- Import/export from PowerToys, Espanso, AutoHotkey
- Low-resource background service (<10MB RAM)
- Per-app exclusion list
- Dark/light theme aware UI

## MVP scope
Build a system tray app with global text expansion using Windows hooks, and a DirectWrite-based font renderer that applies custom subpixel geometry per monitor. Ship with 3 preset OLED profiles and manual calibration.

## Tech stack
C# .NET 8, WinUI 3, Windows App SDK, DirectWrite/Direct2D, SQLite for local snippet DB, Microsoft Graph API for cloud sync, GitHub Actions for CI/CD, MSIX packaging for Store distribution

## Build estimate: 45 days

## Competitors & gaps
- **PowerToys** — gap: Text expansion exists but no OLED subpixel rendering; UI clunky for snippet management.
- **Espanso** — gap: Cross-platform but no Windows-specific font rendering; config file only, no GUI.
- **PhraseExpress** — gap: Expensive subscription; no OLED rendering; Windows-only but heavy.
- **MacType** — gap: Improves font rendering but no text expansion; complex setup, no per-monitor profiles.
- **BetterClearType** — gap: Only ClearType tuning; no text expansion; limited to RGB stripe.

## Landing page copy
- **Headline:** Stop typing the same things. See text clearly on OLED.
- **Subheadline:** SnapType gives you instant text expansion and monitor-perfect font rendering in one lightweight Windows app.
- Bullet: Insert emails, addresses, code blocks with a few keystrokes
- Bullet: Eliminate color fringing on WOLED & QD-OLED monitors
- Bullet: Sync snippets securely across all your PCs
- Bullet: Zero latency, runs in the background at <10MB RAM
- **CTA:** Download Free Beta

## WhatsApp-first bot
- **Flow:** User messages 'snip <trigger> <text>' to save a snippet; 'list' shows all; 'sync' pushes to Windows app via cloud. Bot also sends daily tip for OLED calibration.
- **Commands:** /new, /list, /delete, /sync, /help
- **Pricing:** Free for 50 snippets; $19/year for unlimited + cloud sync + OLED profiles

## Pricing model: Freemium: free tier (50 snippets, basic rendering), Pro $19/year (unlimited snippets, cloud sync, advanced OLED profiles, priority support)
