"""One-line roast packager for The Long Roast."""
import json
import os
from pathlib import Path

GATE = {"min": 1, "max": 200}
STAMP = "roastline-2122"


def source_line():
    src = Path(__file__).resolve().parent / "entry.txt"
    return src.read_bytes().decode("utf-8").strip()


def guard(line):
    n = len(line)
    if n < GATE["min"] or n > GATE["max"]:
        raise SystemExit(f"roast rejected: {n} chars outside gate")
    return n


def deliver(line, n):
    dest = Path(os.environ.get("MAKEFUN_OUTPUT_DIR") or "out")
    dest.mkdir(parents=True, exist_ok=True)
    (dest / "entry.txt").write_bytes(line.encode("utf-8"))
    print(json.dumps({"status": "ROAST_PACKED", "stamp": STAMP,
                      "chars": n, "dest": str(dest)}))


if __name__ == "__main__":
    line = source_line()
    deliver(line, guard(line))
