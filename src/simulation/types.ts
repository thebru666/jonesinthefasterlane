export type PlaceId = 'home' | 'civic' | 'market' | 'hospitality' | 'college' | 'trades' | 'clinic' | 'tech' | 'depot' | 'pawn' | 'discount' | 'clothes' | 'bank' | 'cinema' | 'park';
export type Mode = 'walk' | 'bike' | 'bus' | 'car';
export type JobId = 'cook' | 'counter' | 'supervisor' | 'manager' | 'checkout' | 'butcher';
export type ItemId = 'groceries1' | 'groceries2' | 'groceries4' | 'hamburger' | 'cheeseburger' | 'casual' | 'dress' | 'suit' | 'bike' | 'car' | 'fridge';
export type Goals = { wealth: number; happiness: number; career: number; learning: number };
export type EconomyLayer = { trend: number; reading: number; risk: number };
export type Economy = { main: EconomyLayer; investments: EconomyLayer; goods: EconomyLayer; gold: EconomyLayer; silver: EconomyLayer; pork: EconomyLayer; blue: EconomyLayer; penny: EconomyLayer };
export type Shock = 'none' | 'boom' | 1 | 2 | 3;
export interface Player {
  id: string; name: string; cash: number; place: PlaceId; time: number;
  job: JobId | null; wage: number; baseWage: number; raises: number;
  experience: number; maxExperience: number; dependability: number;
  relaxation: number; happiness: number; workTime: number;
  qualifications: string[]; enrolled: boolean; lessons: number;
  clothes: { casual: number; dress: number; suit: number };
  groceries: number; meal: boolean;
  owns: { bike: boolean; car: boolean; fridge: boolean };
  rentStock: number; rentContract: number; rentDebt: number;
  extensionHistory: number; extensionAttempt: 0 | 1 | 2; rentOpen: boolean; rentAccounted: boolean;
  recoveryChecks: number; rejectionMemory: JobId[]; warned: boolean;
  rested: boolean; groceryBonus: boolean; mealBonus: boolean; carPaid: boolean;
  goals: Goals; finished: boolean;
}
export interface GameState {
  schema: 1; rules: 'prototype-0.1'; content: 'town-0.1';
  rng: number; sequence: number; week: number; active: number;
  players: Player[]; economy: Economy; shock: Shock;
  economyMode: 'live' | 'neutral-fixture';
  notices: string[]; status: 'playing' | 'finished';
}
export type Action =
  | { type: 'travel'; destination: PlaceId; mode: Mode }
  | { type: 'apply'; job: JobId }
  | { type: 'work' } | { type: 'buy'; item: ItemId }
  | { type: 'enroll' } | { type: 'study' } | { type: 'relax' }
  | { type: 'payRent' } | { type: 'payArrears' } | { type: 'extendRent' }
  | { type: 'endTurn' } | { type: 'acknowledge' };
export interface Intent { id: number; action: Action }
export interface Transition { state: GameState; accepted: boolean; message: string }
