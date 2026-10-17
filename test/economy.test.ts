import test from 'node:test';
import assert from 'node:assert/strict';
import type { GameState, Player } from '../src/simulation/types.ts';
import { createEconomy, price, updateEconomy, updateLayer } from '../src/simulation/economy.ts';
import { random } from '../src/simulation/rng.ts';

// Economy tests never access player fields, only participant count.
function fixture(seed = 1): GameState {
  return {
    schema: 1, rules: 'prototype-0.1', content: 'town-0.1', rng: seed,
    sequence: 0, week: 1, active: 0, players: [{} as Player],
    economy: createEconomy(), shock: 'none', economyMode: 'live',
    notices: [], status: 'playing',
  };
}
function draws(values: number[], expected: number[][]): (low: number, high: number) => number {
  let index = 0;
  return (low, high) => {
    assert.deepEqual([low, high], expected[index]);
    const value = values[index++];
    assert.ok(value !== undefined, 'unexpected additional random draw');
    assert.ok(value >= low && value <= high, 'fixed draw lies within inclusive bounds');
    return value;
  };
}

test('ordinary price examples retain split arithmetic and factor floor', () => {
  for (const [reading, fifty, rent] of [[10,25,162], [70,25,162], [100,50,325], [130,75,487], [190,125,812]] as const) {
    assert.equal(price(50, reading), fifty);
    assert.equal(price(325, reading), rent);
  }
  assert.equal(price(11, 101), 11); // factor101: the two separately truncated pieces.
  assert.equal(price(19, 108), 20); // factor113 would yield21 after one final truncation.
  assert.equal(price(0, 100), 1);
  assert.throws(() => price(Number.MAX_SAFE_INTEGER, 190), RangeError);
  assert.throws(() => price(-1, 100), RangeError);
  assert.throws(() => price(50, 100.5), RangeError);
  const safeBase = Math.floor(Number.MAX_SAFE_INTEGER / 250);
  assert.ok(Number.isSafeInteger(price(safeBase, 190)));
  assert.throws(() => price(safeBase + 1, 190), RangeError);
});

test('C07 lower-bound risk subtracts while upper-bound never gains risk bonus', () => {
  const lower = { trend: 1, reading: 100, risk: 4 };
  updateLayer(lower, 0, 'none', draws([1, -3, 4], [[-3,3], [-3,5], [0,4]]));
  assert.equal(lower.reading, 93);
  const upper = { trend: 1, reading: 100, risk: 4 };
  updateLayer(upper, 0, 'none', draws([1, 5], [[-3,3], [-3,5]]));
  assert.equal(upper.reading, 105);
});

test('C08 main contribution uses the existing target draw without another RNG call', () => {
  for (const target of [-3, 0, 3]) {
    const layer = { trend: 0, reading: 100, risk: 4 };
    const adjustmentBounds = target < 0 ? [-5,3] : target > 0 ? [-3,5] : [-3,3];
    updateLayer(layer, undefined, 'none', draws([target, 0], [[-3,3], adjustmentBounds]));
    assert.equal(layer.reading, 100 + Math.trunc(target / 3));
  }
  const child = { trend: 0, reading: 100, risk: 4 };
  updateLayer(child, 6, 'none', draws([-3, 0], [[-3,3], [-5,3]]));
  assert.equal(child.reading, 102, 'children use parent trend rather than their target');
});

test('floppy recovery/downward thresholds and shock multipliers clamp after adjustment', () => {
  const low = { trend: 0, reading: 10, risk: 4 };
  updateLayer(low, 0, 1, draws([-3,-9,12], [[-3,5], [-9,3], [0,12]]));
  assert.equal(low.reading, 10);
  const high = { trend: 0, reading: 190, risk: 4 };
  updateLayer(high, 0, 'boom', draws([3,9], [[-5,3], [-3,9]]));
  assert.equal(high.reading, 190);
  for (const shock of [1,2,3,'boom'] as const) {
    const layer = { trend: 0, reading: 100, risk: 4 };
    // target0 moves the shock-biased trend one step back toward zero.
    const range = shock === 'boom' ? [-3,7] : [-7,3];
    updateLayer(layer, 0, shock, draws([0,0], [[-3,3], range]));
    assert.equal(layer.reading, shock === 'boom' ? 110 : 80 + shock * 5);
  }
});

test('zero is a valid RNG seed; replay and full inclusive uint32 bounds are stable', () => {
  const state = fixture(0);
  assert.equal(random(state, 0, 0xffffffff), 1013904223);
  assert.equal(state.rng, 1013904223);
  const again = fixture(0);
  assert.equal(random(again, 0, 0xffffffff), 1013904223);
  assert.equal(random(state, -3, 3), random(again, -3, 3));
  assert.throws(() => random(state, 2, 1), RangeError);
  assert.throws(() => random(state, 0, 0x100000000), RangeError);
  assert.throws(() => random(state, Number.NaN, 1), RangeError);
  const before = state.rng;
  const singleton = Number.MAX_SAFE_INTEGER;
  assert.equal(random(state, singleton, singleton), singleton);
  assert.notEqual(state.rng, before, 'singleton draws still advance the stream');
  assert.ok(Number.isSafeInteger(random(state, singleton - 10, singleton)));
});

test('fixed-seed multilayer replay survives serialization and remains bounded', () => {
  const state = fixture(71);
  for (let week = 1; week <= 10; week++) { state.week = week; updateEconomy(state); }
  const resumed = JSON.parse(JSON.stringify(state)) as GameState;
  for (let week = 11; week <= 100; week++) {
    state.week = resumed.week = week;
    updateEconomy(state); updateEconomy(resumed);
    assert.deepEqual(state, resumed);
    for (const layer of Object.values(state.economy)) assert.ok(layer.reading >= 10 && layer.reading <= 190);
  }
  assert.notEqual(state.economy.goods.reading, state.economy.main.reading);
});

test('neutral fixtures reset layers and shock without consuming a draw', () => {
  const state = fixture(17);
  state.economyMode = 'neutral-fixture';
  state.economy.main.reading = 10; state.economy.goods.trend = -3; state.shock = 1;
  updateEconomy(state);
  assert.equal(state.rng, 17);
  assert.equal(state.shock, 'none');
  assert.deepEqual(state.economy, createEconomy());
});

test('floppy crash is gated before week four but boom is possible in week one', () => {
  // Search deterministic seeds rather than replacing the production RNG stream.
  let earlyBoom = false;
  let lateCrash = false;
  for (let seed = 0; seed < 2000; seed++) {
    const early = fixture(seed); updateEconomy(early);
    assert.ok(early.shock === 'none' || early.shock === 'boom');
    earlyBoom ||= early.shock === 'boom';
    const late = fixture(seed); late.week = 4; updateEconomy(late);
    lateCrash ||= typeof late.shock === 'number';
  }
  assert.ok(earlyBoom); assert.ok(lateCrash);
});
