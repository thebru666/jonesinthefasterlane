import type { Economy, EconomyLayer, GameState, Shock } from './types.ts';
import { random } from './rng.ts';

/** All eight persisted layers start at neutral readings; risks are market-specific. */
export function createEconomy(): Economy {
  const layer = (risk = 4): EconomyLayer => ({ trend: 0, reading: 100, risk });
  return {
    main: layer(), investments: layer(), goods: layer(), gold: layer(2),
    silver: layer(2), pork: layer(), blue: layer(1), penny: layer(10),
  };
}

/** Audited ordinary-range split integer price arithmetic (ECON-003).
 * Safe JS integer amounts only: no emulation of legacy 16-bit overflow branches.
 */
export function price(base: number, reading: number): number {
  if (!Number.isSafeInteger(base) || base < 0 || !Number.isSafeInteger(reading) || reading < 10 || reading > 190) {
    throw new RangeError('Price expects a nonnegative integer base and reading 10..190');
  }
  const factor = Math.max(50, reading < 100
    ? reading - Math.trunc(2 * (100 - reading) / 3)
    : reading + Math.trunc(2 * (reading - 100) / 3));
  if (!Number.isSafeInteger(base * factor)) throw new RangeError('Price product exceeds safe integer arithmetic');
  return Math.max(1, Math.trunc(base * Math.trunc(factor / 10) / 10) + Math.trunc(base * (factor % 10) / 100));
}

type Draw = (low: number, high: number) => number;

/** Analytical reconstruction of ECON-002, floppy bounds. Undefined parent means
 * the main layer's explicit C08 target contribution; no extra draw is consumed.
 * Mutates only this layer, and returns its target for deterministic audit tests.
 */
export function updateLayer(layer: EconomyLayer, parent: number | undefined, shock: Shock, draw: Draw): number {
  let trend = layer.trend;
  if (typeof shock === 'number') trend = trend > -3 ? Math.max(-3, trend - 3) : trend - 1;
  if (shock === 'boom') trend = trend < 3 ? Math.min(3, trend + 3) : trend + 1;
  const recovery = layer.reading < 40 ? 2 : layer.reading < 70 ? 1 : 0;
  const downward = layer.reading > 160 ? 2 : layer.reading > 130 ? 1 : 0;
  const target = draw(-3 - downward, 3 + recovery);
  if (trend < target) trend = Math.min(trend + 1, 3 + recovery);
  else if (trend > target) trend = Math.max(trend - 1, -3 - downward);
  layer.trend = trend;
  const lower = -3 + 2 * Math.min(trend, 0);
  const upper = 3 + 2 * Math.max(trend, 0);
  let adjustment = draw(lower, upper);
  // C07 intentionally retains only the shipped lower-bound extra adjustment.
  // The duplicated alternative condition cannot provide an upper-bound bonus.
  if (adjustment === lower) adjustment -= draw(0, layer.risk * Math.abs(trend));
  let reading = layer.reading + adjustment + Math.trunc((parent ?? target) / 3);
  if (typeof shock === 'number') reading = Math.trunc(reading * (16 + shock) / 20);
  else if (shock === 'boom') reading = Math.trunc(reading * 11 / 10);
  layer.reading = Math.max(10, Math.min(190, reading));
  return target;
}

/** One update per incoming participant, including week one. Event eligibility
 * uses the PRE-update main reading; employment consequences belong to turn flow.
 */
export function updateEconomy(state: GameState): void {
  if (state.economyMode === 'neutral-fixture') {
    state.economy = createEconomy();
    state.shock = 'none';
    return;
  }
  const draw: Draw = (low, high) => random(state, low, high);
  const previous = state.economy.main.reading;
  const count = state.players.length;
  if (count < 1) throw new RangeError('An economy update requires a player');
  let shock: Shock = 'none';
  if (state.week >= 4 && previous >= 80 && draw(0, 20 * count) === 0) {
    shock = draw(1, 3) as 1 | 2 | 3;
  } else if (previous <= 120 && draw(0, 30 * count) === 0) {
    shock = 'boom';
  }
  state.shock = shock;
  const economy = state.economy;
  updateLayer(economy.main, undefined, shock, draw);
  updateLayer(economy.investments, economy.main.trend, shock, draw);
  updateLayer(economy.goods, economy.main.trend, shock, draw);
  for (const key of ['gold', 'silver', 'pork', 'blue', 'penny'] as const) {
    updateLayer(economy[key], economy.investments.trend, shock, draw);
  }
}
