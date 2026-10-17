import { ITEMS } from './content.ts';
import { price, updateEconomy } from './economy.ts';
import { random } from './rng.ts';
import { activePlayer, clothingStock, happy, reachedGoals } from './selectors.ts';
import type { GameState } from './types.ts';

// Prototype subset of weekly-processing, food-and-housing and happiness-events.
// Notice effects are committed here; acknowledging a notice performs no mutation.
// Weekend, theft, tickets, loan, appliance and investment events are deliberately
// absent. C20 replaces the original cash donation, rather than running beside it.
export function prepareTurn(state: GameState): void {
  if (state.status === 'finished') return;
  const p = activePlayer(state);
  if (p.finished) return;
  p.place = 'home';
  p.time = 60;
  updateEconomy(state);

  // The subset has neither stove nor microwave: their pre-gate +1 is inactive.
  // Atomic derived scores replace the original redraw-dependent stored values.
  if (reachedGoals(p)) {
    p.finished = true;
    if (state.players.every(player => player.finished)) state.status = 'finished';
    state.notices.push(`${p.name} reached all four goals in week ${state.week}.`);
    state.shock = 'none';
    return;
  }

  p.rested = false;
  p.groceryBonus = false;
  p.mealBonus = false;
  p.carPaid = false;
  p.warned = true;
  p.rejectionMemory = [];
  if (state.week === 1) {
    state.shock = 'none';
    return;
  }

  p.relaxation = Math.max(10, p.relaxation - 1);
  // Remember coverage before spoilage and meal expiry. The -1 sentinel avoids
  // charging hunger time a second time when groceries were the sole spoiled food.
  let coverage = p.meal ? 2 : p.groceries > 0 ? 1 : 0;
  if (p.groceries > 0 && !p.owns.fridge) {
    p.groceries = 0;
    happy(p, -2);
    if (coverage === 1) coverage = -1;
    state.notices.push(`${p.name}'s groceries spoiled without a fridge.`);
  } else if (p.groceries > 6) {
    p.groceries = 6;
    happy(p, -1);
    state.notices.push(`${p.name}'s fridge holds six grocery units; the excess spoiled.`);
  }
  p.meal = false;
  let illnessGate = 1;
  if (coverage === 0) {
    happy(p, -2);
    illnessGate = random(state, 0, 3);
    p.time -= 20;
    state.notices.push(`${p.name} went hungry: 20 time lost.`);
  }
  if (coverage === -1) illnessGate = random(state, 0, 1);
  if (p.relaxation === 10 && random(state, 0, 4) === 0) illnessGate = 0;
  if (illnessGate === 0 && p.cash > 0) {
    happy(p, -4);
    const ceiling = Math.min(p.cash, p.cash < 500 ? 50 : 200);
    const bill = ceiling > 30 ? random(state, 30, ceiling) : ceiling;
    p.cash -= bill;
    p.time -= 10;
    state.notices.push(`${p.name} needed a doctor: $${bill} and 10 time lost.`);
  }

  p.groceries = Math.max(0, p.groceries - 1);
  p.rentStock = Math.max(0, p.rentStock - 1);
  for (const grade of ['casual', 'dress', 'suit'] as const) {
    p.clothes[grade] = Math.max(0, p.clothes[grade] - 1);
  }
  if (state.week % 4 === 0 && p.rentStock === 0) {
    p.rentAccounted = false;
    state.notices.push(`${p.name}'s rent is due: $${p.rentContract}.`);
  }
  if (clothingStock(p) === 1) {
    state.notices.push(`${p.name} has one turn of clothing left.`);
  }

  const shock = state.shock;
  if (typeof shock === 'number') {
    happy(p, -(4 - shock));
    state.notices.push(`Economic downturn, severity ${shock}.`);
    if (shock <= 2) {
      // One shared event, applied to each unfinished actor, not just the speaker.
      for (const player of state.players) {
        if (player.finished || !player.job || player.wage === 0) continue;
        if (random(state, 0, shock - 1) === 0) {
          player.job = null;
          player.wage = 0;
          happy(player, -7);
          state.notices.push(`${player.name} lost their job in the downturn.`);
        } else {
          player.wage = Math.max(1, Math.trunc(player.wage * 8 / 10));
          happy(player, -3);
          state.notices.push(`${player.name}'s wage was cut to $${player.wage}.`);
        }
      }
    }
  } else if (shock === 'boom') {
    // Investor happiness is inactive because this subset has no investments.
    state.notices.push('The economy is booming.');
  }
  state.shock = 'none';

  // C20: consecutive eligible recurring checks, no RNG and no durable-value gate.
  if (clothingStock(p) === 0 && p.cash < price(ITEMS.casual.base, state.economy.goods.reading)) {
    p.recoveryChecks += 1;
    if (p.recoveryChecks >= 2) {
      p.clothes.casual = 1;
      p.recoveryChecks = 0;
      state.notices.push(`${p.name} received temporary casual clothing to get back to work.`);
    }
  } else {
    p.recoveryChecks = 0;
  }
}

export function endTurn(state: GameState): void {
  if (state.status === 'finished') return;
  const outgoing = activePlayer(state);
  const needsArrears = !outgoing.finished && outgoing.rentStock === 0
    && outgoing.extensionAttempt !== 1 && !outgoing.rentAccounted
    && (state.week % 4 === 0 || outgoing.rentDebt === 0);
  const firstUnfinished = state.players.findIndex(player => !player.finished);
  let next = state.active;
  if (firstUnfinished !== -1) {
    do { next = (next + 1) % state.players.length; } while (state.players[next]!.finished);
  }
  // Reject unsupported imported-counter extremes before any outgoing mutation.
  // The public dispatcher converts this RangeError into an ordinary refusal.
  if ((needsArrears && outgoing.rentDebt + outgoing.rentContract > 1_000_000_000)
    || (firstUnfinished !== -1 && next === firstUnfinished && state.week >= 1_000_000_000)) {
    throw new RangeError('Supported turn or rent-debt limit reached.');
  }
  if (!outgoing.finished) {
    outgoing.dependability = Math.max(0, outgoing.dependability - 3);
    if (needsArrears) {
      outgoing.rentDebt += outgoing.rentContract;
      outgoing.rentAccounted = true;
    }
    outgoing.rentOpen = outgoing.extensionAttempt === 1;
    outgoing.extensionAttempt = 0;
  }
  if (state.players.every(player => player.finished)) {
    state.status = 'finished';
    return;
  }
  // Original round boundary is the first eligible participant, including when
  // earlier array entries have finished. Retirement/removal UI is not in scope.
  state.active = next;
  if (next === firstUnfinished) state.week += 1;
  prepareTurn(state);
}
