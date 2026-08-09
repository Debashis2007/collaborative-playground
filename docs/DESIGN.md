# Design: Collaborative Playground

**Project:** `collaborative-playground`  
**Parent system design:** [02 — Streaming Token Delivery](https://github.com/Debashis2007/collaborative-playground/blob/main/02-streaming-token-delivery.md) · [10 — Global Realtime Product Surface](https://github.com/Debashis2007/collaborative-playground/blob/main/10-global-realtime-product-surface.md)

## 1. What this POC demonstrates

One owner starts a generation; many viewers fan out from the same token log (single GPU work).

## 2. Architecture (POC)

```text
POST /rooms → POST /rooms/{id}/start (owner) → POST /rooms/{id}/join (viewers)
```

## 3. Patterns used (and why)

| Pattern | Why used | Where in code |
|---------|----------|---------------|
| Single-writer generation | N viewers must not N× the model cost. | Owner-only `/start`. |
| Fanout from event log | All subscribers see the same seq order. | Shared `tokens` list. |
| Role ACL | Only owner controls cancel/regenerate. | 403 for non-owner start. |

## 4. Key endpoints

`GET /health`, `POST /rooms`, `POST /rooms/{id}/start`, `POST /rooms/{id}/join`

## 5. Tradeoffs / POC limits

No live SSE fanout broker — join returns snapshot for POC simplicity.

## 6. How to run

See the **Run (self-contained POC)** section in [`../README.md`](../README.md).

This folder is self-contained and can be published as its own GitHub repository.

## 7. Design walkthrough video

> **Watch on YouTube:** [Collaborative Playground — System Design #Shorts](https://youtu.be/YgqE_iyIIE8)
>
> Direct link: **https://youtu.be/YgqE_iyIIE8**

Also available in-repo:
- GIF preview: [`video/design-overview.gif`](./video/design-overview.gif)
- MP4 download: [`video/design-overview.mp4`](./video/design-overview.mp4)
- Narration script: [`video/narration.txt`](./video/narration.txt)

---

**Copyright (c) 2026 Debashis Bhattacharjee. All Rights Reserved.**  
Unauthorized copying or redistribution of this material is prohibited.  
GitHub: [Debashis2007](https://github.com/Debashis2007)

