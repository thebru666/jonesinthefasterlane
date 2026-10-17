import test from 'node:test';
import assert from 'node:assert/strict';
import { endTurn, prepareTurn } from '../src/simulation/turns.ts';
import { scores } from '../src/simulation/selectors.ts';
import type { Economy, GameState, Player } from '../src/simulation/types.ts';

function player(id = 'p1'): Player {
  return {
    id, name: id, cash: 200, place: 'market', time: 4,
    job: null, wage: 0, baseWage: 0, raises: 0,
    experience: 10, maxExperience: 10, dependability: 20,
    relaxation: 25, happiness: 50, workTime: 0,
    qualifications: [], enrolled: false, lessons: 0,
    clothes: { casual: 6, dress: 0, suit: 0 }, groceries: 0, meal: false,
    owns: { bike: false, car: false, fridge: false },
    rentStock: 3, rentContract: 325, rentDebt: 0,
    extensionHistory: 0, extensionAttempt: 0, rentOpen: false, rentAccounted: false,
    recoveryChecks: 0, rejectionMemory: ['counter'], warned: false,
    rested: true, groceryBonus: true, mealBonus: true, carPaid: true,
    goals: { wealth: 100, happiness: 100, career: 100, learning: 100 }, finished: false,
  };
}
function fixture(week = 2, players: Player[] = [player()]): GameState {
  const layer = () => ({ trend: 0, reading: 100, risk: 0 });
  const economy: Economy = {
    main: layer(), investments: layer(), goods: layer(), gold: layer(),
    silver: layer(), pork: layer(), blue: layer(), penny: layer(),
  };
  return {
    schema: 1, rules: 'prototype-0.1', content: 'town-0.1',
    rng: 1, sequence: 0, week, active: 0, players, economy,
    shock: 'none', economyMode: 'neutral-fixture', notices: [], status: 'playing',
  };
}

test('first week resets turn context and latches without recurring consumption', () => {
  const s = fixture(1);
  const p = s.players[0]!;
  p.groceries = 4;
  p.meal = true;
  p.recoveryChecks = 1;
  prepareTurn(s);
  assert.equal(p.place, 'home');
  assert.equal(p.time, 60);
  assert.equal(p.relaxation, 25);
  assert.equal(p.groceries, 4);
  assert.equal(p.meal, true);
  assert.equal(p.rentStock, 3);
  assert.equal(p.clothes.casual, 6);
  assert.equal(p.recoveryChecks, 1);
  assert.equal(p.rested || p.groceryBonus || p.mealBonus || p.carPaid, false);
  assert.equal(p.warned, true);
  assert.deepEqual(p.rejectionMemory, []);
  assert.equal(s.rng, 1);
  assert.deepEqual(s.notices, []);
});

test('incoming goal gate runs before hunger, clothing and rent consequences', () => {
  const s = fixture(4);
  const p = s.players[0]!;
  p.goals = { wealth: 0, happiness: 0, career: 0, learning: 0 };
  p.clothes.casual = 1;
  p.rentStock = 1;
  prepareTurn(s);
  assert.equal(p.finished, true);
  assert.equal(s.status, 'finished');
  assert.equal(p.time, 60);
  assert.equal(p.cash, 200);
  assert.equal(p.clothes.casual, 1);
  assert.equal(p.rentStock, 1);
  assert.equal(s.rng, 1);
  assert.equal(s.notices.length, 1);
  const snapshot = structuredClone(s);
  endTurn(s);
  prepareTurn(s);
  assert.deepEqual(s, snapshot);
});

test('no food costs twenty time; cash zero suppresses doctor billing', () => {
  const s = fixture();
  const p = s.players[0]!;
  p.cash = 0;
  prepareTurn(s);
  assert.equal(p.time, 40);
  assert.equal(p.happiness, 48);
  assert.equal(p.cash, 0);
  assert.equal(s.notices.filter(n => n.includes('hungry')).length, 1);
  assert.equal(s.notices.some(n => n.includes('doctor')), false);
});

test('sole spoiled groceries use sentinel and avoid the separate hunger penalty', () => {
  const s = fixture();
  const p = s.players[0]!;
  p.cash = 0;
  p.groceries = 4;
  prepareTurn(s);
  assert.equal(p.groceries, 0);
  assert.equal(p.time, 60);
  assert.equal(p.happiness, 48);
  assert.equal(s.notices.some(n => n.includes('spoiled')), true);
  assert.equal(s.notices.some(n => n.includes('hungry')), false);
});

test('meal coverage survives expiry and overrides spoiled-grocery illness marker', () => {
  const s = fixture();
  const p = s.players[0]!;
  p.meal = true;
  p.groceries = 1;
  prepareTurn(s);
  assert.equal(p.meal, false);
  assert.equal(p.groceries, 0);
  assert.equal(p.time, 60);
  assert.equal(p.cash, 200);
  assert.equal(p.happiness, 48);
  assert.equal(s.rng, 1);
});

test('fridge caps before decrement; all wardrobe grades decay together', () => {
  const s = fixture();
  const p = s.players[0]!;
  p.owns.fridge = true;
  p.groceries = 7;
  p.clothes = { casual: 10, dress: 3, suit: 2 };
  prepareTurn(s);
  assert.equal(p.groceries, 5);
  assert.equal(p.happiness, 49);
  assert.deepEqual(p.clothes, { casual: 9, dress: 2, suit: 1 });
  assert.equal(s.notices.some(n => n.includes('clothing left')), false);
  assert.equal(p.time, 60);
});

test('due-week notice follows decrement and reopens rent accounting only when unpaid', () => {
  const s = fixture(4);
  const p = s.players[0]!;
  p.meal = true;
  p.rentStock = 1;
  p.rentAccounted = true;
  prepareTurn(s);
  assert.equal(p.rentStock, 0);
  assert.equal(p.rentAccounted, false);
  assert.equal(s.notices.some(n => n.includes('rent is due')), true);
  const prepaid = fixture(4);
  prepaid.players[0]!.meal = true;
  prepaid.players[0]!.rentStock = 5;
  prepaid.players[0]!.rentAccounted = true;
  prepareTurn(prepaid);
  assert.equal(prepaid.players[0]!.rentAccounted, true);
  assert.equal(prepaid.notices.some(n => n.includes('rent is due')), false);
});

test('outgoing fourth-week debt adds the new obligation once, unlike other weeks', () => {
  const s = fixture(4);
  const p = s.players[0]!;
  p.cash = 0;
  p.rentStock = 0;
  p.rentDebt = 20;
  endTurn(s);
  assert.equal(p.rentDebt, 345);
  assert.equal(p.rentAccounted, true);
  endTurn(s);
  assert.equal(p.rentDebt, 345);
  assert.equal(s.week, 6);
  const midCycle = fixture(5);
  midCycle.players[0]!.rentStock = 0;
  midCycle.players[0]!.rentDebt = 20;
  endTurn(midCycle);
  assert.equal(midCycle.players[0]!.rentDebt, 20);
});

test('successful extension postpones arrears and carries rent-counter access', () => {
  const s = fixture(4);
  const p = s.players[0]!;
  p.rentStock = 0;
  p.extensionAttempt = 1;
  endTurn(s);
  assert.equal(p.rentDebt, 0);
  assert.equal(p.rentOpen, true);
  assert.equal(p.extensionAttempt, 0);
  endTurn(s);
  assert.equal(p.rentDebt, 325);
  assert.equal(p.rentOpen, false);
});

test('outgoing dependability decay changes the next incoming career gate', () => {
  const s = fixture();
  const p = s.players[0]!;
  p.job = 'counter';
  p.wage = 5;
  p.dependability = 26;
  p.goals = { wealth: 0, happiness: 0, career: 30, learning: 0 };
  endTurn(s);
  assert.equal(p.dependability, 23);
  assert.equal(scores(p).career, 20);
  assert.equal(p.finished, false);
  p.dependability = 27;
  endTurn(s);
  assert.equal(p.dependability, 24);
  assert.equal(p.finished, true);
  assert.equal(s.status, 'finished');
});

test('C20 recovers both cash-one and cash-zero-with-fridge deadlocks exactly once', () => {
  for (const [cash, fridge] of [[1, false], [0, true]] as const) {
    const s = fixture();
    const p = s.players[0]!;
    p.cash = cash;
    p.owns.fridge = fridge;
    p.clothes.casual = 0;
    prepareTurn(s);
    assert.equal(p.clothes.casual, 0);
    assert.equal(p.recoveryChecks, 1);
    endTurn(s);
    assert.equal(p.clothes.casual, 1);
    assert.equal(p.recoveryChecks, 0);
    assert.equal(s.notices.filter(n => n.includes('temporary casual clothing')).length, 1);
    assert.equal(p.workTime, 0);
  }
});

test('C20 nonqualifying checks reset the consecutive eligibility counter', () => {
  const s = fixture();
  const p = s.players[0]!;
  p.recoveryChecks = 1;
  p.cash = 73;
  p.clothes.casual = 0;
  p.meal = true;
  prepareTurn(s);
  assert.equal(p.recoveryChecks, 0);
  assert.equal(p.clothes.casual, 0);
  p.cash = 0;
  endTurn(s);
  assert.equal(p.recoveryChecks, 1);
  assert.equal(p.clothes.casual, 0);
});

test('rotation separates actors, increments week on wrap and skips finished actors', () => {
  const first = player('first');
  const second = player('second');
  const s = fixture(2, [first, second]);
  first.cash = second.cash = 0;
  endTurn(s);
  assert.equal(s.active, 1);
  assert.equal(s.week, 2);
  assert.equal(first.dependability, 17);
  assert.equal(second.dependability, 20);
  assert.equal(first.clothes.casual, 6);
  assert.equal(second.clothes.casual, 5);
  second.finished = true;
  endTurn(s);
  assert.equal(s.active, 0);
  assert.equal(s.week, 3);
  assert.equal(second.dependability, 20);
  assert.equal(first.clothes.casual, 5);
});

test('seeded doctor bills respect the cash floor and the 499/500 ceiling boundary', () => {
  for (const [cash, bill] of [[1, 1], [30, 30], [31, 31], [499, 48], [500, 162]]) {
    const s = fixture();
    const p = s.players[0]!;
    p.cash = cash!;
    // Seed 1 opens the no-food gate; the next draw supplies the known bill.
    prepareTurn(s);
    assert.equal(p.cash, cash! - bill!);
    assert.equal(p.time, 30);
    assert.equal(p.happiness, 44);
    assert.equal(s.notices.filter(n => n.includes('doctor')).length, 1);
  }
});

test('minimum relaxation can cause illness even when food coverage is good', () => {
  const s = fixture();
  const p = s.players[0]!;
  s.rng = 7132;
  p.relaxation = 11;
  p.meal = true;
  prepareTurn(s);
  assert.equal(p.relaxation, 10);
  assert.equal(p.time, 50);
  assert.equal(p.happiness, 46);
  assert.equal(s.notices.some(n => n.includes('doctor')), true);
  const aboveFloor = fixture();
  aboveFloor.rng = 7132;
  aboveFloor.players[0]!.relaxation = 12;
  aboveFloor.players[0]!.meal = true;
  prepareTurn(aboveFloor);
  assert.equal(aboveFloor.players[0]!.time, 60);
  assert.equal(aboveFloor.rng, 7132);
});

test('one severity-one shock dismisses every unfinished employee, then clears', () => {
  const actors = ['a', 'b', 'finished'].map(id => {
    const p = player(id);
    p.job = 'counter';
    p.wage = 5;
    p.meal = true;
    return p;
  });
  actors[2]!.finished = true;
  const s = fixture(4, actors);
  s.economyMode = 'live';
  s.rng = 1; // With three participants this selects severity one.
  prepareTurn(s);
  assert.deepEqual(actors.map(p => p.job), [null, null, 'counter']);
  assert.deepEqual(actors.map(p => p.wage), [0, 0, 5]);
  assert.deepEqual(actors.map(p => p.happiness), [40, 43, 50]);
  assert.equal(s.notices.filter(n => n.includes('lost their job')).length, 2);
  assert.equal(s.shock, 'none');
});

test('severity-two shock independently cuts or removes each unfinished job', () => {
  const actors = ['a', 'b', 'finished'].map(id => {
    const p = player(id);
    p.job = 'counter';
    p.wage = 5;
    p.meal = true;
    return p;
  });
  actors[2]!.finished = true;
  const s = fixture(4, actors);
  s.economyMode = 'live';
  s.rng = 306;
  prepareTurn(s);
  assert.deepEqual(actors.slice(0, 2).map(p => p.wage).sort(), [0, 4]);
  assert.equal(actors[2]!.wage, 5);
  assert.equal(actors[2]!.happiness, 50);
  assert.equal(s.notices.filter(n => n.includes('lost their job')).length, 1);
  assert.equal(s.notices.filter(n => n.includes('wage was cut')).length, 1);
  assert.equal(s.shock, 'none');
});

test('finishing the first actor advances week at the new first eligible actor', () => {
  const first = player('finished');
  first.finished = true;
  const second = player('second');
  second.cash = 0;
  const s = fixture(2, [first, second]);
  endTurn(s);
  assert.equal(s.active, 1);
  assert.equal(s.week, 3);
  assert.equal(first.dependability, 20);
  assert.equal(second.dependability, 20);
  endTurn(s);
  assert.equal(s.active, 1);
  assert.equal(s.week, 4);
  assert.equal(second.dependability, 17);
});

test('turn and arrears limits refuse before any outgoing mutation', () => {
  const debt = fixture(4);
  debt.players[0]!.rentStock = 0;
  debt.players[0]!.rentDebt = 1_000_000_000;
  const beforeDebt = structuredClone(debt);
  assert.throws(() => endTurn(debt), RangeError);
  assert.deepEqual(debt, beforeDebt);
  const week = fixture(1_000_000_000);
  const beforeWeek = structuredClone(week);
  assert.throws(() => endTurn(week), RangeError);
  assert.deepEqual(week, beforeWeek);
});
