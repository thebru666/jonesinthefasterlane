# Project brief

Recorded: 2026-10-15. Source: initial planning conversation with the project owner.

## Intent

Rebuild the appeal of *Jones in the Fast Lane* as a modern browser game. Remain nearly identical in core mechanics, while updating jobs, buildings, university courses, other opportunities, and visual artifacts. Potential public release; currently a personal project with the owner's children helping iterate.

## Audience and setting

- The owner's children are 8 and 11, but are one audience rather than the entire target market.
- Retain enough depth and humour for adults and fans of the original.
- Small US-style town, with a little Australian flavour that is not overdone.
- Accessible language and clear feedback should help children understand decisions and consequences.

## Essential qualities

1. Economic humps: good and bad periods that affect strategy. Exact original behaviour still needs investigation.
2. Humour: memorable characters, everyday absurdity, and kitsch.
3. Simplicity: meaningful tradeoffs without excessive systems, meters, or management.
4. Near-original gameplay: content modernisation should precede mechanical expansion.

## Play modes

Plan for both shared-device multiplayer and a computer-controlled opponent from the beginning. Player counts, mixed human/computer configurations, opponent difficulty, and detailed handover behaviour are not yet specified.

## Visual direction

Preserve the feel of the existing art. Modern illustrated retro is a promising direction, but no visual style has been approved through mockups yet. Candidate elements include a compact town board, distinct storefronts, expressive location characters, bold panels, and visible possessions. These are proposals rather than final asset requirements.

Create original assets and writing for the new game. A final public-facing name and release/licensing decisions remain open.

## Technical direction

The owner supports the proposed React/TypeScript rendering approach. Initial direction:

- React + TypeScript + Vite frontend.
- Plain TypeScript simulation separate from TSX presentation.
- Data-driven content and balance values.
- Reproducible seeded randomness.
- Local saves and eventual save export/import.
- No application backend initially; consider a leaderboard later.

Detailed architecture and storage choices still require a specification. A shared leaderboard would require a service, and trustworthy competitive scores would require validation beyond accepting client totals.

## Planning before implementation

The owner explicitly wants substantial planning before building. A first playable slice is acceptable once the design is sufficiently specified. Candidate slice: get a job, buy food, pay rent, study toward a better job, and complete a week.

Subsequent direction: document how the original game was organised before redesigning its screens or flow. Use the [original-game baseline](../original-game/README.md) as the reference to refine; keep modernisation suggestions in the separate [follow-up brief](follow-up-original-first-iteration.md).

The earlier suggestion of four goals, one rival, and a 30–45 minute short-game mode is still a proposal. Session length and the complete first-release scope have not been agreed.

## Repository workflow

Use `https://github.com/thebru666/jonesinthefasterlane` for documentation, discovery artifacts, the rules audit, and later implementation. Commit and push each completed step.
