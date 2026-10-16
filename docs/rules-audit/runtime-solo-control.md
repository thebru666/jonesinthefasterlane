# Independent solo no-food control

Session began 2026-10-15 and resumed 2026-10-16 after a usage-limit interruption during setup. **OBSERVED** describes the specific visible actions/states below; this is a partial execution of [RT03](runtime-test-plan.md), with presentation and measurement limits preserved.

Reference URL: <https://jonesinthefastlane.com/>. Separate Chrome extension-controlled tab, 1600 × 786 viewport; the parent's in-app-browser multiplayer session was not touched. The site supplied its js-dos runtime. Exact emulator/browser builds, RNG seed and persistent save bytes were not recorded. The repository's independently identified [source bundle](../../artifacts/discovery/2026-10-15-bundle-inventory.json) is version 1.000.060, SHA-256 `c08f3310f4f9cf47316bc32745507ae065bba7741430f7c3620602f534c46180`; this run did not intercept the browser's response bytes to establish an additional independent byte match. No debugger, edited save, hidden-state inspection or injected input state was used.

## Setup and action trace

1. New website tab → skip opening sequence → Play Game → 1 human → first character. The goal dialog showed Goal Points = 200 and four unchanged midpoint stars; accepted the defaults and clicked No to the Jones challenge. The usage interruption occurred after this last action. On resume, the same tab showed Player 1 on the week-1 town board; no reload or restore was used.
2. Selected the bank directly. No food or other purchase, work, job application, loan or withdrawal occurred anywhere in week 1. Bank cash display showed $200.
3. Clicked Deposit twice: visible cash $200 → $100 → $0. F4 Statistics then explicitly showed Cash $0, Savings $200, Rent Owed $0, Loan Balance $0 and Total Goods $0. Closed Statistics, then the bank's Done control.
4. Selected Low-Cost Housing and entered the resident apartment. Clicked Relax nine times in total (one, then four, then three, then one), checking the clock between groups. The last visible clock was entirely red. Clicked Done to end the turn. This method deliberately changes relaxation and happiness; it is not a neutral way to wait.
5. Week 2 opened with the weekend panel and a clear clock. The anecdote concerned helping older women cross the street to an aerobics class. Cash remained $0; no expense amount was displayed. Clicked Done once.
6. The next stable board frame showed Week #2 and a red clock sector of approximately one third of its circle. No travel, work, relaxation or other time-consuming player action had occurred during week 2. F4 then explicitly confirmed Cash $0, Savings $200, Rent Owed $0, Loan Balance $0 and Total Goods $0. One subsequent Statistics down-arrow click exposed Investment Total $0; it did not alter the test state.

## Result and interpretation

| Claim | Evidence / limit |
| --- | --- |
| Two ordinary deposit clicks transferred the starting $200 into savings | Directly observed cash 200→100→0 plus Statistics savings200/cash0. Supports FIN-001 for these values. |
| This no-food control began week 2 with substantial time already spent | Directly observed clear clock at weekend versus approximately one-third red on the settled board before normal actions. This is consistent with the script's 20-of-60 hunger penalty. The UI captured a graphical clock, not an exact numerical internal counter. |
| Savings were untouched through this transition | Directly observed $200 before and after; carried cash remained0. This supports the absence of an automatic savings debit in this particular transition. |
| A doctor consequence was not evident in the settled state | No extra ten-hour sector or cash/savings loss was visible. This agrees with the zero-cash script gate but does not establish whether the illness random gate opened. One run cannot establish probabilities or prove universal suppression. |
| The hunger notice text and exact −2 happiness executed | **Not directly captured/measured.** Intermediate notices passed between screenshot frames; no immediate before/after happiness reading was taken. Keep those claims SCRIPT-derived. The weekend anecdote is also a source-defined possible happiness event, so a net weekly happiness difference would not isolate hunger. |

Compare the separate [multiplayer food/spoilage observations](runtime-observations.md), preserving their own state and capture limits. This solo run does not test illness odds, alternative food stocks, loan repayment, durable bonuses, edited precision states or save persistence. It does not fully pass every component of the prescribed RT03 variant.

## Local evidence

Original screenshots remain ignored under `work/runtime-validation/2026-10-15-solo-control/`; the folder name reflects session start even though captures03–11 were taken on 2026-10-16. All are 1600 × 786 JPEGs. Chrome captures sometimes show a transient black frame or stale presentation immediately after an input; only stable readable frames support behavioural conclusions. Capture03 is retained as a transient black-frame record and is **not** proof of a game state.

| Capture | SHA-256 |
| --- | --- |
| `01-startup-attempt.jpg` | `e298ece484b741c84ba325effbe71da88f90b094ce0890b02670a40cd9e03352` |
| `02-solo-default-goals.jpg` | `6b0023659e91cd42ec228c72ede703c93e1926fed5b3d6291ad7d83397c3fe4d` |
| `03-resumed-week1.jpg` | `436381e8f18bbea33b19285d080605b2d9e1737dd49dfd86ee08db1bac40f6e6` |
| `04-bank-before-200.jpg` | `c5eff36eaf9f4e6024bd73d498f20b854154c5649e7de2ea2feeb43ac0d8fffa` |
| `05-bank-cash-100.jpg` | `a4dcd348d1ee0dac081a1ec993c7edb553e5c05556a99f72b8a77999d5fcd48e` |
| `06-bank-cash-zero.jpg` | `91eed2e3a0922d63aa36c5af16d2f5b3882740c974e124e6d020c96e495a7888` |
| `07-statistics-cash0-savings200.jpg` | `e5cdff924565586858667836eba0287043823222a6c8cf9fa62b17fc44417bb3` |
| `08-week1-home-clock-full.jpg` | `a3a113bf50959f6b947248100e1a00fb18b1a410067d87540d1bb5b8e8e69e32` |
| `09-week2-weekend-cash0-clock-clear.jpg` | `9e854f8166797ffd0b6dd443fb4efe1b4bd8b746f653838da724726d0dbf0922` |
| `10-after-weekend.jpg` | `a5f9156d14ebd001a3b86ccb7be404b4509421f91cb8298dad5867cfe1058848` |
| `11-week2-statistics-money.jpg` | `3b3da61316531089f5e79f6513b843d935603197a86d81f5895d1d44d9576632` |
