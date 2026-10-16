# Package trace: computer actions at every destination

Verified 2026-10-16 against website DOS1.000.060. Evidence **BYTECODE** for controller presence, event dispatch and the selected transaction/confirmation branches below. [Metadata](../../artifacts/rules-audit/bytecode-ai-actions-verification.json) records the thirteen destination controllers plus broker, input hashes, method entries and message-write offsets. Original code stays local. No live execution or exhaustive fairness claim.

## The actual bridge to ordinary actions

Actual script255 `Dialog.doit` creates an event at `0x0e1a`, gives it to the attached script's `handleEvent` and `doit` at `0x0e3f`, then passes the **same event** into the dialog's normal `handleEvent` at `0x0e46`. The dialog's control dispatch at `0x1098` searches its controls; the selected path calls that control's `doit` at `0x10eb`. The controller does not need a second inventory/payment implementation merely because it synthesizes a keyboard event.

Every destination's `computerScript` inherits class68 (`DialogScript`). The shared controller supplies work key119 and exit key120, with the eligibility and incidental-work checks already traced in [AI-B01](bytecode-weekly-opponent.md#ai-b01-policy-location-controller-and-shared-action-are-separate-layers). Destination controllers select item/action keys and pass other states to that controller. A successful dispatch still reaches the ordinary action handler's checks/costs; choosing an event is not proof of a successful transaction.

## Destination and child-controller catalogue

Offsets identify `computerScript.handleEvent`; example offsets identify actual message writes or shared-controller calls. The intent descriptions refer to the listed inspected branches, not every strategy predicate.

| Destination | Script / entry | Verified action route and example anchors |
| --- | --- | --- |
| Low-cost home | 200 / `0x0472` | Relax button key→event at `0x04c5`; shared controller at `0x04d8` with work disabled |
| Rent office | 201 / `0x1300` | Pay rent `0x1344`, move `0x13af/0x13f9`, extension `0x1420`, arrears payment `0x1464`; shared work enabled |
| Security home | 202 / `0x0512` | Relax key→event `0x0565`; shared controller `0x0578` with work disabled |
| Market | 203 / `0x0daa` | One/two/four-week grocery keys→events `0x0dfe/0x0e1d/0x0e30`; newspaper `0x0ee9`, tickets `0x0f60`; shared work enabled |
| Bank | 204 / `0x1016` | Deposit `0x105f`, withdraw `0x10b1`, repayment `0x10e0`, broker `0x1110`, loan `0x11b3`; shared work enabled |
| Factory | 205 / `0x0542` | Delegates to common work/exit controller at `0x0568`; no separate computer payroll handler here |
| Employment agency | 206 / `0x0fda` | Candidate scan chooses employer event at `0x10f3` and job key436; raises use current job key; shared work disabled |
| University | 207 / `0x144c` | Enrollment key→event `0x1603`, selected course key→event `0x164c`; shared work enabled |
| Appliance shop | 208 / `0x1098` | Object key→event for ordinary purchases: refrigerator `0x10e8`, stove `0x1109`, later computer `0x12df`; shared work enabled |
| Clothes shop | 209 / `0x09fe` | Chosen uniform key→event at `0x0a7c` or later `0x0af2`; shared work enabled |
| Fast food | 210 / `0x0caa` | Chosen food key→event `0x0d76`; shared work enabled |
| Discount shop | 211 / `0x167e` | Atlas/dictionary/encyclopedia events `0x16e2/0x1739/0x1790`, clothes and entertainment keys; shared work enabled |
| Pawn shop and selectors | 212 / `0x1a00` | Pawn/redeem events `0x1a50/0x1a77`, selected pawn action `0x1ae0`, item selection and confirmation-route event `0x1b68`; work disabled |
| Broker, inside bank | 213 / `0x0f70` | Holding selection, Buy `0x10a6`, Sell `0x11c7/0x12bd`; shared work disabled |

The employer child lists use `JobScript`, class77 in script206, whose state2 writes selected job key436 into the event at `0x06d1`. The ordinary `JobDItem.doit` then controls application time, qualifications, opening chance, rejection memory and raise/hiring effects. This closes the selected agency→employer-list→ordinary-job-action chain; it does not re-prove every candidate-ranking formula.

The broker's direct `doit` call at `0x12d7` invokes the **destination policy script300** to choose what to do next. It is not a direct investment grant or a separate trade settlement. Other broker states select normal buy/sell keys. The policy still reads hidden economic trends, so shared action execution must not be confused with equal information.

## Confirmed presentation shortcuts

| Shared action | Actual computer-specific branch | What remains shared |
| --- | --- | --- |
| Enrollment | Script207 `0x118a–0x119c` tests playing29 and directly calls `enrollmentFee.doit`; human path confirms first and calls it at `0x1225` | Same fee object, affordability/debit and enrollment counter |
| Approved loan | Script204 `0x0a8e–0x0a9b` short-circuits the Yes/No question for playing29 | Ordinary loan qualification, amount, cash/principal and schedule path |
| Pawn offer | Script212 `0x12a8–0x12b5` accepts computer marker29 before the human confirmation | Ordinary item/offer/transaction path; not proof of a higher pawn price |
| Moving apartments | Script201 tests computer marker29 at `0x0bc1–0x0bce` and `0x0e15–0x0e22`, clears the prior rent quantity and skips the forfeiture question | Same selected housing action afterward; no inferred free move or rent discount |

These are genuine original differences in interaction. Bank clerk/animation treatment can differ too, without bypassing the money movement. A 2.0 shared-rules engine can separate policy and confirmations while preserving the action's calculation; exact UI event synthesis is not an approved requirement for the new architecture.

## Verification scope and remaining work

All14 controller method tables were resolved from package objects. Their recovered instruction spans were compared with the raw script bytes. Controller event writes and the shared dialog chain were traced using selectors resolved from vocabulary997; selected computer-marker branches above were checked directly. That establishes the ordinary dispatch architecture and bounded shortcuts.

Not established: every destination-policy arithmetic expression, every fallback or state-restoration path, every controller loop's termination under unusual state, all financing estimates, future-price knowledge or exhaustive absence of privileges. Destination choice, economic information and transaction legality remain separate audit questions. No new gameplay session was needed for these dispatch checks.
