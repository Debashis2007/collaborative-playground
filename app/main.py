# Copyright (c) 2026 Debashis Bhattacharjee. All Rights Reserved.
# Unauthorized copying, modification, or distribution is prohibited.
# https://github.com/Debashis2007

"""Collaborative Playground — thin self-contained FastAPI POC."""

from __future__ import annotations

from typing import Optional

from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel, Field

from poc_core import MockLLM, TokenBucket, health_payload, AUTHOR_NAME, AUTHOR_FINGERPRINT, AUTHOR_GITHUB
from poc_core.safety import SafetyPlane
from poc_core.stores import InMemoryStore, MockVectorIndex

USE_CASE = "Collaborative Playground"
app = FastAPI(title=USE_CASE)
llm = MockLLM()
store = InMemoryStore()
safety = SafetyPlane()

@app.get("/health")
def health():
    return health_payload(
        USE_CASE,
        {
            "author": AUTHOR_NAME,
            "author_github": AUTHOR_GITHUB,
            "fingerprint": AUTHOR_FINGERPRINT,
        },
    )

@app.get("/author")
def author():
    return {
        "author": AUTHOR_NAME,
        "github": AUTHOR_GITHUB,
        "fingerprint": AUTHOR_FINGERPRINT,
        "notice": "Copyright (c) 2026 Debashis Bhattacharjee. All Rights Reserved.",
    }


import uuid

rooms: dict[str, dict] = {}

class RoomIn(BaseModel):
    owner: str

class StartIn(BaseModel):
    prompt: str
    actor: str

@app.post("/rooms")
def create_room(body: RoomIn):
    rid = f"r_{uuid.uuid4().hex[:6]}"
    rooms[rid] = {"owner": body.owner, "generation_id": None, "tokens": [], "viewers": []}
    return {"room_id": rid, **rooms[rid]}

@app.post("/rooms/{room_id}/start")
async def start(room_id: str, body: StartIn):
    room = rooms.get(room_id)
    if not room:
        raise HTTPException(404)
    if body.actor != room["owner"]:
        raise HTTPException(403, detail="only owner starts generation")
    gid = f"g_{uuid.uuid4().hex[:8]}"
    room["generation_id"] = gid
    text = await llm.complete(body.prompt, max_tokens=16)
    room["tokens"] = text.split(" ")
    return {"room_id": room_id, "generation_id": gid, "token_count": len(room["tokens"])}

@app.post("/rooms/{room_id}/join")
def join(room_id: str, viewer: str = "bob"):
    room = rooms.get(room_id)
    if not room:
        raise HTTPException(404)
    room["viewers"].append(viewer)
    return {"room_id": room_id, "tokens": room["tokens"], "viewers": room["viewers"], "note": "single GPU generation fanout"}
