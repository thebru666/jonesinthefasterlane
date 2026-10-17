#!/usr/bin/env python3
"""Arithmetic/score overlay for a proposal, not a game implementation."""
import argparse
import csv
import hashlib
import json
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "artifacts/planning/town-layout-v1/career-ledger.csv"
OUTPUT = ROOT / "artifacts/planning/learning-coverage-v1.json"


def score(work_time, qualifications):
    return min(100, work_time // 12 + 10 * qualifications)


def generate():
    examples = [(0,0,0),(6,0,0),(12,0,1),(119,0,9),(120,0,10),
                (600,0,50),(1200,0,100),(480,1,50),(360,2,50),(120,4,50),(0,1,10)]
    cases = []
    for work, qualifications, expected in examples:
        result = score(work, qualifications)
        assert result == expected
        cases.append(dict(work_time=work, unique_qualifications=qualifications,
                          learning=result, growth_allowance=5*(result//10)))
    # Effort fragmentation preserves total work credit/history steps. Growth
    # against changing job ceilings is not executed by this arithmetic check.
    assert sum([1]*60) == sum([6]*10)
    assert score(sum([1]*60),0) == score(sum([6]*10),0) == 5
    assert sum(((i+1)//6-i//6) for i in range(60)) == 10
    assert 45+20+5*(40//10) == 85
    assert min(100,10*((85-3)//8)) == 100
    groups = defaultdict(list)
    with SOURCE.open(newline="") as stream:
        for row in csv.DictReader(stream):
            groups[(row['layout'],row['route'],row['variant'])].append(row)
    overlay = []
    for (layout, route, variant), rows in groups.items():
        work_time = 0
        targets = {str(t):None for t in (10,20,50,100)}
        for row in rows:
            work_time += 6*int(row['shifts'])
            learning = score(work_time,int(row['completed_courses']))
            for target in targets:
                if targets[target] is None and learning >= int(target):
                    targets[target] = int(row['turn'])
        overlay.append(dict(layout=layout,route=route,variant=variant,final_work_time=work_time,
                            final_unique_qualifications=int(rows[-1]['completed_courses']),
                            final_learning=learning,first_target_turn=targets))
    return dict(status="PROPOSAL: arithmetic and score-only overlay on old schedules; NOT a new-rule game/cash/win simulation",
                formula="min(100, floor(successful actual work time/12) + 10*unique qualifications)",
                cash_and_work_history_recomputed=False,
                source_ledger="town-layout-v1/career-ledger.csv",
                source_sha256=hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
                cases=cases,partial_work_case="60*1 time and 10*6 time both earn Learning5 and ten history steps before ceiling effects",
                career_ceiling_case=dict(learning=40,declared_dependability=45,growth_allowance=20,ceiling=85,outgoing_dependability=82,career=100),
                excluded_failed_plan_partial_ledgers=True,coverage=overlay)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check',action='store_true')
    args = parser.parse_args()
    result = generate()
    if args.check:
        assert json.loads(OUTPUT.read_text()) == result
        print(f"Checked11 score cases, partial-work arithmetic, Career ceiling and {len(result['coverage'])} score-only overlays")
    else:
        OUTPUT.write_text(json.dumps(result,indent=2)+'\n')
        print(f"Wrote {OUTPUT.relative_to(ROOT)}")


if __name__ == '__main__':
    main()
