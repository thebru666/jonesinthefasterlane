# Employment: application, raises, work and dismissal

Audit date: 2026-10-16. Reference: website DOS **1.000.060**, [bundle source](https://jonesinthefastlane.com/bundle.jsdos). **BYTECODE** below means selected paths checked in the extracted package, rather than an assumption that the published decompilation matches every instruction. No new runtime experiments were performed. No adaptation changes are approved here.

[Verification metadata](../../artifacts/rules-audit/bytecode-employment-verification.json) records resource hashes, ranges and all **37 employer-specific job records**. Their property words were reread directly from raw resources; 1,075 instruction records were matched to their resource bytes, with independent operand and comparison checks. The [human-readable career table](../original-game/content-progression.md#employment-what-the-lists-actually-offer) remains the convenient presentation; the metadata supplies package values and object offsets. This is not whole-program execution proof.

## EMP-001: the player-facing route

The employment agency opens a list of nine employers. Selecting one opens its job list, where selecting an occupation means applying for it or requesting a raise for the occupation already held. The agency is not itself an employer. Obtaining a job does not start a work shift: the player travels to the employer and uses Work there.

Actual agency initialization charges **2 time units** (`206:0x07af–0x07b6`). Every ordinary job object declares **4 application time units**. `JobDItem.doit` checks whether the clock is already 60, charges those four units, then evaluates the application (`206:0x03ee–0x0407`). It does not require four units to remain and does not recheck closure after that charge. At an already exhausted clock it selects the closed response and performs no qualification roll. Time clamping is defined by [the action audit](time-and-actions.md).

An application has this order:

1. Compute education, dependability, experience and opening results, including prior rejection memory.
2. If employer and occupation match the current job, enter the wage/raise branch.
3. Otherwise, a successful combined result replaces the current job; failure preserves it.
4. Display outcome when returning through agency feedback. A rejected new job costs **1 happiness** through Main export13 (`206:0x00e3–0x00e6`). A refused raise does not take that rejection penalty.

Employer-list entry charges beyond the agency/application costs, every possible re-entry route, and work-button visibility in all nine workplaces have not all received package-level caller checks. Do not infer an extra universal browsing fee.

## EMP-002: eligibility and the opening roll

For a job with declared dependability `D`, experience `E`, and up to two qualification IDs, the ordinary qualification result requires all four conditions:

| Test | Exact condition in the selected path |
| --- | --- |
| Education | Every nonzero required qualification ID must be held; two requirements mean both |
| Work history | Player dependability ≥ `D`, except declared `D=10` means threshold **0** |
| Experience | Player experience ≥ `E` |
| Opening/chance | `Random(1,100) ≤ 30 + trunc((dependability + experience + 8 × numDegrees + 10)/3)`, then rejection-memory override |

Package evidence: `206:0x024c–0x034d`; selectors459/460 are `numDegrees`/`hasDegree`, selector440 is the original misspelling `dependibility`, and selector442 is `experience`. Signed integer comparisons and truncating division matter. The score is not explicitly clamped to100. Inclusive random endpoints follow the pinned SCI semantics; this audit did not statistically test the DOS generator.

The shared qualification path has **no direct current-economy comparison and no stored vacancy count**. Its “no openings” result is the random/history gate. Economic conditions affect offered wages separately. Clothing is not a hiring test: a player can obtain a job before acquiring suitable clothes, then fail to work.

**Cook exception:** occupation index44 sets the opening result true **after** applying rejection memory (`206:0x0311–0x031b`). It still checks education/work-history/experience, whose cook requirements are minimal. It still consumes the ordinary random call. This gives a dependable recovery job rather than a universal guarantee for every low-level job.

A fully successful qualification also writes the selected menu key and current computer-search index into player `jobKey`/`jobT` (`206:0x0336–0x0346`). These writes happen during qualification, before the later raise/hiring distinction.

## EMP-003: remembered rejections and feedback

A failure of the opening test **with education, history and experience already sufficient** records that employer-specific `jobNum`. A later attempt during the same turn forces its opening result false even if the new roll succeeds. Other qualification failures do not add that memory. Storage avoids duplicate entries. Evidence: `206:0x034e–0x03b0`, `0x058a–0x05a9`.

The start-turn script resets the rejection count to zero at `111:0x03e9–0x03f4`. Memory therefore belongs to the active-turn processing, not a permanent career penalty. Distinguish `jobNum` (1…37 employer-specific record), `indexNum` (occupation, reused across employers), and `jobT` (computer search index); they are not interchangeable IDs.

Feedback has a misleading early-game detail: before week4 it overwrites the displayed work-history flag to true (`206:0x010e–0x0119`), **after** the failed application. This hides “poor work history” as a stated reason during those weeks; it does not relax the underlying eligibility test. Education failure also sets the player's `notEnoughEd` flag, used by opponent planning. Do not use feedback prose alone as the authoritative eligibility result.

## EMP-004: changing jobs and requesting raises

A successful new-job application (`206:0x04af–0x0587`) performs these changes:

- Reset `raisesGiven` to0; add **2 experience** immediately.
- Set `maxExperience = requiredExperience + 10 + (requiredExperience == 0 ? 10 : 0)`.
- Store current offered wage, job base wage, employer, occupation, declared dependability requirement and uniform requirement.
- Raise player dependability to10 if below10; otherwise preserve it.
- Recalculate career status and award **3 happiness** through Main export13.

A job change can therefore be strategic even between jobs with the same occupation name. There is one current job, not a concurrent collection of employers. Experience is carried between careers; changing jobs replaces the occupation's growth ceiling. The hiring bonus itself is not bounded by that ceiling in this method.

For **same employer and occupation**, the code ignores the combined `qualify` return value after computing it. Consequently the random opening roll, education failure and rejection memory do **not** directly prevent an existing-job raise. Qualification still consumes randomness and can write planning fields. Evidence: `206:0x0401–0x0427`, then `0x042a–0x04ac`.

| Current wage compared with today's offered wage | Result |
| --- | --- |
| Greater | “asking for less”; wage is preserved |
| Equal | “same wage”; wage is preserved |
| Lower, and player dependability ≥ declared job dependability + `5 × raisesGiven` | Wage becomes today's offer; increment raises count; +3 happiness |
| Lower, but below that threshold | Refuse raise; wage is preserved |

The first raise uses the **literal declared dependability**, including10; the special zero eligibility threshold does not apply here. Experience and education are not retested as requirements by this raise branch. There is no automatic wage cut when offered pay falls. `baseWage` is set on hiring but not rewritten by the raise branch.

Offered wages inherit `CostDItem.init` (`104:0x0344–0x0374`), which normally takes goods reading global309 and calls price helper109:0 with base wage. The selected initializer verifies that connection; the helper's full arithmetic remains documented in [economy](economy.md#econ-003-exact-ordinary-price-calculation).

## EMP-005: clothing, attendance and firing

Work entry is script108 export0 (`0x000c–0x014b`). Its checks are ordered:

1. Clock already60: closed; no shift.
2. `dressedForWork` false: refuse work; no shift. This runs **before** the firing check.
3. Dependability **strictly below** `minDepend − 5`: dismiss; set wage/employer/occupation to0 and `jobT` to−1; return−1.
4. Dependability **strictly below** `minDepend − 2` with the turn's warning flag set: show warning, then work normally.
5. Otherwise work normally.

At exactly `minDepend−5` the player is not fired; at exactly `minDepend−2` no warning is required by that comparison. The warning flag starts true (`111:0x03e4–0x03e6`) and is cleared by a successful shift (`108:0x014e–0x0150`). Refused work and dismissal do not reach the shift's six-unit time charge. Other caller/UI costs are separate.

`Player.dressedForWork` (`1:0x0bf4–0x0c6e`) chooses the best available nonzero-quantity clothing, checking business suit34, dress35, then casual36. It accepts that grade when its numeric ID is ≤ required uniform ID. No clothes fails. Owning better clothes satisfies lower requirements; the method does not present a manual outfit-selection choice. Consumption and replacement cadence belong to [weekly processing](weekly-processing.md).

## EMP-006: work progression, income and education integration

A successful shift applies progression **once per Work action**, including a partial final shift (`108:0x014c–0x01c6`):

- If experience < `maxExperience + expCredit`, add1 experience.
- If dependability < `minDepend + 20 + eduCredit`, add1 dependability.

Thus [education](education.md) contributes twice: completed-degree count improves the hiring chance, while `expCredit` and `eduCredit` extend work-growth ceilings. Specific degree prerequisites remain separate. Having more qualifications does not remove every career threshold.

The Player class defaults are experience10, dependability20, and both credits0. The examined `Player.init` does not replace them; setup/save paths have not all been traced to prove every possible start uses unchanged defaults. `Player.endTurn` subtracts **3 dependability**, floored at0 (`1:0x0d9b–0x0dae`). In an ordinary turn, three successful shifts offset that decay; actual goals and ceilings can alter the decision.

Career status is `min(100, 10 × trunc(dependability/8))` when wage is nonzero, otherwise0; hiring, successful work and end-turn update it. This is a stepped score rather than hourly wage or experience.

Payroll starts at eight hourly wages per six-unit shift. A final partial shift prorates by remaining units/6, while progression still occurs first. The successful shift adds its net pay then charges six time units (`108:0x0329–0x0345`). Rent garnishment can overwrite the prorated value with full-shift intermediates: preserve the exact [package-confirmed payroll finding](bytecode-finance-findings.md), not a simplified proportional-pay rule.

## EMP-007: dismissal through economic shocks

`Player.doScandal` (`1:0x0f5c–0x0fb2`) supplies a second dismissal path. For an active player and an existing wage, severity1 always dismisses; severity2 dismisses on zero from `Random(0,1)`, otherwise reduces wage to `max(1,trunc(wage × 8/10))`. The calling event dispatch and player-wide effects are described in [economy](economy.md#econ-006-a-shock-affects-more-than-the-active-player).

Shock dismissal clears wage, employer and occupation but **does not clear `jobT` here**, unlike work-history dismissal. Other career fields also remain stored. That difference is package-confirmed; this pass does not claim it produces a particular visible or AI failure. Severity1 also clears the low bank-balance field. High-word money handling is a separate audit concern.

## Remaining build decisions and verification gaps

No bug correction or new mechanic is approved. Before claiming exact fidelity, resolve:

- Whether to preserve early hidden work-history feedback, random consumption on raise requests, stale planning fields after shock dismissal, and full progression for partial shifts.
- Every employer caller's eligibility/visibility and animation effects; free refused work is established only inside the shared helper.
- Initial-state overrides in setup, loading and opponent creation.
- Extreme signed-word progression/score overflow; the formulas above describe normal reachable values rather than arbitrary unbounded TypeScript numbers.
- Narrow runtime checks of feedback wording, turn-memory reset and exact boundary outcomes, only where bytecode semantics leave presentation or interpreter questions.

These are compatibility choices and focused verification work, not reasons to invent additional job systems for 2.0.
