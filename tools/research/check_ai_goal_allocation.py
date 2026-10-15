#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later
"""Check AI-001 target-allocation arithmetic, independently of the SCI runtime.

This is original analytical code, not a copy/translation of original game code.
It enumerates the documented formula and proves interval/capacity properties for
legal human goals. It does not execute the original random draws or redistribution
retry loop, validate decompilation, or measure original-game behavior.

Run from any directory; defaults to the tracked metadata artifact in this repo.
"""
from __future__ import annotations

import argparse
import itertools
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_OUTPUT = ROOT / "artifacts/rules-audit/ai-goal-allocation-check.json"


def check() -> dict:
    configurations = 0
    draw_pairs = 0
    failures = []
    for goals in itertools.product(range(10, 101, 10), repeat=4):
        for offset in (10, 0, -10):
            configurations += 1
            total = max(40, min(400, sum(goals) + 4 * offset))
            wealth = max(10, min(100, goals[0] + offset))
            remainder = total - wealth
            low = max(1, remainder // 30 - 2)
            high = min(10, remainder // 30 + 2)
            if low > high:
                failures.append([goals, offset, "invalid_random_bounds"])
            possible_targets = range(low * 10, high * 10 + 1, 10)
            for happiness, education in itertools.product(possible_targets, repeat=2):
                draw_pairs += 1
                career = remainder - happiness - education
                redistribution = career - max(10, min(100, career))
                categories = (wealth, happiness, education)
                if redistribution > 0:
                    capacity = sum(100 - value for value in categories)
                else:
                    capacity = sum(value - 10 for value in categories)
                if abs(redistribution) > capacity or redistribution % 10:
                    failures.append([
                        goals, offset, happiness, education, career, "redistribution"
                    ])
    return {
        "research_date": "2026-10-15",
        "evidence": "ANALYTICAL_CHECK",
        "reference": "Published select4.sc at sluicebox/sci-scripts commit "
                     "870a8015b689474484bf3d8b41416956d4315432",
        "rule_id": "AI-001",
        "method": "Enumerate all human goals 10..100 by tens and three offsets. "
                  "Enumerate all happiness/education draw pairs in the derived inclusive "
                  "bounds. Check random interval validity and whether excess/shortfall "
                  "career allocation can be redistributed in tens within "
                  "wealth/happiness/education category limits. This is an independent "
                  "mathematical check, not execution of the original SCI program, RNG, "
                  "or redistribution retry loop.",
        "configurations": configurations,
        "draw_pairs": draw_pairs,
        "failures": failures,
        "result": (
            "All tested intervals are valid and redistribution capacity is sufficient; "
            "no runtime outcome or timing verified."
            if not failures else "Arithmetic property check failed; inspect failures."
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    result = check()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(f"Checked {result['configurations']} configurations / "
          f"{result['draw_pairs']} draw pairs; failures: {len(result['failures'])}")
    print(args.output.resolve())
    return 1 if result["failures"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
