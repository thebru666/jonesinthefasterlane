import { ITEMS, JOBS, PLACES } from './content.ts';
import { createEconomy, price } from './economy.ts';
import { random } from './rng.ts';
import { activePlayer, allowance, clothingStock, happy } from './selectors.ts';
import { endTurn, prepareTurn } from './turns.ts';
import type { Action, GameState, Goals, Intent, Mode, PlaceId, Player, Transition } from './types.ts';

export const LIMIT = 1_000_000_000;
export interface NewGameOptions { seed?: number; names?: string[]; goals?: Goals; economyMode?: 'live' | 'neutral-fixture' }
export function createGame(options: NewGameOptions = {}): GameState {
  const names = options.names ?? ['Player 1'];
  if (names.length < 1 || names.length > 4 || names.some(n => typeof n !== 'string' || !n.trim() || n.length > 40 || /[\u0000-\u001f]/u.test(n))) throw new Error('Choose one to four names of 1–40 characters.');
  const seed = options.seed ?? 1;
  if (!Number.isInteger(seed) || seed < 0 || seed > 0xffffffff) throw new Error('Seed must be an unsigned 32-bit integer.');
  const goals = options.goals ?? { wealth: 10, happiness: 20, career: 30, learning: 10 };
  if (Object.values(goals).length !== 4 || ['wealth', 'happiness', 'career', 'learning'].some(k => !Number.isInteger(goals[k as keyof Goals]) || goals[k as keyof Goals] < 10 || goals[k as keyof Goals] > 100 || goals[k as keyof Goals] % 10 !== 0)) throw new Error('Goals must be 10–100 in steps of ten.');
  if (options.economyMode !== undefined && options.economyMode !== 'live' && options.economyMode !== 'neutral-fixture') throw new Error('Unsupported economy mode.');
  const players: Player[] = names.map((name, i) => ({
    id: `player-${i + 1}`, name: name.trim(), cash: 200, place: 'home', time: 60,
    job: null, wage: 0, baseWage: 0, raises: 0,
    experience: 10, maxExperience: 10, dependability: 20, relaxation: 25, happiness: 0, workTime: 0,
    qualifications: [], enrolled: false, lessons: 0,
    clothes: { casual: 6, dress: 0, suit: 0 }, groceries: 0, meal: false,
    owns: { bike: false, car: false, fridge: false },
    rentStock: 3, rentContract: 325, rentDebt: 0,
    extensionHistory: 0, extensionAttempt: 0, rentOpen: false, rentAccounted: false,
    recoveryChecks: 0, rejectionMemory: [], warned: true,
    rested: false, groceryBonus: false, mealBonus: false, carPaid: false,
    goals: { ...goals }, finished: false,
  }));
  const state: GameState = { schema: 1, rules: 'prototype-0.1', content: 'town-0.1', rng: seed,
    sequence: 0, week: 1, active: 0, players, economy: createEconomy(), shock: 'none',
    economyMode: options.economyMode ?? 'live', notices: [], status: 'playing' };
  prepareTurn(state);
  return state;
}

export interface TripQuote { available: boolean; distance: number; travelTime: number; entryTime: number; cash: number; message: string }
export function quoteTrip(state: GameState, destination: PlaceId, mode: Mode): TripQuote {
  const p = activePlayer(state);
  const to = PLACES.findIndex(place => place.id === destination && place.active);
  const from = PLACES.findIndex(place => place.id === p.place);
  const fail = (message: string): TripQuote => ({ available: false, distance: 0, travelTime: 0, entryTime: 0, cash: 0, message });
  if (to < 0 || from < 0) return fail('That destination is a preview only.');
  if (!['walk', 'bike', 'bus', 'car'].includes(mode)) return fail('Choose an available transport mode.');
  if (state.status !== 'playing' || p.finished || state.notices.length) return fail('Finish the current outcome before travelling.');
  if (destination === p.place) return { available: true, distance: 0, travelTime: 0, entryTime: 0, cash: 0, message: 'Already here — reopen free.' };
  const distance = Math.min(Math.abs(to - from), PLACES.length - Math.abs(to - from));
  const travelTime = mode === 'walk' ? 3 * distance : mode === 'bike' ? Math.ceil(1.5 * distance) : mode === 'bus' ? 2 + distance : 1 + Math.ceil(distance / 2);
  const cash = mode === 'bus' ? 3 : mode === 'car' ? 4 + (p.carPaid ? 0 : 20) : 0;
  const access = mode === 'bike' ? p.owns.bike : mode === 'car' ? p.owns.car : true;
  const available = state.status === 'playing' && !p.finished && state.notices.length === 0 && access && p.cash >= cash && p.time >= travelTime + 2;
  const message = !access ? `Own a ${mode} first.` : p.cash < cash ? `Need $${cash}.` : p.time < travelTime + 2 ? `Need ${travelTime + 2} time.` : `${travelTime} travel + 2 entry, $${cash}.`;
  return { available, distance, travelTime, entryTime: 2, cash, message };
}

// Each accepted request number is consumed once, including paid refusals.
// A stale/double request cannot charge, draw randomness or replay an award.
export function dispatch(previous: GameState, intent: Intent): Transition {
  if (!intent || !Number.isSafeInteger(intent.id) || intent.id !== previous.sequence + 1 || intent.id > LIMIT) return { state: previous, accepted: false, message: 'Stale or out-of-order request.' };
  if (!intent.action || typeof intent.action.type !== 'string') return { state: previous, accepted: false, message: 'Invalid action.' };
  const action = intent.action;
  if (previous.notices.length && action.type !== 'acknowledge') return { state: previous, accepted: false, message: 'Acknowledge the current outcome first.' };
  if (previous.status === 'finished' && action.type !== 'acknowledge') return { state: previous, accepted: false, message: 'The game is finished.' };
  if (activePlayer(previous).finished && action.type !== 'endTurn' && action.type !== 'acknowledge') return { state: previous, accepted: false, message: 'Continue to the next participant.' };
  const state = structuredClone(previous);
  state.sequence = intent.id;
  const p = activePlayer(state);
  const done = (accepted: boolean, message: string): Transition => {
    if (action.type !== 'acknowledge' && message) state.notices.push(message);
    return { state, accepted, message };
  };
  const timed = (cost: number): boolean => { if (p.time <= 0) return false; p.time = Math.max(0, p.time - cost); return true; };
  const quote = (base: number): number => price(base, state.economy.goods.reading);
  switch (action.type) {
    case 'acknowledge':
      if (!state.notices.length) return done(false, 'No pending outcome.');
      state.notices.shift();
      return { state, accepted: true, message: 'Acknowledged.' };
    case 'travel': {
      const trip = quoteTrip(previous, action.destination, action.mode);
      if (!trip.available) return done(false, trip.message);
      p.cash -= trip.cash;
      p.time -= trip.travelTime + trip.entryTime;
      if (trip.distance && action.mode === 'car') p.carPaid = true;
      p.place = action.destination;
      return done(true, trip.distance ? `Arrived at ${PLACES.find(v => v.id === p.place)!.name}.` : 'Already here.');
    }
    case 'apply': {
      const job = Object.hasOwn(JOBS, action.job) ? JOBS[action.job] : undefined;
      if (!job || (p.place !== 'civic' && p.place !== job.place)) return done(false, 'Apply at Civic House or this employer.');
      if (!timed(4)) return done(false, 'No time to apply.');
      const chance = 30 + Math.trunc((p.dependability + p.experience + 8 * p.qualifications.length + 10) / 3);
      const roll = random(state, 1, 100); // Cook and raises still consume the ordinary opening draw.
      const qualified = (!job.qualification || p.qualifications.includes(job.qualification)) && p.experience >= job.experience && p.dependability >= (job.dependability === 10 ? 0 : job.dependability);
      const opening = action.job === 'cook' || (roll <= chance && !p.rejectionMemory.includes(action.job));
      const offer = quote(job.wage);
      if (p.job === action.job) {
        if (offer <= p.wage) return done(false, 'Your current wage is already at least this offer.');
        if (p.dependability < job.dependability + 5 * p.raises) return done(false, 'Build more dependable work history for a raise.');
        if (p.raises === LIMIT) return done(false, 'Supported resource limit reached.');
        p.wage = offer; p.raises++; happy(p, 3);
        return done(true, `Raise granted: $${offer} hourly wage.`);
      }
      if (!qualified) { happy(p, -1); return done(false, !job.qualification || p.qualifications.includes(job.qualification) ? p.experience < job.experience ? 'More experience is required.' : 'More dependable work history is required.' : 'Complete Trade School first.'); }
      if (!opening) { if (!p.rejectionMemory.includes(action.job)) p.rejectionMemory.push(action.job); happy(p, -1); return done(false, 'No opening this turn. Try this role next turn.'); }
      if (p.experience > LIMIT - 2) return done(false, 'Supported resource limit reached.');
      p.job = action.job; p.wage = offer; p.baseWage = job.wage; p.raises = 0;
      p.experience += 2; p.maxExperience = job.experience + 10 + (job.experience === 0 ? 10 : 0);
      p.dependability = Math.max(10, p.dependability); happy(p, 3);
      return done(true, `Hired as ${job.name}. Work at ${PLACES.find(v => v.id === job.place)!.name}.`);
    }
    case 'work': {
      const job = p.job && JOBS[p.job];
      if (!job || p.place !== job.place) return done(false, 'Travel to your current workplace first.');
      if (p.time <= 0) return done(false, 'No time to work.');
      if (!clothingStock(p)) return done(false, 'You need usable work clothes.');
      if (p.dependability < job.dependability - 5) { p.job = null; p.wage = 0; p.baseWage = 0; return done(false, 'Dismissed for poor attendance. Cook remains a recovery option.'); }
      if (p.dependability < job.dependability - 2 && p.warned) state.notices.push('Attendance warning: work regularly to keep this job.');
      const actualTime = Math.min(6, p.time);
      const gross = Math.trunc(8 * p.wage * actualTime / 6);
      if (p.workTime + actualTime > LIMIT || p.cash + gross > LIMIT) return done(false, 'Supported resource limit reached.');
      let net = gross;
      if (p.rentDebt > 0) {
        const half = Math.trunc(gross / 2);
        if (half > p.rentDebt) { net = gross - p.rentDebt; p.rentDebt = 0; }
        else { p.rentDebt -= half; net = Math.max(0, half - 2); }
        p.extensionHistory = -1;
      }
      const steps = Math.floor((p.workTime + actualTime) / 6) - Math.floor(p.workTime / 6);
      p.workTime += actualTime;
      const credit = allowance(p);
      // Blocked growth is consumed, never saved up for a later role.
      if (p.experience < p.maxExperience + credit) p.experience = Math.min(LIMIT, p.maxExperience + credit, p.experience + steps);
      if (p.dependability < job.dependability + 20 + credit) p.dependability = Math.min(LIMIT, job.dependability + 20 + credit, p.dependability + steps);
      p.cash += net; p.time -= actualTime; p.warned = false;
      return done(true, `Worked ${actualTime} time: $${gross} gross, $${net} paid${gross !== net ? ' after rent garnishment' : ''}.`);
    }
    case 'buy': {
      const item = Object.hasOwn(ITEMS, action.item) ? ITEMS[action.item] : undefined;
      if (!item || p.place !== item.place) return done(false, 'This item is sold at another location.');
      if ((action.item === 'bike' || action.item === 'car' || action.item === 'fridge') && p.owns[action.item]) return done(false, 'You already own one.');
      const cost = quote(item.base);
      if (p.cash < cost) return done(false, `Need $${cost} for ${item.name}.`);
      if (action.item.startsWith('groceries') && p.groceries + item.stock! > LIMIT) return done(false, 'Supported stock limit reached.');
      if ((action.item === 'casual' || action.item === 'dress' || action.item === 'suit') && p.clothes[action.item] + item.stock! > LIMIT) return done(false, 'Supported stock limit reached.');
      p.cash -= cost;
      if (action.item.startsWith('groceries')) { p.groceries += item.stock!; if (!p.groceryBonus) { happy(p, item.stock!); p.groceryBonus = true; } }
      else if (action.item === 'hamburger' || action.item === 'cheeseburger') { p.meal = true; if (action.item === 'cheeseburger' && !p.mealBonus) { happy(p, 1); p.mealBonus = true; } }
      else if (action.item === 'casual' || action.item === 'dress' || action.item === 'suit') { p.clothes[action.item] += item.stock!; p.recoveryChecks = 0; happy(p, action.item === 'suit' ? 2 : action.item === 'dress' ? 1 : 0); }
      else if (action.item === 'bike' || action.item === 'car' || action.item === 'fridge') p.owns[action.item] = true;
      return done(true, `Bought ${item.name} for $${cost}.`);
    }
    case 'enroll': {
      if (p.place !== 'college') return done(false, 'Enroll at Next Chapter.');
      if (p.enrolled || p.qualifications.includes('trade-school')) return done(false, 'Your one available course is already enrolled or complete.');
      const cost = quote(50);
      if (p.cash < cost) return done(false, `Need $${cost} to enroll.`);
      p.cash -= cost; p.enrolled = true;
      return done(true, `Trade School enrollment paid: $${cost}.`);
    }
    case 'study':
      if (p.place !== 'college' || !p.enrolled || p.qualifications.includes('trade-school')) return done(false, 'Enroll in Trade School at Next Chapter first.');
      if (p.lessons === 9 && p.dependability > LIMIT - 5) return done(false, 'Supported resource limit reached.');
      if (!timed(6)) return done(false, 'No time to attend.');
      p.lessons++;
      if (p.lessons === 10) { p.qualifications.push('trade-school'); p.enrolled = false; happy(p, 5); p.dependability += 5; return done(true, 'Trade School complete! Qualification earned; +10 Learning.'); }
      return done(true, `Trade School: ${p.lessons}/10 lessons.`);
    case 'relax':
      if (p.place !== 'home') return done(false, 'Relax at Starter Court.');
      if (!timed(6)) return done(false, 'No time to relax.');
      p.relaxation = Math.min(50, p.relaxation + 3);
      if (!p.rested) { happy(p, 2); p.rested = true; }
      return done(true, 'A little rest goes a long way.');
    case 'payRent':
    case 'payArrears':
    case 'extendRent': {
      if (p.place !== 'civic' || (state.week % 4 !== 0 && !p.rentOpen)) return done(false, 'The rent counter opens in due weeks or after an approved extension.');
      if (action.type === 'payArrears') {
        if (p.rentDebt <= 0) return done(false, 'No rent arrears.');
        if (p.cash < p.rentDebt) return done(false, `Need $${p.rentDebt} to clear arrears.`);
        p.cash -= p.rentDebt; p.rentDebt = 0;
        return done(true, 'Rent arrears cleared; current rent is separate.');
      }
      if (action.type === 'payRent') {
        if (p.cash < p.rentContract) return done(false, `Need $${p.rentContract} rent.`);
        if (p.rentStock > LIMIT - (4 - state.week % 4)) return done(false, 'Supported stock limit reached.');
        p.cash -= p.rentContract; p.rentStock += 4 - state.week % 4;
        return done(true, 'Rent paid at your stored contract price.');
      }
      if (p.rentStock > 0 || p.extensionAttempt !== 0) return done(false, 'No new extension request is available this turn.');
      const success = p.extensionHistory === 0 || (p.extensionHistory > 0 && random(state, 1, 12) > (p.extensionHistory === 1 ? 3 : p.extensionHistory === 2 ? 6 : 9));
      p.extensionAttempt = success ? 1 : 2;
      if (success) p.extensionHistory = Math.min(LIMIT, p.extensionHistory + 1);
      happy(p, success ? 1 : -1);
      return done(success, success ? 'Extension approved; the counter remains available next turn. No rent stock granted.' : 'Rent extension refused.');
    }
    case 'endTurn':
      try { endTurn(state); }
      catch (error) {
        if (!(error instanceof RangeError)) throw error;
        const rejected = structuredClone(previous); rejected.sequence = intent.id; rejected.notices.push(error.message);
        return { state: rejected, accepted: false, message: error.message };
      }
      return { state, accepted: true, message: 'Turn completed.' };
    default:
      return done(false, 'Unsupported action.');
  }
}
