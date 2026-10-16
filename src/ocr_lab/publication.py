"""Fail closed on dataset drift, missing responses, and public secret-like strings."""

import hashlib
import re
from pathlib import Path

from PIL import Image

from ocr_lab.evaluation import NAMES, analyze
from ocr_lab.records import read_cases, read_responses

SKIPPED = frozenset(
    {
        ".git",
        ".venv",
        "__pycache__",
        ".pytest_cache",
        ".ruff_cache",
        ".import_linter_cache",
        "private",
        "new-runs",
    }
)
SECRET_PATTERNS = [
    re.compile(r"sk-or-v1-[A-Za-z0-9]{32,}"),
    re.compile(r"gh[pousr]_[A-Za-z0-9]{30,}"),
    re.compile(r"-{5}BEGIN (?:RSA |EC |OPENSSH )?PRIVATE[ ]KEY-{5}"),
]


def public_files(root: Path) -> list[Path]:
    return [
        p for p in root.rglob("*") if p.is_file() and not set(p.relative_to(root).parts) & SKIPPED
    ]


def scan_text(text: str) -> bool:
    return any(pattern.search(text) for pattern in SECRET_PATTERNS)


def verify(root: Path) -> None:
    cases, responses = read_cases(root), read_responses(root / "data/synthetic/responses")
    expected = {(c.id, model) for c in cases for model in NAMES}
    observed = {(r.case_id, r.model) for r in responses}
    if len(cases) != 10 or len(responses) != len(expected) or observed != expected:
        raise ValueError("Incomplete or duplicated primary matrix")
    for case in cases:
        path = (root / case.image).resolve()
        if root.resolve() not in path.parents:
            raise ValueError("Dataset path escapes repository")
        if hashlib.sha256(path.read_bytes()).hexdigest() != case.sha256:
            raise ValueError(f"Image hash mismatch: {case.id}")
        with Image.open(path) as image:
            if image.getexif():
                raise ValueError(f"Unexpected EXIF metadata: {case.id}")
    for path in public_files(root):
        if path.suffix in {".png", ".jpg", ".pyc"}:
            continue
        text = path.read_text(errors="replace")
        if scan_text(text) or ("/" + "Users/") in text or ("/" + "var/folders/") in text:
            raise ValueError(f"Private material detected in {path.relative_to(root)}")
    report = analyze(root)
    if report["scored_calls"] != 40 or report["all_actual_cost_usd"] != "0.12700245":
        raise ValueError("Recorded budget or primary call count drifted")
    if any(row.finish_reason != "stop" for row in responses):
        raise ValueError("Truncated or failed primary response")
