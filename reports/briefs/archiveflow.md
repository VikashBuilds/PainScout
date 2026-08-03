# 🚀 ArchiveFlow

*Automate every backup, share anywhere, never lose a memory*

## The problem
Parents and creators manually manage 3-5 disconnected backup silos (local drives, USB, cloud, Flickr, YouTube) with no unified pipeline for offline/tape archival, cross-device viewing, or effortless sharing.

## The solution
ArchiveFlow connects all your media sources and backup targets into a single automated pipeline. Set rules once — it continuously syncs new photos/videos to cloud, local NAS, USB, and cold storage (tape/LTO), generates shareable albums, and serves a unified library view on every device. Zero ongoing effort after initial setup.

## Features (v1)
- Multi-source ingestion (phone, camera SD, desktop folders, Google Photos, iCloud)
- Multi-target backup rules (S3/Wasabi/Backblaze B2, local NAS, USB auto-mount, LTO tape via LTFS)
- Automated deduplication & integrity verification (checksums, bit-rot detection)
- Smart album generation (by date, location, faces, events) with shareable links
- Cross-device web viewer with offline sync and progressive loading
- Offline/cold storage workflow (print barcode labels, track tape vault location)
- Health dashboard (backup status, storage usage, failed jobs, SLA compliance)
- One-click restore to any device or target
- Privacy-first: end-to-end encryption option, self-hosted mode
- WhatsApp bot for status alerts, quick shares, and restore requests

## MVP scope
Build a desktop agent (macOS/Windows/Linux) that watches designated folders, deduplicates, and pushes to 2 cloud targets (Backblaze B2 + S3-compatible) + 1 local USB/NAS. Add a simple web dashboard for viewing backup health and generating shareable album links. Skip tape/LTO, face recognition, and mobile apps for v1.

## Tech stack
Tauri (Rust + React) for cross-platform desktop agent, Node.js/TypeScript + Fastify for API & dashboard backend, PostgreSQL + Redis for metadata & job queue, Backblaze B2 / S3 API for cloud storage, MinIO for S3-compatible local/NAS target, React + TailwindCSS for web dashboard, Fly.io for hosting (global edge, persistent volumes), WhatsApp Business API via Twilio for bot integration

## Build estimate: 60 days

## Competitors & gaps
- **Arq Backup** — gap: No sharing, album generation, or cross-device viewer — pure backup only
- **Google Photos / iCloud** — gap: Locked ecosystem, no multi-cloud/offline/tape support, privacy concerns
- **Synology/NAS apps** — gap: Hardware-bound, no cloud multi-target, poor sharing UX
- **Backblaze Personal Backup** — gap: Single target only, no local/USB/tape, no album/sharing features
- **Immich / PhotoPrism** — gap: Self-hosted viewers only, no automated multi-target backup pipeline

## Landing page copy
- **Headline:** One Pipeline. Every Backup. Zero Effort.
- **Subheadline:** Connect your cameras, phones, and folders. ArchiveFlow automatically replicates to cloud, NAS, USB, and tape — then serves a beautiful, shareable library on every screen.
- Bullet: Set rules once → runs forever in the background
- Bullet: Backs up to Backblaze, S3, NAS, USB, and LTO tape
- Bullet: Deduplicates, verifies checksums, heals bit-rot
- Bullet: Auto-generates albums by event, person, place
- Bullet: Share a link — recipients view without accounts
- Bullet: Health dashboard + WhatsApp alerts for peace of mind
- **CTA:** Start Free 14-Day Trial

## WhatsApp-first bot
- **Flow:** User links phone number in dashboard → receives daily/weekly backup health summary → can reply 'SHARE [album]' to get a share link → 'RESTORE [date]' to queue a download → 'STATUS' for live sync progress → 'PAUSE'/'RESUME' to control the agent.
- **Commands:** STATUS, SHARE <album_name>, RESTORE <date_range>, PAUSE, RESUME, HEALTH, HELP
- **Pricing:** Included in Pro plan ($12/mo). Free tier gets weekly digest only.

## Pricing model: $12/mo Pro (unlimited sources/targets, sharing, WhatsApp bot, health alerts) | $5/mo Lite (2 cloud targets, local only, no sharing) | Self-hosted free (bring your own infra, community support)
