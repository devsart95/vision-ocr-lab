"""Validated public artifact boundaries; no credentials or provider reasoning blobs."""

from decimal import Decimal
from pathlib import Path

from pydantic import BaseModel, ConfigDict, Field, JsonValue


class Case(BaseModel):
    model_config = ConfigDict(extra="forbid")
    id: str
    title: str
    image: str
    sha256: str
    expected: dict[str, JsonValue]
    tested: bool


class Response(BaseModel):
    model_config = ConfigDict(extra="forbid")
    case_id: str
    model: str
    returned_model: str | None = None
    provider: str | None = None
    seconds: float = Field(ge=0)
    content: str
    finish_reason: str | None
    cost_usd: Decimal = Field(ge=0)
    prompt_tokens: int = Field(ge=0)
    completion_tokens: int = Field(ge=0)
    reasoning_tokens: int = Field(ge=0)
    cached_tokens: int = Field(ge=0)
    cache_write_tokens: int = Field(ge=0)


def read_responses(directory: Path) -> list[Response]:
    return [
        Response.model_validate_json(path.read_text())
        for path in sorted(directory.glob("*__*.json"))
    ]


def read_cases(root: Path) -> list[Case]:
    from pydantic import TypeAdapter

    return TypeAdapter(list[Case]).validate_json((root / "data/synthetic/cases.json").read_text())
