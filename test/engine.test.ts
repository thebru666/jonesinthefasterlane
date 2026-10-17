import test from 'node:test';
import assert from 'node:assert/strict';
import { createGame, dispatch, quoteTrip } from '../src/simulation/engine.ts';
import { scores } from '../src/simulation/selectors.ts';
import { exportSave, importSave } from '../src/simulation/save.ts';
import type { Action, GameState } from '../src/simulation/types.ts';

function act(s: GameState, action: Action): GameState {
  const result = dispatch(s, { id: s.sequence + 1, action });
  assert.ok(result.accepted, result.message);
  s = result.state;
  while (s.notices.length) s = dispatch(s, { id: s.sequence + 1, action: { type: 'acknowledge' } }).state;
  return s;
}
const fresh = () => createGame({ seed: 42, economyMode: 'neutral-fixture' });

test('fresh unemployed opening executes seven shifts and food, not an employed checkpoint', () => {
  let s = fresh(); const before = structuredClone(s);
  s = act(s, { type: 'travel', destination: 'hospitality', mode: 'walk' });
  s = act(s, { type: 'apply', job: 'cook' });
  for (let i = 0; i < 7; i++) s = act(s, { type: 'work' });
  s = act(s, { type: 'buy', item: 'hamburger' });
  assert.equal(s.players[0]!.cash, 345);
  assert.equal(s.players[0]!.time, 3);
  assert.equal(s.players[0]!.experience, 19);
  assert.equal(s.players[0]!.workTime, 42);
  assert.equal(scores(s.players[0]!).learning, 3);
  assert.deepEqual(before, fresh(), 'reducer must not mutate its input');
  s = act(s, { type: 'endTurn' });
  assert.equal(s.week, 2);
  assert.equal(s.players[0]!.dependability, 24);
  assert.equal(scores(s.players[0]!).career, 30);
  assert.equal(s.players[0]!.place, 'home');
  assert.equal(s.players[0]!.time, 60, 'meal prevents hunger time');
  assert.equal(s.players[0]!.rentStock, 2);
});

test('duplicated or pending input cannot pay twice or consume additional randomness', () => {
  const s = fresh();
  const intent = { id: 1, action: { type: 'travel', destination: 'hospitality', mode: 'bus' } } as const;
  const once = dispatch(s, intent).state;
  const copy = structuredClone(once);
  assert.equal(dispatch(once, intent).state, once);
  assert.equal(dispatch(once, { id: 2, action: { type: 'apply', job: 'cook' } }).state, once);
  assert.deepEqual(once, copy);
  assert.equal(quoteTrip(once, 'hospitality', 'walk').available, false);
});

test('exact arrival exhaustion still permits food, but not work or a new paid trip', () => {
  let s = fresh(); s.players[0]!.time = 11;
  s = act(s, { type: 'travel', destination: 'hospitality', mode: 'walk' });
  assert.equal(s.players[0]!.time, 0);
  s = act(s, { type: 'buy', item: 'hamburger' });
  assert.equal(s.players[0]!.cash, 121);
  const refused = dispatch(s, { id: s.sequence + 1, action: { type: 'apply', job: 'cook' } });
  assert.equal(refused.accepted, false);
  assert.equal(refused.state.rng, s.rng);
  assert.equal(refused.state.players[0]!.time, 0);
});

test('first car trip pays package once; same-site reopening and restored quotes are free', () => {
  let s = fresh(); const p = s.players[0]!; p.owns.car = true; p.cash = 100;
  s = act(s, { type: 'travel', destination: 'market', mode: 'car' });
  assert.equal(s.players[0]!.cash, 76);
  s = act(s, { type: 'travel', destination: 'market', mode: 'car' });
  assert.equal(s.players[0]!.cash, 76);
  s = importSave(exportSave(s));
  assert.equal(quoteTrip(s, 'hospitality', 'car').cash, 4);
  s = act(s, { type: 'travel', destination: 'hospitality', mode: 'car' });
  assert.equal(s.players[0]!.cash, 72);
});

test('partial work credits actual effort and prorates garnishment', () => {
  let s = fresh(); s = act(s, { type: 'travel', destination: 'hospitality', mode: 'walk' });
  s = act(s, { type: 'apply', job: 'cook' });
  const p = s.players[0]!; p.time = 1; p.wage = 10; p.rentDebt = 10;
  const old = p.experience;
  s = act(s, { type: 'work' });
  assert.equal(s.players[0]!.cash, 204);
  assert.equal(s.players[0]!.rentDebt, 4);
  assert.equal(s.players[0]!.workTime, 1);
  assert.equal(s.players[0]!.experience, old);
  assert.equal(s.players[0]!.time, 0);
});

test('a final partial lesson graduates once, and restore/reopen cannot award it again', () => {
  let s = fresh(); s.players[0]!.place = 'college'; s.players[0]!.enrolled = true;
  s.players[0]!.lessons = 9; s.players[0]!.time = 1;
  s = act(s, { type: 'study' });
  const p = s.players[0]!;
  assert.equal(p.lessons, 10); assert.equal(p.time, 0); assert.equal(p.happiness, 5);
  assert.equal(p.dependability, 25); assert.equal(scores(p).learning, 10);
  assert.deepEqual(p.qualifications, ['trade-school']);
  s = importSave(exportSave(s));
  const refused = dispatch(s, { id: s.sequence + 1, action: { type: 'study' } });
  assert.equal(refused.accepted, false);
  assert.equal(refused.state.players[0]!.happiness, 5);
});

test('full trip failure preserves cash/time/car payment and does not draw', () => {
  const s = fresh(); s.players[0]!.owns.car = true; s.players[0]!.cash = 23;
  const result = dispatch(s, { id: 1, action: { type: 'travel', destination: 'market', mode: 'car' } });
  assert.equal(result.accepted, false);
  assert.deepEqual(result.state.players, s.players);
  assert.equal(result.state.rng, s.rng);
});

test('closed rent counter does not close the civic job index', () => {
  let s = fresh(); s = act(s, { type: 'travel', destination: 'civic', mode: 'walk' });
  s = act(s, { type: 'apply', job: 'cook' });
  assert.equal(s.players[0]!.job, 'cook');
  assert.equal(dispatch(s, { id: s.sequence + 1, action: { type: 'payRent' } }).accepted, false);
  assert.equal(dispatch(s, { id: s.sequence + 1, action: { type: 'work' } }).accepted, false);
});

test('progression ceilings extend with work and course learning without free actual growth', () => {
  let s = fresh(); const p = s.players[0]!;
  p.place = 'hospitality'; p.job = 'cook'; p.wage = 4; p.baseWage = 4; p.maxExperience = 20;
  p.experience = 25; p.dependability = 30; p.workTime = 119;
  p.enrolled = true; p.lessons = 10; p.enrolled = false; p.qualifications = ['trade-school'];
  s = act(s, { type: 'work' });
  assert.equal(scores(s.players[0]!).learning, 20);
  assert.equal(s.players[0]!.experience, 26);
  assert.equal(s.players[0]!.dependability, 31);
});

test('goal completion waits until incoming gate, then blocks further work', () => {
  let s = fresh(); const p = s.players[0]!;
  p.place = 'hospitality'; p.job = 'cook'; p.wage = 4; p.baseWage = 4; p.maxExperience = 20;
  p.cash = 999; p.dependability = 30; p.happiness = 20; p.workTime = 120;
  s = act(s, { type: 'work' });
  assert.equal(s.status, 'playing');
  s = act(s, { type: 'endTurn' });
  assert.equal(s.status, 'finished');
  assert.equal(dispatch(s, { id: s.sequence + 1, action: { type: 'work' } }).accepted, false);
});

test('seed zero retains its identity and produces a different stream from seed one', () => {
  const zero = createGame({ seed: 0, economyMode: 'neutral-fixture' });
  const one = createGame({ seed: 1, economyMode: 'neutral-fixture' });
  assert.equal(zero.rng, 0); assert.equal(one.rng, 1);
});


test('funded shop fixture acquires useful possessions through real purchases', () => {
  let s = fresh(); s.players[0]!.cash = 2500;
  s = act(s, { type: 'travel', destination: 'tech', mode: 'bus' });
  for (const item of ['bike', 'car', 'fridge'] as const) s = act(s, { type: 'buy', item });
  assert.deepEqual(s.players[0]!.owns, { bike: true, car: true, fridge: true });
  assert.equal(s.players[0]!.cash, 301);
  assert.equal(s.players[0]!.happiness, 0);
  assert.equal(scores(s.players[0]!).learning, 0);
  s = act(s, { type: 'travel', destination: 'market', mode: 'car' });
  s = act(s, { type: 'buy', item: 'groceries4' });
  s = act(s, { type: 'endTurn' });
  assert.equal(s.players[0]!.groceries, 3);
  assert.equal(s.players[0]!.carPaid, false);
});

test('switching civic and local boards cannot reroll a remembered job rejection', () => {
  let s = fresh(); const p = s.players[0]!; p.place = 'civic'; p.experience = 25; p.dependability = 25;
  const first = dispatch(s, { id: 1, action: { type: 'apply', job: 'supervisor' } });
  assert.equal(first.accepted, false);
  s = first.state;
  while (s.notices.length) s = dispatch(s, { id: s.sequence + 1, action: { type: 'acknowledge' } }).state;
  s = act(s, { type: 'travel', destination: 'hospitality', mode: 'walk' });
  const second = dispatch(s, { id: s.sequence + 1, action: { type: 'apply', job: 'supervisor' } });
  assert.equal(second.accepted, false);
  assert.deepEqual(second.state.players[0]!.rejectionMemory, ['supervisor']);
  assert.equal(second.state.players[0]!.time, 44);
});


test('work cannot turn a supported imported experience boundary into an unsaveable value', () => {
  let s = fresh(); const p = s.players[0]!;
  p.job = 'cook'; p.place = 'hospitality'; p.wage = 4; p.baseWage = 4;
  p.experience = 1_000_000_000; p.maxExperience = 1_000_000_000; p.workTime = 120;
  s = importSave(exportSave(s));
  s = act(s, { type: 'work' });
  assert.equal(s.players[0]!.experience, 1_000_000_000);
  assert.deepEqual(importSave(exportSave(s)), s);
});
