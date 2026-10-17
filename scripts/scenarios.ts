/** Deterministic action-driven fixtures. No balance/cash/progression overrides in campaigns. */
import { createGame, dispatch, quoteTrip } from '../src/simulation/engine.ts';
import { ITEMS, JOBS } from '../src/simulation/content.ts';
import { price } from '../src/simulation/economy.ts';
import { clothingStock, scores } from '../src/simulation/selectors.ts';
import { exportSave, importSave } from '../src/simulation/save.ts';
import type { Action, GameState, Intent, JobId, PlaceId } from '../src/simulation/types.ts';
export function driver(initial: GameState) {
  let state = initial;
  const intents: Intent[] = [];
  const ledger: unknown[] = [];
  function send(action: Action): boolean {
    const intent = { id: state.sequence + 1, action };
    const result = dispatch(state, intent);
    intents.push(intent); state = result.state;
    const p = state.players[state.active]!;
    ledger.push({ request: intent.id, action, accepted: result.accepted, message: result.message, week: state.week, player: p.id,
      cash: p.cash, time: p.time, job: p.job, experience: p.experience, dependability: p.dependability, workTime: p.workTime,
      lessons: p.lessons, qualifications: [...p.qualifications], scores: scores(p) });
    while (state.notices.length) {
      const ack: Intent = { id: state.sequence + 1, action: { type: 'acknowledge' } };
      intents.push(ack); state = dispatch(state, ack).state;
    }
    return result.accepted;
  }
  return { get state() { return state; }, intents, ledger, send };
}

export function openingScenario() {
  const d = driver(createGame({ seed: 42, economyMode: 'neutral-fixture' }));
  d.send({ type: 'travel', destination: 'hospitality', mode: 'walk' });
  d.send({ type: 'apply', job: 'cook' });
  for (let i = 0; i < 7; i++) d.send({ type: 'work' });
  d.send({ type: 'buy', item: 'hamburger' });
  const beforeEnd = structuredClone(d.state.players[0]!);
  d.send({ type: 'endTurn' });
  return { initialOptions: { seed: 42, economyMode: 'neutral-fixture' as const }, beforeEnd, final: d.state, intents: d.intents, ledger: d.ledger };
}

export function campaign(route: 'work-first' | 'butcher', seed = 42, economyMode: 'live' | 'neutral-fixture' = 'live') {
  const options = { seed, economyMode };
  const d = driver(createGame(options));
  const p = () => d.state.players[0]!;
  const go = (destination: PlaceId): boolean => {
    if (p().place === destination) return true;
    const choices = (['walk', 'bus', 'bike', 'car'] as const).map(mode => ({ mode, quote: quoteTrip(d.state, destination, mode) }))
      .filter(v => v.quote.available).sort((a, b) => a.quote.travelTime - b.quote.travelTime || a.quote.cash - b.quote.cash);
    return choices[0] ? d.send({ type: 'travel', destination, mode: choices[0].mode }) : false;
  };
  const cost = (base: number) => price(base, d.state.economy.goods.reading);
  let reachedRole = false;
  for (let turn = 0; turn < 100 && d.state.status !== 'finished'; turn++) {
    if (d.state.notices.length) throw new Error('Campaign must start each turn stable.');
    if (route === 'work-first' || reachedRole) d.send({ type: 'relax' });
    if ((d.state.week % 4 === 0 || p().rentOpen) && p().cash >= p().rentContract && go('civic')) d.send({ type: 'payRent' });
    if (clothingStock(p()) <= 1 && p().cash >= cost(ITEMS.casual.base) && go('clothes')) d.send({ type: 'buy', item: 'casual' });
    if (go('hospitality')) {
      if (p().job === 'butcher' && p().cash >= cost(79)) d.send({ type: 'buy', item: 'hamburger' });
      const targets: JobId[] = route === 'work-first' ? ['manager', 'supervisor', 'counter', 'cook'] : ['cook'];
      for (const id of targets) {
        const job = JOBS[id];
        if (p().job === id || (p().job && JOBS[p().job!].wage > job.wage)) break;
        if (p().experience >= job.experience && p().dependability >= (job.dependability === 10 ? 0 : job.dependability) && !p().rejectionMemory.includes(id)) {
          if (d.send({ type: 'apply', job: id })) break;
        }
      }
      // Fund tuition/food first, preserving time for the short trip and two lessons.
      const studyNow = route === 'butcher' && !p().qualifications.length && p().cash >= cost(50) + cost(79) + 100;
      if (studyNow) {
        while (p().time > 28 && p().job && clothingStock(p())) { if (!d.send({ type: 'work' })) break; }
        if (go('college')) {
          if (!p().enrolled) d.send({ type: 'enroll' });
          for (let i = 0; i < 2 && !p().qualifications.length && p().time > 0; i++) d.send({ type: 'study' });
        }
      }
    }
    if (route === 'butcher' && p().qualifications.length && p().experience >= 30 && p().dependability >= 30 && go('market')) {
      if (p().job === 'butcher' || d.send({ type: 'apply', job: 'butcher' })) reachedRole = true;
    }
    const workPlace = p().job ? JOBS[p().job!].place : 'hospitality';
    if (go(workPlace)) while (p().time > 0 && p().job && clothingStock(p())) { if (!d.send({ type: 'work' })) break; }
    // Reserve a trip to a meal if work was at the market/college; do not buy it remotely.
    if (!p().meal && p().place === 'hospitality' && p().cash >= cost(79)) d.send({ type: 'buy', item: 'hamburger' });
    // A market worker needs food near the workplace: groceries keep the audited spoilage costs.
    else if (!p().meal && p().place === 'market' && p().cash >= cost(55)) d.send({ type: 'buy', item: 'groceries1' });
    if (route === 'work-first' && (p().job === 'supervisor' || p().job === 'manager')) reachedRole = true;
    d.send({ type: 'endTurn' });
  }
  const saved = exportSave(d.state);
  if (JSON.stringify(importSave(saved)) !== JSON.stringify(d.state)) throw new Error('Campaign save mismatch.');
  return { route, options, finished: d.state.status === 'finished', reachedRole, weeks: d.state.week,
    final: d.state, intents: d.intents, ledger: d.ledger };
}
