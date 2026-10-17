import { exportSave, importSave } from './simulation/save.ts';
import type { GameState } from './simulation/types.ts';
export type View = { route: 'town' | 'visit'; tab: 'actions' | 'jobs' };
export interface BrowserSave { game: GameState; view: View }
export function encodeBrowserSave(game: GameState, view: View): string {
  return JSON.stringify({ format: 'jones-browser', version: 1, game: JSON.parse(exportSave(game)), view });
}
export function decodeBrowserSave(text: string): BrowserSave {
  if (text.length > 1_048_576) throw new Error('Save is too large.');
  const data: unknown = JSON.parse(text);
  if (typeof data === 'object' && data !== null && 'format' in data) {
    const envelope = data as Record<string, unknown>;
    if (Object.keys(envelope).sort().join(',') !== 'format,game,version,view' || envelope.format !== 'jones-browser' || envelope.version !== 1) throw new Error('Unsupported browser save version.');
    const rawView = envelope.view;
    if (!rawView || typeof rawView !== 'object' || Array.isArray(rawView)) throw new Error('Invalid saved view.');
    const view = rawView as Record<string, unknown>;
    if (Object.keys(view).sort().join(',') !== 'route,tab' || (view.route !== 'town' && view.route !== 'visit') || (view.tab !== 'actions' && view.tab !== 'jobs')) throw new Error('Invalid saved view.');
    const game = importSave(JSON.stringify(envelope.game));
    if (view.tab === 'jobs' && !['civic', 'market', 'hospitality'].includes(game.players[game.active]!.place)) throw new Error('Saved jobs view is unavailable at this place.');
    return { game, view: view as View };
  }
  // Headless exports are also useful diagnostic imports, with no UI selection.
  return { game: importSave(text), view: { route: 'town', tab: 'actions' } };
}
