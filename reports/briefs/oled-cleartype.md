# 🚀 OLED ClearType

*Eliminate color fringing on WRGB and QD-OLED monitors with custom subpixel rendering.*

## The problem
Windows ClearType assumes RGB stripe subpixels, causing severe color fringing on WRGB WOLED and RGB-triangular QD-OLED monitors. No OS-level fix exists despite years of community requests.

## The solution
A Windows utility that replaces ClearType's subpixel anti-aliasing with monitor-specific algorithms for WRGB stripe and RGB triangular layouts, delivering crisp, fringing-free text system-wide via a user-mode DirectWrite hook.

## Features (v1)
- Automatic monitor subpixel layout detection via EDID parsing
- Custom HLSL shader rendering engine for WRGB stripe (WOLED)
- Custom HLSL shader rendering engine for RGB triangular (QD-OLED)
- Per-monitor profiles with hot-swap on display connection change
- System-wide injection via DirectWrite custom text renderer hook
- ClearType-style tuner UI for contrast, gamma, and geometry per layout
- Per-application exclude list (games, Electron apps, etc.)
- Portable mode: no admin rights required for current-user session
- Open-core shaders for community tuning and validation
- Zero telemetry, fully local operation

## MVP scope
Build a user-mode DirectWrite hook that intercepts text rendering calls, detects connected OLED monitor subpixel layout via EDID, and applies a WRGB-stripe shader. Ship as a portable EXE with a system tray toggle and basic per-monitor on/off.

## Tech stack
Rust (2021 edition), windows-rs crate for Win32/DirectWrite/Direct2D interop, MinHook for API detouring, HLSL shaders compiled to DXBC via dxc, egui for native system tray and settings window, cargo-wix for MSI installer and portable zip packaging, GitHub Actions for CI/CD (Windows runners), EDID parsing via windows-rs DisplayConfig APIs

## Build estimate: 35 days

## Competitors & gaps
- **Windows ClearType** — gap: Only supports RGB stripe geometry; no WRGB or triangular profiles
- **MacType** — gap: GDIPP-based, unstable on Windows 11, no OLED-specific shaders
- **Better ClearType Tuner** — gap: Only tweaks existing ClearType parameters; cannot change subpixel geometry
- **DisplayCAL** — gap: Color calibration only; does not modify text rendering pipeline
- **NVIDIA/AMD Control Panels** — gap: GPU-level scaling/sharpening; not subpixel-aware for text

## Landing page copy
- **Headline:** Crisp Text on Every OLED
- **Subheadline:** Finally, subpixel rendering that matches your monitor's actual layout — WRGB WOLED and RGB-triangular QD-OLED.
- Bullet: Auto-detects your panel's subpixel geometry via EDID
- Bullet: Custom shaders for WRGB stripe and RGB triangular layouts
- Bullet: System-wide, per-monitor, per-app control
- Bullet: Zero telemetry, portable, open-core
- **CTA:** Download Free Beta

## WhatsApp-first bot
- **Flow:** User sends monitor model or EDID blob → bot replies with detected subpixel layout and direct download link for matching build → user runs portable EXE → bot follows up with license key after purchase.
- **Commands:** /detect <monitor_model>, /download, /license <email>, /help, /changelog
- **Pricing:** Free beta; $19 one-time license per major version (v1.x, v2.x). Free for personal use on single monitor.

## Pricing model: $19 one-time license per major version, free beta, free for personal use on single monitor
