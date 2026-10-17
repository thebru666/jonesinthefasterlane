import type { GameState, Goals, Player } from './types.ts';
export const activePlayer = (s: GameState): Player => s.players[s.active]!;
export const learning = (p: Player): number => Math.min(100, Math.floor(p.workTime / 12) + 10 * p.qualifications.length);
export const allowance = (p: Player): number => 5 * Math.floor(learning(p) / 10);
export const clothingStock = (p: Player): number => Math.max(p.clothes.casual, p.clothes.dress, p.clothes.suit);
export const scores = (p: Player): Goals => ({ wealth: Math.min(100, Math.max(0, Math.trunc((p.cash - p.rentDebt) / 100))), happiness: p.happiness, career: p.job ? Math.min(100, 10 * Math.floor(p.dependability / 8)) : 0, learning: learning(p) });
export const reachedGoals = (p: Player): boolean => Object.entries(scores(p)).every(([key, value]) => value >= p.goals[key as keyof Goals]);
export const happy = (p: Player, amount: number): void => { p.happiness = Math.max(0, Math.min(100, p.happiness + amount)); };
