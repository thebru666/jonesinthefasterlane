import { mkdirSync, writeFileSync } from 'node:fs';
import { campaign, openingScenario } from './scenarios.ts';
import { scores } from '../src/simulation/selectors.ts';

const write = process.argv.includes('--write');
const folder = new URL('../artifacts/prototype/headless-v1/', import.meta.url);
if (write) mkdirSync(folder, { recursive: true });
const opening = openingScenario();
const summary = {
  status: 'Executed prototype action traces; deterministic examples, not balance or original-equivalence evidence',
  rules: opening.final.rules,
  opening: { mode: 'neutral-fixture', cash: opening.beforeEnd.cash, timeRemaining: opening.beforeEnd.time,
    experience: opening.beforeEnd.experience, workTime: opening.beforeEnd.workTime,
    outgoingDependability: opening.final.players[0]!.dependability, scores: scores(opening.final.players[0]!) },
  campaigns: ([] as unknown[]),
};
for (const route of ['work-first', 'butcher'] as const) {
  for (const mode of ['neutral-fixture', 'live'] as const) {
    const run = campaign(route, 42, mode);
    const p = run.final.players[0]!;
    if (!run.finished || !run.reachedRole) throw new Error(`${route}/${mode} did not complete the fixture.`);
    summary.campaigns.push({ route, seed: 42, economyMode: mode, finishWeek: run.weeks, job: p.job, cash: p.cash,
      scores: scores(p), qualifications: p.qualifications, requests: run.intents.length });
    if (write) writeFileSync(new URL(`${route}-${mode}.json`, folder), JSON.stringify({ ...run, ledger: undefined }, null, 2) + '\n');
  }
}
if (write) {
  writeFileSync(new URL('opening.json', folder), JSON.stringify(opening, null, 2) + '\n');
  writeFileSync(new URL('summary.json', folder), JSON.stringify(summary, null, 2) + '\n');
}
console.log(JSON.stringify(summary, null, 2));
