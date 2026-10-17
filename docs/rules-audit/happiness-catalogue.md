# Happiness: modifier catalogue and evidence limits

Consolidated 2026-10-17 for website DOS **1.000.060**. This joins all **76 identified literal calls** to the common Happiness helper:47 action sites and29 event sites. It is a bounded actual-package catalogue, not a claim that arbitrary computed/native/restored mutations are impossible. Amounts and predicates were read from the selected instructions; no new score observations were made.

The [action catalogue](happiness-actions.md) gives repeatability, flags and all18 nominal durable branches. The [event catalogue](happiness-events.md) gives weekly ordering, recipients, conditions and all29 addresses. [Whole-package inventory](../../artifacts/rules-audit/happiness-inventory.json) identifies69 raw resources,53,740 checked instruction spans, all76 sites, literal score-access candidates and coverage of the two domain manifests.

## State and update contract

- Allocated players, including optional Jones, start with stored Happiness0. The class and four instance defaults agree; see [fresh state](initial-player-state.md).
- Main export13, `0:0x05ea–0x062b`, chooses active player302 unless supplied an explicit second argument. It adds the attempted amount and clamps that call to0…100, then writes the selected player's score at `0x0629`.
- Separate calls clamp separately. A double initial-loan rejection is two−1 calls, not an unrestricted−2 subtraction from an unbounded score.
- Happiness persists across turns. Early preparation clears action latches, not the score itself.
- Its stored value feeds the four-goal completion gates. Stove/microwave ownership can add1 before those gates; the later weekend, lottery and recurring consequences occur after them.

## Consolidated modifier map

Values are attempted changes subject to the helper's clamp. This table groups related sites; it does not replace the exact domain conditions.

| Group | Modifier and normal condition | Detail |
| --- | --- | --- |
| Home rest | +2 first eligible rest per active turn, shared across homes | [Action latches](happiness-actions.md#shared-active-turn-latches) |
| Groceries | +1/+2/+4 for the first successful one/two/four-week purchase in a shared category | Same reference; order matters |
| Enhanced meal / drinks | Cheeseburger+1 or Chicken+2 once; Cola+1 or Shake+2 once | [Fast-food bonuses](fast-food-bonuses.md) |
| Ticket purchases | Baseball/theatre/concert+2 each once; lottery tickets+2 once per active turn | Action latches |
| QT clothing | Suit+2, dress+1 on every successful purchase; casual/Z-Mart clothes no extra reward | [Clothing](clothing-lifecycle.md) |
| Employment | New hire+3; granted raise+3; refused new-job feedback−1 | [Employment](employment.md) |
| Graduation | +5; ordinary lesson/enrollment has no direct modifier | [Education](education.md) |
| Borrowing | Accepted loan/extension+5; refused extension−1; refused initial loan two−1 calls | [Finance](goods-and-finance.md#fin-002-loan-qualification-and-extension) |
| Rent extension | First approval+1 or first refusal−1; repeats do not repeat that call | [Rent lifecycle](finance-lifecycle.md#fl-002-extension-approval-and-arrears-form-a-flag-based-lifecycle) |
| Joke goods | Dog food−1, eight-track−1, Truman Capote−2 on each successful purchase | [Action penalties](happiness-actions.md#refusals-joke-products-and-pawning) |
| Pawn | Accepted pawn−1; pawning fridge with a grocery record adds another−1 | Same reference |
| Durable purchase nominal branches | All18 identified shop overrides skip their nominal bonus with ordinary positive post-receipt quantities | [Complete branch table](happiness-actions.md#all18-nominal-durable-purchase-branches) |
| Ownership | +1 for stove OR microwave, once per incoming preparation; eligible computer-income event+3 | [Current-player weekly calls](happiness-events.md#current-player-weekly-calls) |
| Lottery result | Winning jackpot+10; other winning prizes+5 | Same reference; strict quantity/draw thresholds apply |
| Weekend | Generic fallback outcome58…60 gives Random(2,4); ticket/possession paths do not automatically receive it | [Weekend branch](happiness-events.md#weekend-bonus-and-repeated-draws) |
| Theft / mugging | Eligible home theft−4 once; market OR bank mugging−3 on location return | Event catalogue |
| Food / illness / repair | No food−2; groceries spoiled−2 or excess-stock cap−1; illness−4; selected repair−1 | Event catalogue; distinct predicates/order |
| Overdue loan | −1 at fourth-week notice when debt remains and paySched<0 | Event catalogue |
| Economic mood | Severity1/2/3:−3/−2/−1 to active player, with investor extra−5/−2/−1; eligible investor boom+5 | Event catalogue |
| Crash job consequence | Job loss−7 or pay cut−3 to each eligible affected participant, explicitly targeted | [Recipient sweep](happiness-events.md#crash-job-consequences-explicitly-target-every-eligible-participant) |

Ordinary cash income, a purchase price, animation, possession name or flavour anecdote does not imply a Happiness change. The action/event notes identify inspected paths with no additional score calls. In particular the legitimate recurring appliance effects must not be removed because the purchase bonuses are skipped.

## What the coverage check proves

After [rebuilding local scripts](../discovery/decompile-original-scripts.md), run:

```sh
python3 tools/research/check_happiness_inventory.py --check
```

The original inventory tool checks every decoded instruction span against its hash-identified raw script. It enumerates literal Main export13 calls, finds eight literal hapStat selector loads, and finds no direct mutations of property24 in known Player methods. The only identified literal setter candidate is Main export13; the other literal candidates read the score. Five zero defaults describe initialization rather than executable setters. Each of the76 helper sites appears exactly once in the action/event manifest partition, and the checker detects missing or duplicated membership.

Those checks establish package identity, instruction correspondence and inventory coverage. They do **not** execute branch predicates, infer receiver identity from any arbitrary numeric literal, or prove absence of computed selector/callee forms, native memory writes, save restoration, aliasing or other editions. Manual semantic review supplies amounts/gates and the selected setter target. All eight explicit-recipient calls in the catalogue belong to the cross-player crash sweep; action calls otherwise use the active-player default.

## Planning use

This is now a single reference for which actions and events change the original score, how repeatability differs and where an apparent bonus is only nominal. Designing new rewards, making all item bonuses work, resetting scores on handover or simplifying latches would be explicit changes. The original-first iteration should record those decisions before implementation. No new rule or fix is approved by this catalogue.
