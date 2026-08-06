# 🚀 MonitorSpaces

*Independent virtual desktops per monitor, keep reference apps static while cycling workspaces.*

## The problem
Windows switches virtual desktops globally across all monitors, forcing power users to lose reference apps (e.g., Outlook) when cycling workspaces on other screens. Users need per-monitor desktop switching with shared desktop pools.

## The solution
MonitorSpaces creates independent virtual desktop controllers for each monitor, allowing users to pin reference apps to a static desktop while cycling through shared workspace sets on other screens. It integrates with Windows' native virtual desktop API, providing per-monitor hotkeys, taskbar previews, and a unified desktop pool accessible from any monitor.

## Features (v1)
- Per-monitor virtual desktop switching via customizable hotkeys
- Pin/reference mode: lock a monitor to a specific desktop
- Shared desktop pool: same set of desktops accessible across all monitors
- Taskbar integration showing per-monitor desktop thumbnails
- Multi-monitor layout profiles (save/restore monitor-desktop assignments)
- Automatic desktop assignment on monitor connect/disconnect
- Lightweight system tray controller with keyboard shortcuts
- Compatibility with Windows 10/11 native virtual desktops

## MVP scope
MVP delivers per-monitor desktop switching with shared pool: a system tray app that hooks Windows Virtual Desktop API, exposes per-monitor hotkeys (Win+Ctrl+Left/Right per monitor), and lets users pin one monitor to a fixed desktop. No taskbar integration or profiles in v1.

## Tech stack
.NET 8 (C#), Windows App SDK / WinUI 3, Windows Virtual Desktop COM Interop (IVirtualDesktopManager), NHotkey for global hotkeys, Hardcodet.Wpf.TaskbarNotification for system tray, MSIX packaging & GitHub Actions CI/CD

## Build estimate: 35 days

## Competitors & gaps
- **Windows Native Virtual Desktops** — gap: Switches all monitors globally, no per-monitor control.
- **DisplayFusion** — gap: Focuses on monitor profiles/window management, lacks independent virtual desktop cycling per monitor.
- **Dexpot (discontinued)** — gap: Offered per-monitor desktops but no longer maintained, no Windows 11 support.
- **VirtuaWin** — gap: Legacy virtual desktop manager, no multi-monitor independence, outdated UI.

## Landing page copy
- **Headline:** Per-Monitor Virtual Desktops for Windows Power Users
- **Subheadline:** Keep Outlook on screen 1 while cycling project workspaces on screens 2 & 3 — all from a shared desktop pool.
- Bullet: Independent desktop switching per monitor via custom hotkeys
- Bullet: Pin reference apps to a static desktop on any monitor
- Bullet: Shared desktop pool accessible across all screens
- Bullet: Lightweight, native Windows integration — no electron bloat
- Bullet: Free open-source core, pro features $19 one-time
- **CTA:** Download for Windows 10/11

## WhatsApp-first bot
- **Flow:** User messages bot with 'start' → receives download link and license key (if purchased). Commands: 'switch <monitor> <desktop>' triggers desktop switch via local agent (requires companion app). 'status' shows current desktop per monitor. 'help' lists commands.
- **Commands:** start, switch <monitor> <desktop>, status, help, license
- **Pricing:** Free tier: bot access + core app. Pro: $19 one-time for advanced hotkeys, profiles, and bot remote control.

## Pricing model: Freemium: core per-monitor switching free; Pro $19 one-time unlocks profiles, auto-assign, and WhatsApp remote control.
