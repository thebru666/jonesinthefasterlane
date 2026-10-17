#!/usr/bin/env python3
"""A bounded paper-budget worksheet, NOT the successor game's simulation.

Whole-shift/lesson schedules, fixed visit allowances and deterministic eligible
hires isolate career investment. See the linked planning note for exclusions.
"""
import argparse
import csv
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "artifacts/planning/career-comparison-v1"

JOBS = {
    "service": dict(wage=8, experience=20, dependability=20, courses=0, clothing="casual"),
    "butcher": dict(wage=12, experience=30, dependability=30, courses=1, clothing="casual"),
    "electrician": dict(wage=18, experience=35, dependability=35, courses=2, clothing="casual"),
    "plumber": dict(wage=18, experience=35, dependability=35, courses=2, clothing="casual"),
    "clinic_support": dict(wage=10, experience=30, dependability=30, courses=2, clothing="casual"),
    "doctor": dict(wage=30, experience=40, dependability=40, courses=4, clothing="dress"),
}
PATHS = {
    "butcher": ["Trade School"],
    "electrician": ["Trade School", "Electrical Skills"],
    "plumber": ["Trade School", "Plumbing Skills"],
    "doctor": ["General Studies", "Science Foundations", "Medical Studies", "Clinical Qualification"],
}
INPUTS = dict(
    status="PROPOSAL / bounded paper worksheet; not measured gameplay or full win balance",
    horizon=24, allowance=60, action_time=6, application_time=4, gross_shift_factor=8,
    cash=200, initial_job="service", actual_experience=22, dependability=25,
    initial_casual_units=6, initial_dress_units=0, prepaid_rent_turns=3,
    lessons_per_course=10, fee_per_course=50, max_lessons_per_turn=4,
    food_per_turn=79, rent_every_four_turns=325,
    casual_price=73, casual_units=11, dress_price=125, dress_units=13,
    visit_allowance="Each required visit reserves a two-edge trip plus two entry time; no return home is charged",
    bus_time_per_visit=6, bus_fare_per_visit=3, bike_time_per_visit=5, bike_price=120,
    exclusions=["original fresh-game opening", "actual town tour geometry", "random openings except one specified rejection", "economy price/wage generation", "partial shifts/lessons", "equipment credits", "Happiness/relaxation/events", "full four-goal finish", "savings/loans", "home-working/offers", "optimal play"],
    jobs=JOBS, paths=PATHS,
    variants={"bus": "ordinary fixed-price worksheet", "buy_bike": "buy a bike on turn1 including visit; subsequent bike travel",
              "one_rejection": "first eligible application to the target role fails once, costing4 time",
              "lost_time": "12 extra time consumed on turn4, no cash grant",
              "keep_buffer": "choose lessons only if closing cash stays at least100"},
)


def fees_for(progress, count):
    """One enrollment at the first lesson of each course, including mid-visit starts."""
    return sum(50 for lesson in range(progress, progress + count) if lesson % 10 == 0)


def compare(route, variant, horizon=24, visit_budget=None, career_ladder=None, job_definitions=None, course_path=None):
    job_specs = JOBS if job_definitions is None else job_definitions
    course_names = PATHS[route] if course_path is None else course_path
    goal = 10 * len(course_names)
    cash, experience, dependability = 200, 22, 25
    casual, dress = 6, 0
    progress, job, max_experience = 0, "service", 30
    bike_owned, rejected = False, False
    hired_turn, tuition_total = None, 0
    rows = []
    for turn in range(1, horizon + 1):
        if turn > 1:
            casual, dress = max(0, casual - 1), max(0, dress - 1)
        degrees = progress // 10
        desired = route
        if route == "doctor" and degrees < 4:
            desired = "clinic_support" if degrees >= 2 else "service"
        if career_ladder:
            desired = job
            current_rank = career_ladder.index(job) if job in career_ladder else -1
            for rank, candidate in enumerate(career_ladder):
                c = job_specs[candidate]
                if (rank > current_rank and degrees >= c["courses"]
                        and experience >= c["experience"] and dependability >= c["dependability"]):
                    desired = candidate
        spec = job_specs[desired]
        eligible = (degrees >= spec["courses"] and experience >= spec["experience"]
                    and dependability >= spec["dependability"])
        attempt = desired != job and eligible
        reject = attempt and desired == route and variant == "one_rejection" and not rejected
        if reject:
            rejected = True
        next_job = desired if attempt and not reject else job
        next_spec = job_specs[next_job]
        purchase_clothes = not (dress > 0 or (next_spec["clothing"] == "casual" and casual > 0))
        clothing_cost = (125 if next_spec["clothing"] == "dress" else 73) if purchase_clothes else 0
        buy_bike = variant in ("buy_bike", "bike_buffer") and not bike_owned
        purchase_cost = 120 if buy_bike else 0
        rent = 325 if turn % 4 == 0 else 0
        event_time = 12 if variant == "lost_time" and turn == 4 else 0
        application = 4 if attempt else 0
        opening_cash = cash
        chosen = None
        # Plan before visiting: preserve all obligations, choose as much study as
        # affordable (up to four lessons), then whole shifts fitting that budget.
        for lessons in range(min(4, goal - progress), -1, -1):
            visits = 2 + bool(lessons) + bool(rent) + purchase_clothes + buy_bike
            if visit_budget is not None:
                travel_time, fares, visits = visit_budget(
                    job=next_job, study=bool(lessons), rent=bool(rent),
                    clothes=bool(purchase_clothes), buy_bike=bool(buy_bike),
                    bike_owned=bike_owned)
            elif bike_owned:
                travel_time, fares = 5 * visits, 0
            elif buy_bike:
                # First visit reaches the bike seller by bus; later trips use it.
                travel_time, fares = 6 + 5 * (visits - 1), 3
            else:
                travel_time, fares = 6 * visits, 3 * visits
            room = 60 - travel_time - application - event_time - lessons * 6
            shifts = max(0, room // 6)
            wage = next_spec["wage"]
            gross = shifts * 8 * wage
            tuition = fees_for(progress, lessons)
            closing = cash + gross - (fares + clothing_cost + purchase_cost + rent + 79 + tuition)
            # Bus to any needed shop, clothes and bike are paid before working.
            # Tuition, food and rent are paid after the reserved work block.
            if room >= 0 and closing >= (100 if variant in ("keep_buffer", "bike_buffer") else 0) and cash >= fares + clothing_cost + purchase_cost:
                chosen = lessons, visits, travel_time, fares, shifts, gross, tuition, closing
                break
        if chosen is None:
            raise ValueError(f"Unfunded plan: {route}/{variant}/turn{turn}")
        lessons, visits, travel_time, fares, shifts, gross, tuition, cash = chosen
        if purchase_clothes:
            if next_spec["clothing"] == "dress":
                dress += 13
            else:
                casual += 11
        if buy_bike:
            bike_owned = True
        if next_job != job:
            experience += 2
            max_experience = next_spec["experience"] + 10
            dependability = max(10, dependability)
            job = next_job
            if job == route:
                hired_turn = turn
        # Full shifts happen before the school visit, so graduation credits do
        # not retroactively increase their growth ceilings.
        for _ in range(shifts):
            if experience < max_experience + 5 * degrees:
                experience += 1
            if dependability < job_specs[job]["dependability"] + 20 + 5 * degrees:
                dependability += 1
        previous_degrees = degrees
        progress += lessons
        degrees = progress // 10
        dependability += (degrees - previous_degrees) * 5
        dependability = max(0, dependability - 3)
        tuition_total += tuition
        used_time = travel_time + application + event_time + (shifts + lessons) * 6
        assert used_time <= 60 and cash >= 0
        assert cash == opening_cash + gross - fares - clothing_cost - purchase_cost - rent - 79 - tuition
        rows.append(dict(route=route, variant=variant, turn=turn, opening_cash=opening_cash,
                         job=job, shifts=shifts, gross_pay=gross, lessons=lessons,
                         lessons_total=progress, completed_courses=degrees, tuition=tuition,
                         visits=visits, travel_and_entry_time=travel_time, fares=fares,
                         food=79, rent=rent, clothing=clothing_cost, bicycle=purchase_cost,
                         application_time=application, rejection=int(reject), event_time=event_time,
                         total_time=used_time, unused_time=60-used_time, closing_cash=cash,
                         actual_experience=experience, end_dependability=dependability,
                         education_reference_score=0 if degrees == 0 else min(100, 1 + 9 * degrees)))
    assert progress == goal, (route, variant, "course path unfinished")
    assert hired_turn is not None, (route, variant, "target not hired")
    summary = dict(route=route, variant=variant, courses=len(course_names),
                   qualification_turn=next(r["turn"] for r in rows if r["lessons_total"] == goal) if goal else None,
                   target_hired_turn=hired_turn, tuition=tuition_total,
                   minimum_closing_cash=min(r["closing_cash"] for r in rows),
                   **{f"cash_turn_{t}": rows[t-1]["closing_cash"] for t in (4, 8, 12, 16, 20, 24)},
                   education_reference_score=rows[-1]["education_reference_score"],
                   end_dependability=rows[-1]["end_dependability"],
                   career_reference_score=min(100, 10 * (rows[-1]["end_dependability"] // 8)))
    return rows, summary


def draw_chart(rows, destination):
    colors = {"butcher": "#b86420", "electrician": "#227f82", "doctor": "#7654a1"}
    series = {name: [r for r in rows if r["route"] == name and r["variant"] == "bus"] for name in colors}
    high = math.ceil(max(r["closing_cash"] for line in series.values() for r in line) / 2000) * 2000
    x = lambda t: 95 + (t-1) * 40
    y = lambda cash: 480 - cash / high * 350
    svg = ['<svg xmlns="http://www.w3.org/2000/svg" width="1180" height="600" viewBox="0 0 1180 600">',
           '<rect width="1180" height="600" fill="#fffaf0"/>',
           '<g font-family="Arial,sans-serif" fill="#193743">',
           '<text x="45" y="40" font-size="26" font-weight="bold">Career investment: provisional paper comparison</text>',
           '<text x="45" y="68" font-size="16">Same early-employed checkpoint · fixed prices · bus · no full-game win claim</text>']
    for amount in range(0, high+1, 2000):
        yy = y(amount)
        svg += [f'<line x1="95" y1="{yy}" x2="1015" y2="{yy}" stroke="#d7dedb"/>',
                f'<text x="82" y="{yy+5}" text-anchor="end" font-size="14">${amount:,}</text>']
    for t in (1, 4, 8, 12, 16, 20, 24):
        svg.append(f'<text x="{x(t)}" y="510" text-anchor="middle" font-size="15">{t}</text>')
    for name, line in series.items():
        points = " ".join(f'{x(r["turn"])},{y(r["closing_cash"]):.1f}' for r in line)
        svg.append(f'<polyline points="{points}" fill="none" stroke="{colors[name]}" stroke-width="4"/>')
    for i, (name, color) in enumerate(colors.items()):
        label = "Electrician / plumber" if name == "electrician" else name.title()
        svg.append(f'<text x="{95+i*300}" y="555" fill="{color}" font-size="18" font-weight="bold">{label}</text>')
    svg += ['<text x="950" y="535" font-size="15">Comparison turn</text>',
            '<text x="45" y="584" font-size="13">Cash after study, food, rent, clothes and fares; possessions/goal scores are not cash. PROPOSAL.</text>', '</g></svg>']
    destination.write_text("\n".join(svg) + "\n")


def generate():
    rows, summaries = [], []
    for route in PATHS:
        for variant in ("bus", "buy_bike", "one_rejection", "lost_time", "keep_buffer"):
            detail, summary = compare(route, variant)
            rows.extend(detail)
            summaries.append(summary)
    # Two deliberately mirrored trades are a neutral comparison, not evidence
    # that equivalent real careers pay identically.
    for variant in ("bus", "buy_bike", "one_rejection", "lost_time", "keep_buffer"):
        a = next(s for s in summaries if s["route"] == "electrician" and s["variant"] == variant)
        b = next(s for s in summaries if s["route"] == "plumber" and s["variant"] == variant)
        assert {k:v for k,v in a.items() if k != "route"} == {k:v for k,v in b.items() if k != "route"}
    return rows, summaries


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="recalculate and compare committed tables")
    args = parser.parse_args()
    rows, summaries = generate()
    if args.check:
        assert json.loads((OUT / "inputs.json").read_text()) == INPUTS
        assert json.loads((OUT / "summary.json").read_text()) == summaries
        with (OUT / "turn-ledger.csv").open(newline="") as stream:
            actual = list(csv.DictReader(stream))
        assert actual == [{k:str(v) for k,v in r.items()} for r in rows]
        print(f"Checked {len(rows)} budget rows and {len(summaries)} summaries; no gameplay/balance claim")
        return
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "inputs.json").write_text(json.dumps(INPUTS, indent=2) + "\n")
    (OUT / "summary.json").write_text(json.dumps(summaries, indent=2) + "\n")
    with (OUT / "turn-ledger.csv").open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    draw_chart(rows, OUT / "cash-comparison.svg")
    print(json.dumps(summaries, indent=2))


if __name__ == "__main__":
    main()
