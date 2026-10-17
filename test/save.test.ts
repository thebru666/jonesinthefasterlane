import { test } from 'node:test';
import assert from 'node:assert/strict';
import { createGame, dispatch } from '../src/simulation/engine.ts';
import { exportSave, importSave } from '../src/simulation/save.ts';
import type { GameState } from '../src/simulation/types.ts';

const fixture = (): GameState => createGame({ seed: 42, names: ['Maya'], economyMode: 'neutral-fixture' });
function corrupt(mutate: (state: any) => void): string {
  const state = fixture();
  mutate(state);
  return JSON.stringify(state);
}

test('stable save round-trips every field and is deterministic without sharing state', () => {
  const state = fixture();
  const encoded = exportSave(state);
  const restored = importSave(encoded);
  assert.deepEqual(restored, state);
  assert.equal(exportSave(restored), encoded);
  restored.players[0]!.cash = 123;
  assert.notEqual(restored.players[0]!.cash, state.players[0]!.cash);
});

test('restored next transition preserves sequence and random outcomes', () => {
  const state = createGame({ seed: 983, names: ['Maya'] });
  // Incoming preparation notices are acknowledged before a stable checkpoint.
  let stable = state;
  while (stable.notices.length) stable = dispatch(stable, { id: stable.sequence + 1, action: { type: 'acknowledge' } }).state;
  const restored = importSave(exportSave(stable));
  const intent = { id: stable.sequence + 1, action: { type: 'endTurn' as const } };
  assert.deepEqual(dispatch(restored, intent), dispatch(stable, intent));
});

test('pending feedback cannot be exported or smuggled into an imported save', () => {
  const state = fixture();
  state.notices.push('Salary already resolved');
  assert.throws(() => exportSave(state), /stable save boundary/);
  assert.throws(() => importSave(JSON.stringify(state)), /stable save boundary/);
});

test('save rejects malformed JSON, oversize documents and unsupported versions', () => {
  for (const encoded of ['{', 'null', '[]', '"hello"', ' '.repeat(1_048_577)]) assert.throws(() => importSave(encoded), /Invalid save/);
  for (const [field, value] of [['schema', 2], ['rules', 'future'], ['content', 'other-town']] as const) {
    assert.throws(() => importSave(corrupt(s => { s[field] = value; })), /unsupported/);
  }
});

test('save rejects unknown fields, actions, item IDs and malformed nested objects', () => {
  const mutations: Array<(s: any) => void> = [
    s => { s.action = { type: 'work' }; },
    s => { delete s.rng; },
    s => { s.players[0].job = 'doctor'; },
    s => { s.players[0].place = 'park'; },
    s => { s.players[0].owns.telephone = true; },
    s => { s.players[0].clothes = null; },
    s => { s.economy.gold = []; },
    s => { s.players[0].meal = 1; },
    s => { s.players[0].goals.learning = 15; },
    s => { s.players[0].name = '\u0000'; },
  ];
  for (const mutation of mutations) assert.throws(() => importSave(corrupt(mutation)), /Invalid save/);
});

test('numeric and player bounds reject corrupt or unsafe quantities', () => {
  const mutations: Array<(s: any) => void> = [
    s => { s.players = []; },
    s => { s.players = Array(5).fill(s.players[0]); },
    s => { s.players.push(structuredClone(s.players[0])); },
    s => { s.active = 1; },
    s => { s.week = 0; },
    s => { s.rng = 0x100000000; },
    s => { s.sequence = -1; },
    s => { s.players[0].cash = Number.MAX_SAFE_INTEGER; },
    s => { s.players[0].cash = -1; },
    s => { s.players[0].workTime = 1.5; },
    s => { s.players[0].time = 61; },
    s => { s.players[0].happiness = 101; },
    s => { s.players[0].relaxation = 0; },
    s => { s.players[0].extensionHistory = -2; },
    s => { s.economy.main.reading = 191; },
    s => { s.economy.main.risk = 2; },
  ];
  for (const mutation of mutations) assert.throws(() => importSave(corrupt(mutation)), /Invalid save/);
});

test('qualification IDs and lessons are unique and coherent, with no graduation replay', () => {
  for (const mutation of [
    (s: any) => { s.players[0].qualifications = ['trade-school', 'trade-school']; },
    (s: any) => { s.players[0].qualifications = ['medicine']; },
    (s: any) => { s.players[0].lessons = 10; },
    (s: any) => { s.players[0].lessons = 2; },
    (s: any) => { s.players[0].qualifications = ['trade-school']; s.players[0].lessons = 10; s.players[0].enrolled = true; },
    (s: any) => { s.players[0].rejectionMemory = ['cook', 'cook']; },
  ]) assert.throws(() => importSave(corrupt(mutation)), /Invalid save/);
  const state = fixture();
  state.players[0]!.qualifications = ['trade-school'];
  state.players[0]!.lessons = 10;
  const restored = importSave(exportSave(state));
  assert.deepEqual(restored, state);
});

test('signed extension history and zero LCG state remain representable', () => {
  const state = fixture();
  state.rng = 0;
  state.players[0]!.extensionHistory = -1;
  assert.deepEqual(importSave(exportSave(state)), state);
});

test('finish status must agree with completed-player flags', () => {
  assert.throws(() => importSave(corrupt(s => { s.status = 'finished'; })), /finished players/);
  assert.throws(() => importSave(corrupt(s => { s.players[0].finished = true; })), /unfinished player/);
  const state = fixture();
  state.status = 'finished';
  state.players[0]!.finished = true;
  assert.deepEqual(importSave(exportSave(state)), state);
});

test('actual graduation exports as a stable completed qualification', () => {
  let state = fixture();
  state.players[0]!.cash = 1000;
  state.players[0]!.place = 'college';
  const run = (action: { type: 'enroll' | 'study' }): void => {
    const result = dispatch(state, { id: state.sequence + 1, action });
    assert.equal(result.accepted, true, result.message);
    state = result.state;
    while (state.notices.length) state = dispatch(state, { id: state.sequence + 1, action: { type: 'acknowledge' } }).state;
  };
  run({ type: 'enroll' });
  for (let lesson = 0; lesson < 10; lesson++) run({ type: 'study' });
  assert.deepEqual(state.players[0]!.qualifications, ['trade-school']);
  assert.deepEqual(importSave(exportSave(state)), state);
});

test('a completed participant can be saved while awaiting shared-device handover', () => {
  const state = createGame({ seed: 1, names: ['Maya', 'Alex'], economyMode: 'neutral-fixture' });
  state.players[0]!.finished = true;
  assert.deepEqual(importSave(exportSave(state)), state);
});
