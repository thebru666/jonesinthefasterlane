import test from 'node:test';
import assert from 'node:assert/strict';
import { encodeBrowserSave, decodeBrowserSave } from '../src/browser-save.ts';
import { createGame } from '../src/simulation/engine.ts';
import { exportSave } from '../src/simulation/save.ts';
test('browser checkpoint preserves the nested view without running rules on restore', () => {
  const game = createGame({ seed: 42, economyMode: 'neutral-fixture' }); game.players[0]!.place = 'civic';
  const saved = encodeBrowserSave(game, { route: 'visit', tab: 'jobs' });
  assert.deepEqual(decodeBrowserSave(saved), { game, view: { route: 'visit', tab: 'jobs' } });
});
test('headless game imports get an explicit town view', () => {
  const game = createGame({ economyMode: 'neutral-fixture' });
  assert.deepEqual(decodeBrowserSave(exportSave(game)).view, { route: 'town', tab: 'actions' });
});
test('bad browser envelopes, unavailable views and pending outcomes are rejected', () => {
  const game = createGame({ economyMode: 'neutral-fixture' });
  const bad = JSON.parse(encodeBrowserSave(game, { route: 'town', tab: 'actions' }));
  bad.view.tab = 'jobs'; assert.throws(() => decodeBrowserSave(JSON.stringify(bad)), /unavailable/);
  bad.view.tab = 'actions'; bad.view.route = ['town']; assert.throws(() => decodeBrowserSave(JSON.stringify(bad)), /view/);
  bad.view.route = 'town'; bad.version = 2; assert.throws(() => decodeBrowserSave(JSON.stringify(bad)), /version/);
  game.notices.push('Pending'); assert.throws(() => encodeBrowserSave(game, { route: 'town', tab: 'actions' }), /stable/);
});
