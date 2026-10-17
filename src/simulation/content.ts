import type { ItemId, JobId, PlaceId } from './types.ts';
export const PLACES: ReadonlyArray<{ id: PlaceId; name: string; active: boolean }> = [
  { id: 'home', name: 'Starter Court', active: true },
  { id: 'civic', name: 'Civic House', active: true },
  { id: 'market', name: 'Corner Basket', active: true },
  { id: 'hospitality', name: 'Daily Grind / Copper Spoon', active: true },
  { id: 'college', name: 'Next Chapter', active: true },
  { id: 'trades', name: 'TownWorks', active: false },
  { id: 'clinic', name: 'Community Clinic', active: false },
  { id: 'tech', name: 'Reboot', active: true },
  { id: 'depot', name: 'Parcel Depot', active: false },
  { id: 'pawn', name: 'Second Chance', active: false },
  { id: 'discount', name: 'Bargain Barn', active: false },
  { id: 'clothes', name: 'Good Threads', active: true },
  { id: 'bank', name: 'Nest Egg / Upstairs Studio', active: false },
  { id: 'cinema', name: 'Picture House / Rec Hall', active: false },
  { id: 'park', name: 'Parkside', active: false },
];
export interface Job { name: string; place: PlaceId; wage: number; experience: number; dependability: number; qualification?: string }
export const JOBS: Record<JobId, Job> = {
  cook: { name: 'Cook', place: 'hospitality', wage: 4, experience: 0, dependability: 10 },
  counter: { name: 'Counter Assistant', place: 'hospitality', wage: 5, experience: 10, dependability: 20 },
  supervisor: { name: 'Shift Supervisor', place: 'hospitality', wage: 10, experience: 25, dependability: 25 },
  manager: { name: 'Venue Manager', place: 'hospitality', wage: 14, experience: 35, dependability: 35 },
  checkout: { name: 'Checkout Assistant', place: 'market', wage: 8, experience: 20, dependability: 20 },
  butcher: { name: 'Butcher', place: 'market', wage: 12, experience: 30, dependability: 30, qualification: 'trade-school' },
};
export const ITEMS: Record<ItemId, { name: string; place: PlaceId; base: number; stock?: number }> = {
  groceries1: { name: 'One-week groceries', place: 'market', base: 55, stock: 1 },
  groceries2: { name: 'Two-week groceries', place: 'market', base: 100, stock: 2 },
  groceries4: { name: 'Four-week groceries', place: 'market', base: 190, stock: 4 },
  hamburger: { name: 'Hamburger', place: 'hospitality', base: 79 },
  cheeseburger: { name: 'Cheeseburger', place: 'hospitality', base: 89 },
  casual: { name: 'Casual clothes', place: 'clothes', base: 73, stock: 11 },
  dress: { name: 'Smart clothes', place: 'clothes', base: 125, stock: 13 },
  suit: { name: 'Business suit', place: 'clothes', base: 295, stock: 13 },
  bike: { name: 'Bike', place: 'tech', base: 120 },
  car: { name: 'Car', place: 'tech', base: 1200 },
  fridge: { name: 'Fridge', place: 'tech', base: 876 },
};
