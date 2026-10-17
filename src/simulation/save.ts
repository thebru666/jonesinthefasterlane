import { JOBS, PLACES } from './content.ts';
import type { GameState } from './types.ts';

/** Stable, version-specific snapshots. Imports validate data; they never run game rules. */
const MAX_BYTES = 1_048_576;
const MAX_COUNTER = 1_000_000_000;
const JOB_IDS = Object.keys(JOBS);
const PLACE_IDS = PLACES.filter(place => place.active).map(place => place.id);
const ECONOMY_RISKS: Record<string, number> = { main: 4, investments: 4, goods: 4, gold: 2, silver: 2, pork: 4, blue: 1, penny: 10 };
const ECONOMY_IDS = Object.keys(ECONOMY_RISKS);
const PLAYER_KEYS = [
  'id', 'name', 'cash', 'place', 'time', 'job', 'wage', 'baseWage', 'raises',
  'experience', 'maxExperience', 'dependability', 'relaxation', 'happiness', 'workTime',
  'qualifications', 'enrolled', 'lessons', 'clothes', 'groceries', 'meal', 'owns',
  'rentStock', 'rentContract', 'rentDebt', 'extensionHistory', 'extensionAttempt',
  'rentOpen', 'rentAccounted', 'recoveryChecks', 'rejectionMemory', 'warned', 'rested',
  'groceryBonus', 'mealBonus', 'carPaid', 'goals', 'finished',
];
function fail(path: string, detail: string): never {
  throw new Error(`Invalid save: ${path} ${detail}`);
}
function record(value: unknown, path: string, keys: string[]): Record<string, unknown> {
  if (typeof value !== 'object' || value === null || Array.isArray(value)) fail(path, 'must be an object');
  const obj = value as Record<string, unknown>;
  if (Object.keys(obj).length !== keys.length || !keys.every(key => Object.hasOwn(obj, key))) {
    fail(path, 'has missing or unsupported fields');
  }
  return obj;
}
function integer(value: unknown, path: string, min = 0, max = MAX_COUNTER): number {
  if (typeof value !== 'number' || !Number.isSafeInteger(value) || value < min || value > max) {
    fail(path, `must be an integer from ${min} to ${max}`);
  }
  return value;
}
function boolean(value: unknown, path: string): void {
  if (typeof value !== 'boolean') fail(path, 'must be boolean');
}
function text(value: unknown, path: string, max: number): string {
  if (typeof value !== 'string' || value.trim().length === 0 || value.length > max || /[\u0000-\u001f]/u.test(value)) {
    fail(path, `must be nonempty text of at most ${max} characters`);
  }
  return value;
}
function member(value: unknown, path: string, choices: readonly unknown[]): void {
  if (!choices.includes(value)) fail(path, 'contains an unsupported value');
}
function uniqueList(value: unknown, path: string, choices: readonly string[]): string[] {
  if (!Array.isArray(value) || value.length > choices.length) fail(path, 'must be a bounded list');
  for (const element of value) member(element, path, choices);
  if (new Set(value).size !== value.length) fail(path, 'contains duplicate entries');
  return value as string[];
}
function validate(value: unknown): GameState {
  const state = record(value, 'state', ['schema', 'rules', 'content', 'rng', 'sequence', 'week', 'active', 'players', 'economy', 'shock', 'economyMode', 'notices', 'status']);
  member(state.schema, 'schema', [1]);
  member(state.rules, 'rules', ['prototype-0.1']);
  member(state.content, 'content', ['town-0.1']);
  integer(state.rng, 'rng', 0, 0xffffffff);
  integer(state.sequence, 'sequence');
  integer(state.week, 'week', 1);
  member(state.economyMode, 'economyMode', ['live', 'neutral-fixture']);
  member(state.shock, 'shock', ['none', 'boom', 1, 2, 3]);
  member(state.status, 'status', ['playing', 'finished']);
  if (!Array.isArray(state.notices) || state.notices.length !== 0) fail('notices', 'must be empty at a stable save boundary');
  if (!Array.isArray(state.players) || state.players.length < 1 || state.players.length > 4) fail('players', 'must contain one to four players');
  integer(state.active, 'active', 0, state.players.length - 1);
  const ids = new Set<string>();
  for (const [index, rawPlayer] of state.players.entries()) {
    const path = `players[${index}]`;
    const p = record(rawPlayer, path, PLAYER_KEYS);
    const id = text(p.id, `${path}.id`, 64);
    if (ids.has(id)) fail(`${path}.id`, 'is duplicated');
    ids.add(id);
    text(p.name, `${path}.name`, 80);
    member(p.place, `${path}.place`, PLACE_IDS);
    member(p.job, `${path}.job`, [null, ...JOB_IDS]);
    for (const key of ['cash', 'wage', 'baseWage', 'raises', 'experience', 'maxExperience', 'dependability', 'workTime', 'groceries', 'rentStock', 'rentContract', 'rentDebt', 'recoveryChecks']) {
      integer(p[key], `${path}.${key}`);
    }
    integer(p.time, `${path}.time`, 0, 60);
    integer(p.relaxation, `${path}.relaxation`, 10, 50);
    integer(p.extensionHistory, `${path}.extensionHistory`, -1);
    integer(p.happiness, `${path}.happiness`, 0, 100);
    integer(p.lessons, `${path}.lessons`, 0, 10);
    integer(p.extensionAttempt, `${path}.extensionAttempt`, 0, 2);
    for (const key of ['enrolled', 'meal', 'rentOpen', 'rentAccounted', 'warned', 'rested', 'groceryBonus', 'mealBonus', 'carPaid', 'finished']) boolean(p[key], `${path}.${key}`);
    const qualifications = uniqueList(p.qualifications, `${path}.qualifications`, ['trade-school']);
    uniqueList(p.rejectionMemory, `${path}.rejectionMemory`, JOB_IDS);
    if (qualifications.length > 0 && (p.lessons !== 10 || p.enrolled !== false)) fail(path, 'has inconsistent course completion');
    if (qualifications.length === 0 && (p.lessons === 10 || (p.enrolled === false && p.lessons !== 0))) fail(path, 'has inconsistent course progress');
    const clothes = record(p.clothes, `${path}.clothes`, ['casual', 'dress', 'suit']);
    for (const key of ['casual', 'dress', 'suit']) integer(clothes[key], `${path}.clothes.${key}`);
    const owns = record(p.owns, `${path}.owns`, ['bike', 'car', 'fridge']);
    for (const key of ['bike', 'car', 'fridge']) boolean(owns[key], `${path}.owns.${key}`);
    const goals = record(p.goals, `${path}.goals`, ['wealth', 'happiness', 'career', 'learning']);
    for (const key of ['wealth', 'happiness', 'career', 'learning']) {
      const target = integer(goals[key], `${path}.goals.${key}`, 10, 100);
      if (target % 10 !== 0) fail(`${path}.goals.${key}`, 'must be a multiple of ten');
    }
  }
  const economy = record(state.economy, 'economy', ECONOMY_IDS);
  for (const id of ECONOMY_IDS) {
    const layer = record(economy[id], `economy.${id}`, ['trend', 'reading', 'risk']);
    integer(layer.trend, `economy.${id}.trend`, -100, 100);
    integer(layer.reading, `economy.${id}.reading`, 10, 190);
    member(layer.risk, `economy.${id}.risk`, [ECONOMY_RISKS[id]]);
  }
  const players = state.players as GameState['players'];
  if (state.status === 'finished' && !players.every(p => p.finished)) fail('status', 'does not match finished players');
  if (state.status === 'playing' && players.every(p => p.finished)) fail('status', 'requires an unfinished player');
  // Every field has been checked above. No prototype methods, callbacks or pending action are restored.
  return value as GameState;
}

export function exportSave(state: GameState): string {
  validate(state);
  const result = JSON.stringify(state);
  if (new TextEncoder().encode(result).byteLength > MAX_BYTES) fail('document', 'exceeds one megabyte');
  return result;
}

export function importSave(text: string): GameState {
  if (typeof text !== 'string' || text.length > MAX_BYTES || new TextEncoder().encode(text).byteLength > MAX_BYTES) fail('document', 'exceeds one megabyte or is not text');
  let data: unknown;
  try { data = JSON.parse(text); }
  catch { fail('document', 'is not valid JSON'); }
  return validate(data);
}
