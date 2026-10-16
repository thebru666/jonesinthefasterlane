#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later
"""Enumerate analytical lottery examples; this does not execute the original game.

Original research code derived from the formulas documented in EVENT-004.
No original game source, bytecode or resource payload is included or required.
"""
import argparse
from collections import Counter
from fractions import Fraction
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / 'artifacts/rules-audit/lottery-probability-check.json'
EXPECTED_COUNTS = {10: (1, 2, 7), 20: (2, 3, 15), 100: (6, 15, 79)}


def rational(value):
    return {'fraction': str(value), 'decimal': round(float(value), 8)}


def generate():
    records = []
    for quantity, expected in EXPECTED_COUNTS.items():
        prizes = Counter()
        happiness = Counter()
        for draw in range(501):
            prize = 0
            bonus = 0
            if quantity > draw:
                if draw <= quantity // 20:
                    prize, bonus = 5000, 10
                elif draw <= quantity // 5:
                    prize, bonus = 500, 5
                else:
                    prize, bonus = 200, 5
            prizes[prize] += 1
            happiness[bonus] += 1
        actual = tuple(prizes[p] for p in (5000, 500, 200))
        if actual != expected or sum(prizes.values()) != 501:
            raise ValueError(f'Unexpected prize distribution for {quantity}: {actual}')
        expected_cash = Fraction(sum(p * n for p, n in prizes.items()), 501)
        records.append({
            'tickets': quantity,
            'draw_cases': 501,
            'prize_outcomes': {str(p): prizes[p] for p in (0, 200, 500, 5000)},
            'happiness_outcomes_before_clamping': {
                str(p): happiness[p] for p in (0, 5, 10)
            },
            'winning_probability': rational(Fraction(quantity, 501)),
            'purchase_cost_dollars': quantity,
            'expected_cash_prize_dollars': rational(expected_cash),
            'expected_cash_net_after_purchase_dollars': rational(expected_cash - quantity),
        })
    return {
        'rule_id': 'EVENT-004',
        'evidence': 'ANALYTICAL: exhaustive integer draw enumeration, not gameplay or package-bytecode execution.',
        'source_revision': '870a8015b689474484bf3d8b41416956d4315432',
        'source_url': 'https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/startTrn.sc#L214',
        'assumptions': [
            'Independent uniform draw among the 501 integers 0 through 500 inclusive.',
            'Positive ordinary ticket quantities without signed integer overflow.',
            'Ticket purchase costs $1 each, sold in batches of ten.',
            'Cash expectation excludes travel, other opportunities and happiness utility.',
            'Happiness outcome counts precede the shared 0–100 clamp.',
        ],
        'enumerated_cases': sum(r['draw_cases'] for r in records),
        'cases': records,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true',
                        help='Verify tracked metadata without changing it.')
    args = parser.parse_args()
    result = generate()
    if args.check:
        if json.loads(OUTPUT.read_text(encoding='utf-8')) != result:
            raise SystemExit('Lottery metadata differs; rerun without --check and review the change.')
        print(f"Verified {result['enumerated_cases']} analytical lottery cases against tracked metadata.")
    else:
        OUTPUT.parent.mkdir(parents=True, exist_ok=True)
        OUTPUT.write_text(json.dumps(result, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
        print(f"Wrote {result['enumerated_cases']} analytical lottery cases to {OUTPUT.relative_to(ROOT)}.")


if __name__ == '__main__':
    main()
