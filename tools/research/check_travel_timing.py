#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later
"""Check the bounded travel timing model, not an SCI interpreter or game port.

Original analytical code. Uses already tracked analytical place metadata; does
not copy coordinates, scripts or assets. The cycle schedule assumes the pinned
reference-engine ordering documented in travel-timing.md. No DOS execution.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PIN = "2b5f9b5d95f267c87889746906148db6088130f8"


def schedule(distance: int, speed: int, residual: int) -> tuple[int, int, int]:
    """Count observations by independent phase/step advancement, no arrival formula."""
    hours = calls = 0
    phase, steps = speed - 1, 0
    while True:
        phase += 1
        if phase == speed:
            phase = 0
            steps += 1
        if steps == distance:
            break
        calls += 1
        residual += 1
        if residual > 14 * speed:
            hours += 1
            residual = 0
    return calls, hours, residual


def check() -> dict:
    places = json.loads((ROOT / "artifacts/rules-audit/bytecode-flow-verification.json").read_text())["places"]
    cases = 0
    for distance in range(1, 86):
        for speed in range(1, 7):
            for residual in range(14 * speed + 1):
                calls, hours, remainder = schedule(distance, speed, residual)
                expected_calls = (distance - 1) * speed
                expected_hours, expected_remainder = divmod(residual + expected_calls, 14 * speed + 1)
                assert (calls, hours, remainder) == (expected_calls, expected_hours, expected_remainder)
                cases += 1
    assert schedule(1, 6, 84) == (0, 0, 84)
    # A threshold reduction may preserve a residue above the new threshold.
    # One subsequent nonarrival observation resets it, charging only one hour.
    assert schedule(2, 1, 84) == (1, 1, 0)
    matrix = []
    varying = []
    for a in places:
        row = []
        for b in places:
            delta = abs(a["ring_index"] - b["ring_index"])
            distance = min(delta, 170 - delta)
            row.append(distance)
            if a["place_id"] < b["place_id"] and distance:
                costs = [(distance - 1) * speed // (14 * speed + 1) for speed in range(1, 7)]
                if len(set(costs)) > 1:
                    varying.append({"from": a["place_id"], "to": b["place_id"], "distance": distance, "travel_hours_by_speed_1_to_6_at_residual_0": costs})
        matrix.append(row)
    resources = []
    for number in (0, 1, 101, 992, 994, 997, 998):
        path = ROOT / f"work/bytecode/decoded/script-{number:03}.json"
        decoded = json.loads(path.read_text())
        resource = ROOT / f"work/original-assets/decoded/resources/script.{number:03}.bin"
        actual_hash = hashlib.sha256(resource.read_bytes()).hexdigest()
        assert actual_hash == decoded["sha256"], f"payload mismatch: script{number}"
        resources.append({"script": number, "sha256": actual_hash})
    engine = ROOT / "work/audit/scummvm-engine-animate.cpp"
    engine_header = ROOT / "work/audit/scummvm-engine-animate.h"
    assert "kSignalFrozen        = 0x0100" in engine_header.read_text()
    board = json.loads((ROOT / "work/bytecode/decoded/script-001.json").read_text())
    signals = {o["name"]: next(p["value"] for p in o["properties"] if p["name"] == "signal") for o in board["objects"] if o["name"] in ("timeKeep", "marble")}
    assert signals == {"marble": 0, "timeKeep": 257}
    return {
        "research_date": "2026-10-16",
        "evidence": "BYTECODE + PINNED_REFERENCE_ENGINE + ANALYTICAL_CHECK; no original DOS execution",
        "version": "1.000.060",
        "bundle_sha256": "c08f3310f4f9cf47316bc32745507ae065bba7741430f7c3620602f534c46180",
        "resources": resources,
        "reference_engine": {
            "commit": PIN,
            "url": f"https://github.com/scummvm/scummvm/blob/{PIN}/engines/sci/graphics/animate.cpp",
            "retrieved": "2026-10-16",
            "sha256": hashlib.sha256(engine.read_bytes()).hexdigest(),
            "anchors": ["GfxAnimate::invoke lines135-176", "GfxAnimate::kernelAnimate lines649-675"],
            "signal_header_url": f"https://github.com/scummvm/scummvm/blob/{PIN}/engines/sci/graphics/animate.h#L30",
            "signal_header_sha256": hashlib.sha256(engine_header.read_bytes()).hexdigest(),
            "cast_signal_values": signals,
            "clock_exclusion": "timeKeep signal0x0101 contains frozen0x0100, preserved by View.init; automatic cast doit skips it",
        },
        "bytecode_anchors": {
            "101": ["init 0x000c-0x0066", "doit 0x0067-0x00a4", "next 0x00a5-0x0111", "at 0x0112-0x013b", "setDirection 0x013c-0x01c1"],
            "1": ["marbleMoved.cue 0x0158", "Place.handleEvent 0x022e", "room1.doit 0x2253", "arrival dispatch 0x2267-0x227d", "clock call 0x2290", "timeKeep.doit 0x24f8"],
            "992": ["Motion.moveDone 0x04c0", "Motion.motionCue 0x04d7"],
            "994": ["Game.doit 0x046d: Animate 0x0481; motionCue 0x0495; room doit 0x04a9; User doit 0x04b0"],
            "998": ["Act.doit 0x0489: mover doit 0x04cc", "Act.motionCue 0x068c"],
            "997": ["speed menu 0x0576-0x063a: reset movement phase 0x0606; threshold setter 0x063a"],
        },
        "assumptions": ["distinct endpoints on ordinary ring", "speed constant 1..6", "initial residual 0..14*speed", "no turn exhaustion, frozen actor, reroute, modal suspension or external state mutation", "one normal cast update followed by board update per observed cycle"],
        "formula": {"distance": "min(abs(a-b),170-abs(a-b))", "arrival_cycle": "1+(distance-1)*speed", "no_argument_clock_calls": "(distance-1)*speed", "travel_hours": "floor((initial_residual+clock_calls)/(14*speed+1))", "final_residual": "(initial_residual+clock_calls) mod (14*speed+1)", "entry_cost": "2 separately, capped together with spent hours at60"},
        "checked_distance_speed_residual_cases": cases,
        "boundary_fixtures": ["distance1 speed6 residual84: zero travel calls, no charge", "speed reduced6to1 with residual84: next nonarrival call charges1 and resets0, not5hours"],
        "failures": 0,
        "matrix_place_order": [p["place_id"] for p in places],
        "matrix_semantics": "shortest ring steps; diagonal0 means same endpoint, not a MarblePath zero-step completion contract",
        "route_step_matrix": matrix,
        "speed_sensitive_pairs_at_zero_residual": varying,
        "limits": ["formula is conditional analytical consequence, not observed DOS timing", "speed-change overflow residue is reset after one hour, not divided", "same-place mover and interruption paths require stateful recurrence, not diagonal formula", "elapsed wall-clock seconds are not game hours"],
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT / "artifacts/rules-audit/travel-timing-verification.json")
    args = parser.parse_args()
    result = check()
    args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(f"Checked {result['checked_distance_speed_residual_cases']} analytical cases; 0 failures; wrote {args.output}")
