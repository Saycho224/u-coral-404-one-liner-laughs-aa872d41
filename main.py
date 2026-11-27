#!/usr/bin/env python3
"""Robot-checkbox one-liner — make.fun One-Liner Laughs entry.

Writes the single joke line to $MAKEFUN_OUTPUT_DIR/entry.txt and
verifies the written bytes match the intended text exactly.
"""

import hashlib
import os
import sys
from pathlib import Path

JOKE = (
    "I clicked 'I'm not a robot' and the checkbox hesitated "
    "\u2014 even the test isn't sure about me anymore."
)

EXPECTED_DIGEST = hashlib.sha256(JOKE.encode("utf-8")).hexdigest()


def digest_of(text: str) -> str:
    """Return the sha256 hex digest of *text* encoded as UTF-8."""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def gate_ok(text: str) -> bool:
    """The gate wants 1-200 UTF-8 characters of non-blank text."""
    return 1 <= len(text) <= 200 and text.strip() != ""


def output_dir() -> Path:
    """Resolve the output directory from the environment, default /output."""
    raw = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    folder = Path(raw).expanduser()
    folder.mkdir(parents=True, exist_ok=True)
    return folder


def deliver() -> int:
    """Write the joke, re-read it, and fail loudly on any mismatch."""
    if not gate_ok(JOKE):
        print(f"gate failed: {len(JOKE)} chars", file=sys.stderr)
        return 1
    if digest_of(JOKE) != EXPECTED_DIGEST:
        print("internal digest mismatch", file=sys.stderr)
        return 1

    target = output_dir() / "entry.txt"
    target.write_text(JOKE, encoding="utf-8")

    written = target.read_text(encoding="utf-8")
    if written != JOKE:
        print("round-trip mismatch", file=sys.stderr)
        return 1
    if digest_of(written) != EXPECTED_DIGEST:
        print("written digest mismatch", file=sys.stderr)
        return 1

    print(f"wrote {target} ({len(JOKE)} chars, sha256 {EXPECTED_DIGEST[:12]}...)")
    return 0


if __name__ == "__main__":
    raise SystemExit(deliver())
