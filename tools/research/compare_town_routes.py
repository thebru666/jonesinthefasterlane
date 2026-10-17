#!/usr/bin/env python3
"""Generate a static town schematic and bounded analytical route comparisons."""
import argparse
import csv
import html
import json
import math
from pathlib import Path
from compare_career_budgets import compare, JOBS, PATHS

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "artifacts/planning/town-layout-v1"
CONFIG = json.loads((OUT / "inputs.json").read_text())
ORDER = [s["id"] for s in CONFIG["stops"]]
ALTERNATIVE = ORDER.copy()
A, B = (ORDER.index(s) for s in CONFIG["alternative_swap"])
ALTERNATIVE[A], ALTERNATIVE[B] = ALTERNATIVE[B], ALTERNATIVE[A]
MODES = ("walk", "bike", "bus", "car")


def distance(a, b, order=ORDER):
    difference = abs(order.index(a) - order.index(b))
    return min(difference, len(order) - difference)


def route(stops, mode, order=ORDER, acquiring_bike=False):
    total_time, total_cash, legs = 0, 0, []
    driving_paid = False
    bike_acquired = False
    for start, end in zip(stops, stops[1:]):
        d = distance(start, end, order)
        if d == 0:
            continue
        actual_mode = ("bike" if bike_acquired else "bus") if acquiring_bike else mode
        travel, cash = {
            "walk": (3*d, 0), "bike": (math.ceil(1.5*d), 0),
            "bus": (2+d, 3), "car": (1+math.ceil(d/2), 4 + (0 if driving_paid else 20)),
        }[actual_mode]
        if actual_mode == "car":
            driving_paid = True
        legs.append(dict(start=start, end=end, distance=d, mode=actual_mode,
                         travel_time=travel, entry_time=2, cash=cash))
        total_time += travel + 2
        total_cash += cash
        if acquiring_bike and end == "reboot":
            bike_acquired = True
    return dict(stops=stops, mode=mode, legs=legs, distance=sum(l["distance"] for l in legs),
                visits=len(legs), travel_and_entry_time=total_time, cash=total_cash,
                time_left=60-total_time, full_action_slots=max(0, (60-total_time)//6))


def itinerary(job, study, rent, clothes, buy_bike=False, home="starter-court"):
    stops = [home]
    if buy_bike:
        stops.append("reboot")
    if clothes:
        stops.append("good-threads")
    stops.append(CONFIG["job_locations"][job])
    if study:
        stops.append("next-chapter")
    if rent:
        stops.append("civic-house")
    stops.append(CONFIG["food_stop"])
    return stops


def budget(order, home):
    def calculate(job, study, rent, clothes, buy_bike, bike_owned):
        stops = itinerary(job, study, rent, clothes, buy_bike, home)
        result = route(stops, "bike" if bike_owned else "bus", order, acquiring_bike=buy_bike)
        return result["travel_and_entry_time"], result["cash"], result["visits"]
    return calculate


def render_map(destination, order=ORDER, name="A"):
    colours = {"home":"#f1d7b0", "study":"#c9e6dc", "services":"#d8e8f0", "work":"#f4e8ce"}
    centres = [(900 + 690*math.cos(-math.pi/2 + i*2*math.pi/15),
                650 + 455*math.sin(-math.pi/2 + i*2*math.pi/15)) for i in range(15)]
    svg = ['<svg xmlns="http://www.w3.org/2000/svg" width="1800" height="1280" viewBox="0 0 1800 1280">',
           '<rect width="1800" height="1280" fill="#fffaf0"/>',
           '<g font-family="Arial,sans-serif" fill="#183b48">',
           '<text x="70" y="60" font-size="34" font-weight="bold">Fifteen-stop working town</text>',
           f'<text x="70" y="98" font-size="21">PROPOSAL {name} · equal logical edges · clockwise order, travel in either direction</text>']
    for i, (x,y) in enumerate(centres):
        nx,ny = centres[(i+1)%15]
        svg.append(f'<line x1="{x:.1f}" y1="{y:.1f}" x2="{nx:.1f}" y2="{ny:.1f}" stroke="#839fa3" stroke-width="6"/>')
    lookup = {s["id"]:s for s in CONFIG["stops"]}
    for i, (stop_id, (x,y)) in enumerate(zip(order, centres)):
        s = lookup[stop_id]
        svg += [f'<rect x="{x-125:.1f}" y="{y-55:.1f}" width="250" height="110" rx="14" fill="{colours[s["group"]]}" stroke="#5c7b80" stroke-width="2"/>',
                f'<text x="{x-110:.1f}" y="{y-30:.1f}" font-size="16" font-weight="bold">{i+1:02d}</text>']
        lines = s["name"].split(" / ")
        for j, line in enumerate(lines):
            svg.append(f'<text x="{x:.1f}" y="{y-5+24*j:.1f}" text-anchor="middle" font-size="19" font-weight="bold">{html.escape(line)}</text>')
        subtitle = s["subtitle"]
        # Descriptive subtitle wraps separately from the always-visible name.
        if len(subtitle) > 34:
            subtitle = "Electrical, plumbing, industry"
        svg.append(f'<text x="{x:.1f}" y="{y+45:.1f}" text-anchor="middle" font-size="14">{html.escape(subtitle)}</text>')
    for y, text, size in [(500,"Time versus money",32),(550,"Walk · Bike · Bus · Car",25),
                           (595,"Bus available at every stop",22),(650,"Shared site = one arrival",22),
                           (690,"Distinct employers = distinct jobs",22),(745,"Clinic near college" if name == "A" else "Longer clinic-to-college journey",22),
                           (785,"Alternative B swaps clinic and parcel depot",19)]:
        svg.append(f'<text x="900" y="{y}" text-anchor="middle" font-size="{size}">{html.escape(text)}</text>')
    svg += ['<text x="70" y="1207" font-size="20">One edge = one logical distance unit. Schematic geometry is not a physical-distance scale.</text>',
            '<text x="70" y="1240" font-size="19">15 stops accepted as working direction; exact order, tuning and illustrated layout remain open.</text>', '</g></svg>']
    destination.write_text("\n".join(svg)+"\n")


def generate():
    job_specs = {**JOBS, **CONFIG["work_first_jobs"]}
    journeys = []
    for name, order in (("A", ORDER), ("B", ALTERNATIVE)):
        for home in ("starter-court", "parkside"):
            for job in ("butcher", "electrician", "doctor"):
                for study, rent in ((False,False),(True,False),(True,True)):
                    stops = itinerary(job, study, rent, False, home=home)
                    for mode in MODES:
                        journeys.append(dict(layout=name, home=home, job=job, study=study, rent=rent,
                                             **route(stops, mode, order)))
    ledgers, summaries = [], []
    # Preserve the cash/stock checkpoint and v1 scheduling policy; only replace
    # the visit allowance with actual ordered route distances/entries.
    for name, order in (("A", ORDER), ("B", ALTERNATIVE)):
        for job in ("butcher", "electrician", "plumber", "doctor", *CONFIG["work_first_ladders"]):
            for variant in ("bus", "buy_bike", "keep_buffer", "bike_buffer"):
                try:
                    rows, summary = compare(job, variant, visit_budget=budget(order, "starter-court"),
                                            career_ladder=CONFIG["work_first_ladders"].get(job),
                                            job_definitions=job_specs,
                                            course_path=[] if job in CONFIG["work_first_ladders"] else PATHS[job])
                except (ValueError, AssertionError) as exc:
                    summaries.append(dict(layout=name, route=job, variant=variant,
                                          status="blocked under unchanged v1 worksheet policy", reason=str(exc)))
                    continue
                ledgers.extend(dict(layout=name, **r) for r in rows)
                summaries.append(dict(layout=name, **summary))
    assert len(ORDER) == len(set(ORDER)) == 15
    for a in ORDER:
        for b in ORDER:
            assert distance(a,b) == distance(b,a)
            assert 0 <= distance(a,b) <= 7
    return journeys, ledgers, summaries


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    journeys, ledgers, summaries = generate()
    outputs = {"journeys.json":journeys, "career-summary.json":summaries}
    if args.check:
        for name, value in outputs.items():
            assert json.loads((OUT/name).read_text()) == value
        with (OUT/"career-ledger.csv").open(newline="") as stream:
            actual=list(csv.DictReader(stream))
        assert actual == [{k:str(v) for k,v in row.items()} for row in ledgers]
        print(f"Checked {len(journeys)} journeys and {len(ledgers)} route-linked budget rows")
        return
    for name, value in outputs.items():
        (OUT/name).write_text(json.dumps(value,indent=2)+"\n")
    with (OUT/"career-ledger.csv").open("w",newline="") as stream:
        writer=csv.DictWriter(stream,fieldnames=list(ledgers[0]),lineterminator="\n")
        writer.writeheader();writer.writerows(ledgers)
    render_map(OUT/"town-map-a.svg")
    render_map(OUT/"town-map-b.svg", ALTERNATIVE, "B")
    print(f"Generated {len(journeys)} journeys, {len(ledgers)} career rows and town-map-a.svg")


if __name__ == "__main__":
    main()
