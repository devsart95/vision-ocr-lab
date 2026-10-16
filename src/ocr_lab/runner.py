"""Explicit single-call replay; never writes into the published evidence."""

import base64
import hashlib
import json
import os
import time
import urllib.request
from decimal import Decimal
from pathlib import Path
from uuid import uuid4

from pydantic import BaseModel, Field

from ocr_lab.domain import JSON
from ocr_lab.evaluation import NAMES
from ocr_lab.records import Response, read_cases


class Message(BaseModel):
    content: str | None = None


class Choice(BaseModel):
    message: Message
    finish_reason: str | None = None


class Usage(BaseModel):
    cost: Decimal
    prompt_tokens: int = 0
    completion_tokens: int = 0
    completion_tokens_details: dict[str, int] = Field(default_factory=dict)
    prompt_tokens_details: dict[str, int] = Field(default_factory=dict)


class Envelope(BaseModel):
    model: str | None = None
    provider: str | None = None
    choices: list[Choice]
    usage: Usage


def replay(root: Path, case_id: str, model: str, execute: bool) -> Path | None:
    cases = {c.id: c for c in read_cases(root)}
    if case_id not in cases or model not in NAMES:
        raise ValueError("Choose a published case ID and one of the four recorded model IDs")
    case = cases[case_id]
    if not execute:
        return None
    key = os.environ.get("OPENROUTER_API_KEY")
    if not key:
        raise ValueError("Set OPENROUTER_API_KEY in the process environment")
    image = (root / case.image).read_bytes()
    if hashlib.sha256(image).hexdigest() != case.sha256:
        raise ValueError("Image hash does not match the dataset")
    record = request(root, case_id, model, key, image)
    folder = root / "new-runs"
    folder.mkdir(exist_ok=True)
    path = folder / f"{case_id}__{model.replace('/', '__')}__{uuid4().hex[:12]}.json"
    path.write_text(record.model_dump_json(indent=2) + "\n")
    return path


def request(root: Path, case_id: str, model: str, key: str, image: bytes) -> Response:
    content: list[JSON] = [
        {"type": "text", "text": (root / "data/synthetic/prompt.txt").read_text().strip()},
        {
            "type": "image_url",
            "image_url": {"url": "data:image/png;base64," + base64.b64encode(image).decode()},
        },
    ]
    body = {
        "model": model,
        "messages": [{"role": "user", "content": content}],
        "max_tokens": 4096,
        "reasoning": {"effort": "low", "exclude": True},
        "usage": {"include": True},
    }
    req = urllib.request.Request(
        "https://openrouter.ai/api/v1/chat/completions",
        data=json.dumps(body).encode(),
        headers={"Authorization": "Bearer " + key, "Content-Type": "application/json"},
    )
    start = time.perf_counter()
    with urllib.request.urlopen(req, timeout=180) as response:
        result = Envelope.model_validate_json(response.read())
    if not result.choices:
        raise ValueError("Provider returned no completion")
    choice, usage = result.choices[0], result.usage
    return Response(
        case_id=case_id,
        model=model,
        returned_model=result.model,
        provider=result.provider,
        seconds=round(time.perf_counter() - start, 3),
        content=choice.message.content or "",
        finish_reason=choice.finish_reason,
        cost_usd=usage.cost,
        prompt_tokens=usage.prompt_tokens,
        completion_tokens=usage.completion_tokens,
        reasoning_tokens=usage.completion_tokens_details.get("reasoning_tokens", 0),
        cached_tokens=usage.prompt_tokens_details.get("cached_tokens", 0),
        cache_write_tokens=usage.prompt_tokens_details.get("cache_write_tokens", 0),
    )
