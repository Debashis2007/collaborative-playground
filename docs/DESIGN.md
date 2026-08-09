# Design: Collaborative Playground

**Project:** `collaborative-playground`  
**Parent system design:** `02-streaming-token-delivery.md / 10-global-realtime-product-surface.md`

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

Narrated with **ElevenLabs Debpro voice** and Debpro still image (via [GitaProject](/Users/deb/Development/GenAI/GitaProject)):

- Video: [`video/design-overview.mp4`](./video/design-overview.mp4)
- Script: [`video/narration.txt`](./video/narration.txt)

