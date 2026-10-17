import test from 'node:test';
import assert from 'node:assert/strict';
import { campaign, driver } from '../scripts/scenarios.ts';
import { createGame, dispatch } from '../src/simulation/engine.ts';
import { exportSave, importSave } from '../src/simulation/save.ts';
import { reachedGoals } from '../src/simulation/selectors.ts';

for (const route of ['work-first', 'butcher'] as const) {
  test(`seeded fresh ${route} campaign reaches its role and all goals, and replays exactly`, () => {
    const run = campaign(route);
    assert.equal(run.options.economyMode, 'live');
    assert.equal(run.finished, true);
    assert.equal(run.reachedRole, true);
    const p = run.final.players[0]!;
    assert.equal(reachedGoals(p), true);
    assert.deepEqual(p.qualifications, route === 'work-first' ? [] : ['trade-school']);
    assert.equal(p.job, route === 'work-first' ? 'manager' : 'butcher');
    let replay = createGame(run.options);
    for (const intent of run.intents) {
      replay = dispatch(replay, intent).state;
      if (replay.notices.length === 0) replay = importSave(exportSave(replay));
    }
    assert.deepEqual(replay, run.final);
  });
}

test('both reduced-service clothing deadlocks recover through legal travel, hiring and paid work', () => {
  for (const cash of [0, 1]) {
    const initial = createGame({ seed: 42, economyMode: 'neutral-fixture' });
    const p = initial.players[0]!;
    p.cash = cash; p.clothes.casual = 0; p.owns.fridge = cash === 0;
    const d = driver(initial);
    d.send({ type: 'endTurn' });
    assert.equal(d.state.players[0]!.recoveryChecks, 1);
    d.send({ type: 'endTurn' });
    assert.equal(d.state.players[0]!.clothes.casual, 1);
    assert.ok(d.send({ type: 'travel', destination: 'hospitality', mode: 'walk' }));
    assert.ok(d.send({ type: 'apply', job: 'cook' }));
    assert.ok(d.send({ type: 'work' }));
    assert.equal(d.state.players[0]!.workTime, 6);
    assert.ok(d.state.players[0]!.cash >= 32);
    while (d.state.players[0]!.time > 0) assert.ok(d.send({ type: 'work' }));
    assert.ok(d.send({ type: 'endTurn' }));
    assert.ok(d.send({ type: 'travel', destination: 'clothes', mode: 'bus' }));
    assert.ok(d.send({ type: 'buy', item: 'casual' }));
    assert.equal(d.state.players[0]!.clothes.casual, 11, 'paid replacement follows temporary aid');
  }
});
