import type { GameState } from './types.ts';

/** prototype-0.1 RNG: uint32 Numerical Recipes LCG (1664525*x+1013904223).
 * Rejection sampling gives inclusive integer bounds without modulo bias.
 * This is the successor's reproducible stream, not the DOS generator.
 */
export function random(state: GameState, low: number, high: number): number {
  const span = high - low + 1;
  if (!Number.isSafeInteger(low) || !Number.isSafeInteger(high) || low > high || span > 0x100000000) {
    throw new RangeError('Random bounds must be integers spanning at most 2^32 outcomes');
  }
  const limit = Math.floor(0x100000000 / span) * span;
  let value: number;
  do {
    state.rng = (Math.imul(state.rng, 1664525) + 1013904223) >>> 0;
    value = state.rng;
  } while (value >= limit);
  return low + value % span;
}
