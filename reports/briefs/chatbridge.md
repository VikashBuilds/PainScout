# 🚀 ChatBridge

*Seamlessly migrate WhatsApp chats between Android and iPhone without data loss*

## The problem
WhatsApp backups are locked to Google Drive (Android) and iCloud (iPhone) with no official cross-platform migration path. Switching operating systems results in permanent chat history loss.

## The solution
A desktop app that extracts encrypted WhatsApp backups from both Google Drive and iCloud, decrypts them locally using the user's encryption key, and converts them into a universal format for restoration on the target device via WhatsApp's official 'Move Chats' feature. All processing happens offline — chat data never leaves the user's machine.

## Features (v1)
- OAuth authentication with Google Drive to locate and download encrypted WhatsApp backup (crypt12/crypt14)
- Apple ID authentication via app-specific password to access iCloud WhatsApp backup
- Local decryption using user's 64-digit encryption key (derived from phone number + user passphrase)
- Parse decrypted SQLite database into structured JSON with messages, media references, contacts, groups
- Selective migration UI: filter by contact, group, date range, media type; preview before export
- Generate WhatsApp-compatible backup bundle for target OS (Android .crypt14 or iOS .sqlite)
- Media handling: download thumbnails, re-encrypt media keys, preserve voice notes/documents
- Progress tracking with pause/resume, checksum verification, detailed logs
- Offline-first: zero cloud upload of chat content; only backup metadata touches APIs
- License key validation via local signed JWT (no phone-home required after activation)

## MVP scope
Build a Tauri (Rust + React) desktop app for macOS/Windows that authenticates with Google Drive and iCloud, downloads encrypted backup files, decrypts locally using user-provided 64-digit key, parses SQLite to JSON, and outputs a standardized backup bundle compatible with WhatsApp's official 'Move Chats to Android/iOS' flow. Text messages and media references only in v1; full media migration in v1.1.

## Tech stack
Tauri 2.0 (Rust backend, React/TypeScript frontend, WebView2/WebKit), Google Drive API v3 (googledrive Rust crate or Node via sidecar), iCloud access via pyicloud-rs (Rust port) or CloudKit JS via embedded WebView, Custom crypt12/crypt14 decryption implementation (AES-256-GCM, PBKDF2-HMAC-SHA512), SQLite (rusqlite) for backup parsing and universal format generation, Serde JSON for universal backup schema, Vercel for landing page + license API (Edge Functions), LemonSqueezy for licensing, payments, affiliate management

## Build estimate: 45 days

## Competitors & gaps
- **MobileTrans (Wondershare)** — gap: $39.95/year subscription, closed source, uploads data to their servers, bloated with unnecessary features
- **Dr.Fone (Wondershare)** — gap: Similar subscription model, privacy concerns, forces full toolkit install, no selective migration
- **WhatsApp Official 'Move to iOS/Android'** — gap: Only works during initial device setup, requires factory reset, one-directional, no selective chat choice
- **iCareFone Transfer (Tenorshare)** — gap: Freemium with 20-message limit, requires USB debugging/lightning cable, Windows-only for Android->iOS
- **Backuptrans** — gap: Ancient UI, Windows only, no media support, $29.95 one-time but abandoned updates

## Landing page copy
- **Headline:** Switch Phones. Keep Every Chat.
- **Subheadline:** The only tool that moves your full WhatsApp history — texts, media, voice notes — between Android and iPhone without data loss or cloud exposure.
- Bullet: Extract from Google Drive & iCloud — no factory reset needed
- Bullet: Local-only decryption — your chats never touch our servers
- Bullet: Selective migration — move only the chats that matter
- Bullet: Preserves media, timestamps, sender info, and formatting
- Bullet: Works with WhatsApp's official restore flow — no hacks
- Bullet: One-time purchase, no subscription
- **CTA:** Download Free Trial (Moves 50 Messages)

## WhatsApp-first bot
- **Flow:** User purchases license → receives key via email → downloads desktop app → authenticates Google Drive/iCloud in app → bot sends real-time progress notifications (download %, decryption status, export complete) and final success/failure alert with log link
- **Commands:** STATUS - current migration progress percentage, LOGS - last 50 lines of operation log, RETRY - resume failed migration from checkpoint, HELP - setup guide link + video tutorial, LICENSE - resend license key to this chat
- **Pricing:** Free bot notifications included with $49 one-time license

## Pricing model: $49 one-time license (lifetime updates, 3 devices), free trial migrates 50 messages per chat. No subscription.
