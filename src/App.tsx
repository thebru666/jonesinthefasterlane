import { useEffect, useRef, useState } from 'react';
import type { ReactNode } from 'react';
import { createGame, dispatch, quoteTrip } from './simulation/engine.ts';
import { ITEMS, JOBS, PLACES } from './simulation/content.ts';
import { price } from './simulation/economy.ts';
import { activePlayer, clothingStock, learning, scores } from './simulation/selectors.ts';
import { encodeBrowserSave, decodeBrowserSave } from './browser-save.ts';
import type { View } from './browser-save.ts';
import type { Action, GameState, ItemId, JobId, Mode, PlaceId } from './simulation/types.ts';
import townArt from '../artifacts/planning/concepts/town-fifteen-v2.png';

const SAVE_KEY = 'jones-fasterlane-prototype-0.1';
const money = (n: number) => `$${n.toLocaleString('en-US')}`;
const modeNames: Record<Mode, string> = { walk: 'Walk', bike: 'Bike', bus: 'Town bus', car: 'Car' };
function initialSave(): { game: GameState | null; view: View; error: string } {
  try { const raw = localStorage.getItem(SAVE_KEY); const saved = raw ? decodeBrowserSave(raw) : null; if (saved && saved.game.players.length !== 1) throw new Error('Solo preview only.'); return { game: saved?.game ?? null, view: saved?.view ?? { route: 'town', tab: 'actions' }, error: '' }; }
  catch { return { game: null, view: { route: 'town', tab: 'actions' }, error: 'The saved game could not be read. It has been kept; you can start a new game or import a valid save.' }; }
}
function Modal({ title, children, close, wide = false }: { title: string; children: ReactNode; close: () => void; wide?: boolean }) {
  const ref = useRef<HTMLDialogElement>(null);
  useEffect(() => { const el = ref.current; el?.showModal(); return () => el?.close(); }, []);
  return <dialog ref={ref} className={`modal ${wide ? 'wide' : ''}`} aria-label={title} onCancel={e => { e.preventDefault(); close(); }}>
    <div className="modal-head"><h2>{title}</h2><button className="secondary" onClick={close} aria-label={`Close ${title}`}>Close</button></div>{children}
  </dialog>;
}

export default function App() {
  const [checkpoint] = useState(initialSave);
  const [game, setGame] = useState<GameState | null>(null);
  const [resume, setResume] = useState<GameState | null>(checkpoint.game);
  const [resumeView, setResumeView] = useState<View>(checkpoint.view);
  const [exportText, setExportText] = useState('');
  const [name, setName] = useState('Maya');
  const [error, setError] = useState(checkpoint.error);
  const [route, setRoute] = useState<'town' | 'visit'>('town');
  const [tab, setTab] = useState<View['tab']>('actions');
  const [modal, setModal] = useState<'goals' | 'stats' | 'menu' | 'export' | null>(null);
  const [destination, setDestination] = useState<PlaceId | null>(null);
  const [mode, setMode] = useState<Mode>('walk');
  const [lastMode, setLastMode] = useState<Mode>('walk');
  const [preview, setPreview] = useState<PlaceId | null>(null);
  const [saveStatus, setSaveStatus] = useState(checkpoint.game ? 'A saved game is ready.' : 'Your game stays on this browser.');
  const importInput = useRef<HTMLInputElement>(null);
  const generation = useRef(0);

  useEffect(() => {
    if (!game) return;
    if (game.notices.length) { setSaveStatus('Previous checkpoint kept until these notices finish.'); return; }
    try { const raw = encodeBrowserSave(game, { route, tab }); localStorage.setItem(SAVE_KEY, raw); setResume(game); setResumeView({ route, tab }); setSaveStatus('Saved on this browser.'); }
    catch { setSaveStatus('Could not save on this browser. Use Export save in the menu.'); }
  }, [game, route, tab]);

  function send(action: Action) {
    if (!game) return;
    const id = game.sequence + 1;
    setGame(current => current ? dispatch(current, { id, action }).state : current);
  }
  function start() {
    if ((resume || checkpoint.error) && !window.confirm('Replace the current saved game with a new one?')) return;
    try {
      const seed = crypto.getRandomValues(new Uint32Array(1))[0]!;
      const next = createGame({ seed, names: [name.trim() || 'Maya'] });
      generation.current++; setGame(next); setError(''); setRoute('town'); setTab('actions'); setModal(null);
    } catch (e) { setError((e as Error).message); }
  }
  function selectPlace(id: PlaceId) {
    const place = PLACES.find(v => v.id === id)!;
    if (!place.active) { setPreview(id); return; }
    if (game && activePlayer(game).place === id) { setRoute('visit'); setTab('actions'); return; }
    setDestination(id); setMode(game && quoteTrip(game, id, lastMode).available ? lastMode : 'walk');
  }
  function travel() {
    if (!game || !destination) return;
    const result = dispatch(game, { id: game.sequence + 1, action: { type: 'travel', destination, mode } });
    setGame(current => current?.sequence === game.sequence ? result.state : current);
    if (result.accepted) { setRoute('visit'); setLastMode(mode); setTab('actions'); }
    setDestination(null);
  }
  function showExport() {
    if (!game) return;
    try { setExportText(encodeBrowserSave(game, { route, tab })); setModal('export'); } catch (e) { setError((e as Error).message); }
  }
  function downloadSave() {
    if (!game) return;
    try {
      const url = URL.createObjectURL(new Blob([encodeBrowserSave(game, { route, tab })], { type: 'application/json' }));
      const link = document.createElement('a'); link.href = url; link.download = 'jones-fasterlane-save.json'; document.body.append(link); link.click(); link.remove();
      setTimeout(() => URL.revokeObjectURL(url), 1000); setError('');
    } catch (e) { setError((e as Error).message); }
  }
  async function loadFile(file?: File) {
    if (!file) return;
    const generationAtRead = generation.current;
    try {
      if (file.size > 1_048_576) throw new Error('This file is larger than the supported save size.');
      const saved = decodeBrowserSave(await file.text());
      const candidate = saved.game;
      if (candidate.players.length !== 1) throw new Error('This interface currently loads solo games only.');
      if ((game || resume || generation.current !== generationAtRead) && !window.confirm('Replace the current game with this validated save?')) return;
      generation.current++; setGame(candidate); setRoute(saved.view.route); setTab(saved.view.tab); setModal(null); setError('');
    } catch (e) { setError((e as Error).message); }
    if (importInput.current) importInput.current.value = '';
  }
  const fileInput = <input className="visually-hidden" ref={importInput} type="file" accept=".json,application/json" onChange={e => { void loadFile(e.currentTarget.files?.[0]); }} aria-label="Import a saved game" />;

  if (!game) return <main className="start-screen"><div className="start-card">
    <p className="eyebrow">A SMALL TOWN. SOME BIG PLANS.</p><h1>Jones in the<br/>Faster Lane</h1>
    <p>Find your feet. Find a job. Make a life.</p><img className="start-art" src={townArt} alt="Illustrated retro town with shops, homes and places to work"/>
    <label className="name-input">Your name<input value={name} maxLength={40} onChange={e => setName(e.target.value)} /></label>
    <div className="modal-actions"><button className="primary" onClick={start}>Start a new life</button>{resume && <button onClick={() => { generation.current++; setGame(resume); setRoute(resumeView.route); setTab(resumeView.tab); }}>Resume game</button>}<button className="secondary" onClick={() => importInput.current?.click()}>Import save</button></div>
    {error && <p className="error" role="alert">{error}</p>}<p className="save-note">Early solo prototype · Saves on this browser · No account needed</p>{fileInput}
  </div></main>;

  const week = game.week;
  const p = activePlayer(game), place = PLACES.find(v => v.id === p.place)!;
  const goalScores = scores(p);
  const cost = (base: number) => price(base, game.economy.goods.reading);
  const busy = game.notices.length > 0 || game.status === 'finished';
  const button = (label: string, detail: string, action: Action, disabled = false) => <button className="action-button" disabled={busy || disabled} onClick={() => send(action)}><strong>{label}</strong><small>{detail}</small></button>;
  function buy(id: ItemId) { const item = ITEMS[id]; return <div key={id}>{button(item.name, `${money(cost(item.base))}${item.stock ? ` · ${item.stock} stock` : ''}`, { type: 'buy', item: id }, p.cash < cost(item.base) || ((id === 'bike' || id === 'car' || id === 'fridge') && p.owns[id]))}</div>; }
  function jobs(local: boolean) {
    return <div className="job-list">{(Object.entries(JOBS) as [JobId, typeof JOBS[JobId]][]).filter(([, j]) => !local || j.place === p.place).map(([id, j]) => <article className="job-card" key={id}>
      <div className="job-meta"><h3>{j.name}</h3><strong>{money(cost(j.wage))} rate</strong></div>
      <p>{PLACES.find(v => v.id === j.place)!.name}{p.job === id ? ' · Your current job' : ''}</p>
      <p className="requirements">Experience {j.experience} · Work history {j.dependability === 10 ? 0 : j.dependability}{j.qualification ? ' · Trade School' : ' · No course required'}</p>
      {button(p.job === id ? 'Ask for a raise' : 'Apply', '4 time · An opening is not guaranteed', { type: 'apply', job: id }, p.time <= 0)}
    </article>)}</div>;
  }
  function visit() {
    const job = p.job ? JOBS[p.job] : null;
    const localJob = job?.place === p.place;
    return <>
      <div className="visit-head"><p className="location-kicker">YOU ARE AT</p><h2>{place.name}</h2><p className="clerk-line">{p.place === 'hospitality' ? '“We’re short staffed. The coffee isn’t.”' : p.place === 'civic' ? '“Helping you get somewhere. Please take a number.”' : p.place === 'college' ? '“A little learning opens a few doors.”' : p.place === 'tech' ? '“Useful things. Slightly less useful payment plans.”' : p.place === 'market' ? '“Fresh opportunities, aisle three.”' : p.place === 'clothes' ? '“Dress for the job you’ve actually got.”' : '“Home sweet reasonably priced home.”'}</p></div>
      {(p.place === 'civic' || p.place === 'market' || p.place === 'hospitality') && <div className="tabs"><button className={tab === 'actions' ? 'selected' : ''} onClick={() => setTab('actions')}>{p.place === 'civic' ? 'Rent counter' : 'Work & shop'}</button><button className={tab === 'jobs' ? 'selected' : ''} onClick={() => setTab('jobs')}>Public jobs</button></div>}
      {tab === 'jobs' ? jobs(p.place !== 'civic') : <div className="actions">
        {localJob && <><p className="section-label">YOUR JOB · {job.name}</p>{button('Work a shift', `${Math.min(6, p.time)} time · ${money(Math.trunc(8 * p.wage * Math.min(6, p.time) / 6))} gross${p.rentDebt ? ' before garnishment' : ''}`, { type: 'work' }, p.time <= 0 || clothingStock(p) === 0)}</>}
        {p.place === 'home' && <>{button('Put your feet up', '6 time · First rest each turn: +2 Happiness', { type: 'relax' }, p.time <= 0)}<p className="section-label">YOUR POSSESSIONS</p><p>{Object.entries(p.owns).filter(([, v]) => v).map(([k]) => k).join(' · ') || 'Room for a few useful things.'}</p></>}
        {p.place === 'civic' && <><p className="hint">Stored rent: {money(p.rentContract)} · Prepaid stock: {p.rentStock} · Arrears: {money(p.rentDebt)}</p>{week % 4 === 0 || p.rentOpen ? <>{button('Pay current rent', `${money(p.rentContract)} · Buys the remainder of this rent period`, { type: 'payRent' }, p.cash < p.rentContract)}{button('Ask for an extension', 'No rent stock granted · One request per turn', { type: 'extendRent' }, p.rentStock > 0 || p.extensionAttempt !== 0)}{p.rentDebt > 0 && button('Clear rent arrears', money(p.rentDebt), { type: 'payArrears' }, p.cash < p.rentDebt)}</> : <p className="empty">The rent counter opens every fourth week. Public jobs are open now.</p>}</>}
        {p.place === 'hospitality' && <>{!p.job && <p className="hint">Start with Public jobs. Cook is the dependable fallback.</p>}{buy('hamburger')}{buy('cheeseburger')}</>}
        {p.place === 'market' && <>{!p.owns.fridge && <p className="hint">Groceries spoil at the next turn without a fridge. A meal from Hospitality covers the turn without storage.</p>}{buy('groceries1')}{buy('groceries2')}{buy('groceries4')}</>}
        {p.place === 'college' && <><h3>Trade School</h3><p>Opens the Butcher qualification. Experience and work history still matter.</p><p className="hint">{p.qualifications.length ? 'Completed · +10 Learning earned' : `${p.lessons}/10 lessons complete`}</p>{!p.qualifications.length && (p.enrolled ? button('Attend a lesson', '6 time · One lesson step', { type: 'study' }, p.time <= 0) : button('Enroll in Trade School', `${money(cost(50))} once · No lesson fee`, { type: 'enroll' }, p.cash < cost(50)))}</>}
        {p.place === 'tech' && <>{buy('bike')}{buy('car')}{buy('fridge')}<p className="hint">Bike: no fares. Car: faster trips, with operating costs. Fridge: stores groceries.</p></>}
        {p.place === 'clothes' && <>{buy('casual')}{buy('dress')}{buy('suit')}<p className="hint">All jobs in this prototype accept casual clothes. Better grades are optional.</p></>}
      </div>}
      <button className="secondary" onClick={() => setRoute('town')}>Back to town · no time cost</button>
    </>;
  }

  return <main className="app-shell">
    <header className="masthead"><div><p className="eyebrow">A SMALL TOWN. SOME BIG PLANS.</p><h1>Jones in the Faster Lane</h1></div><span className="prototype-badge">EARLY PROTOTYPE</span></header>
    <div className="toolbar"><div className="stat"><small>PLAYER</small><strong>{p.name}</strong></div><div className="stat"><small>WEEK</small><strong>{game.week}</strong></div><div className="stat"><small>TIME LEFT</small><strong>{p.time} / 60</strong></div><div className="stat"><small>CASH</small><strong>{money(p.cash)}</strong></div><div className="stat"><small>YOUR JOB</small><strong>{p.job ? JOBS[p.job].name : 'Looking for work'}</strong></div><button className="secondary" onClick={() => setModal('menu')} disabled={busy}>Menu</button></div>
    <section className="goals-strip" aria-label="Your goals">{(Object.keys(goalScores) as (keyof typeof goalScores)[]).map(k => <button className="goal" key={k} onClick={() => setModal('goals')} disabled={busy}><span>{k[0]!.toUpperCase() + k.slice(1)} <strong>{goalScores[k]} / {p.goals[k]}</strong></span><span className="goal-track"><i style={{ width: `${Math.min(100, 100 * goalScores[k] / p.goals[k])}%` }}/></span></button>)}</section>
    <div className="layout"><section className="town-panel" aria-label="Town destinations"><div className="town-art"><img src={townArt} alt="Illustrated small town"/><div className="map-caption"><span className="eyebrow">WELCOME TO THE NEIGHBOURHOOD</span><h2>Your next move?</h2><p>Seven places open. Choose a stop below.</p></div></div><div className="destinations">{PLACES.map((v, i) => <button className={`destination ${v.id === p.place ? 'active-place' : ''} ${!v.active ? 'preview' : ''}`} key={v.id} onClick={() => selectPlace(v.id)} disabled={busy}><span className="stop-number">{i + 1}</span><span className="place-label">{v.name}<small>{v.id === p.place ? 'You are here · reopen free' : v.active ? 'Visit' : 'Preview only'}</small></span></button>)}</div></section>
      <aside className="visit-panel" aria-label="Current location">{route === 'visit' ? visit() : <><p className="location-kicker">MAKE A LITTLE PROGRESS</p><h2>Every turn counts.</h2><p>You’re at <strong>{place.name}</strong>.</p><p className="clerk-line">Work pays the bills. Learning opens doors. Leave a little time to enjoy yourself.</p><div className="actions"><button className="primary" onClick={() => { setRoute('visit'); setTab('actions'); }} disabled={busy}>Open {place.name}</button><button className="secondary" onClick={() => setModal('stats')} disabled={busy}>Check your situation</button></div><p className="hint">Get hired at Civic House or a local job board. Work at the employer. Spend time and money deliberately.</p></>}</aside>
    </div>
    <footer className="footer-controls"><div><p className="status-line">{saveStatus}</p><small>Prototype rules and prices will change as we play.</small></div><div className="modal-actions"><button className="secondary" onClick={() => setModal('stats')} disabled={busy}>Statistics</button><button className="primary" disabled={busy} onClick={() => { send({ type: 'endTurn' }); setRoute('town'); setTab('actions'); }}>End turn</button></div></footer>
    {error && <p className="error" role="alert">{error}</p>}{fileInput}
    {game.notices.length > 0 ? <Modal title={game.status === 'finished' ? 'You made it!' : 'Town news'} close={() => send({ type: 'acknowledge' })}><div className="notice-card"><p>{game.notices[0]}</p><button className="primary" autoFocus onClick={() => send({ type: 'acknowledge' })}>Continue</button></div></Modal>
      : modal === 'export' ? <Modal title="Export your game" close={() => setModal(null)}><p>Download a portable copy, or select and copy the save text if downloads aren’t supported here.</p><textarea className="save-text" aria-label="Portable save JSON" readOnly value={exportText}/><button className="primary" onClick={downloadSave}>Download JSON</button></Modal>
      : game.status === 'finished' ? <Modal title="A life well made" close={() => { setGame(null); }}><p>You reached all four goals in week {game.week}. Nice work, {p.name}.</p><div className="modal-actions"><button className="primary" onClick={() => { setGame(null); }}>Back to start</button><button onClick={showExport}>Export this game</button></div></Modal>
      : destination ? <Modal title={`Travel to ${PLACES.find(v => v.id === destination)!.name}`} close={() => setDestination(null)}><p>Compare the whole journey, including entry.</p><div className="mode-list">{(['walk', 'bike', 'bus', 'car'] as Mode[]).map(m => { const q = quoteTrip(game, destination, m); return <button key={m} className={`mode ${mode === m ? 'chosen' : ''}`} disabled={!q.available} aria-pressed={mode === m} onClick={() => setMode(m)}><strong>{modeNames[m]}</strong><small>{q.travelTime + q.entryTime} time · {money(q.cash)}</small><small>{q.available ? `Arrive with ${p.time - q.travelTime - q.entryTime} time${m === 'car' && !p.carPaid ? ' · includes operating package' : ''}` : q.message}</small></button>; })}</div><div className="modal-actions"><button className="primary" onClick={travel} disabled={!quoteTrip(game, destination, mode).available}>Confirm journey</button><button className="secondary" onClick={() => setDestination(null)}>Cancel</button></div></Modal>
      : preview ? <Modal title={PLACES.find(v => v.id === preview)!.name} close={() => setPreview(null)}><p>This part of town is planned for a later version. No journey, time or money spent.</p><p>For now, try work, Trade School, transport and the seven open places.</p></Modal>
      : modal === 'goals' ? <Modal title="Your four goals" close={() => setModal(null)}><p>Meet every target, then reach the next incoming finish check.</p><dl className="inventory"><dt>Wealth · {goalScores.wealth}/{p.goals.wealth}</dt><dd>Cash minus rent arrears. Possessions help you live; they aren’t spendable cash.</dd><dt>Happiness · {p.happiness}/{p.goals.happiness}</dt><dd>Enjoy life as well as work. Rest, some purchases and achievements help.</dd><dt>Career · {goalScores.career}/{p.goals.career}</dt><dd>Current standing at work. It can fall after missed work or unemployment.</dd><dt>Learning · {learning(p)}/{p.goals.learning}</dt><dd>Work: {Math.floor(p.workTime / 12)} points. Qualifications: {p.qualifications.length * 10} points. Next work point in {12 - p.workTime % 12} time.</dd></dl></Modal>
      : modal === 'stats' ? <Modal title="Your situation" close={() => setModal(null)}><dl className="inventory"><dt>Work</dt><dd>{p.job ? JOBS[p.job].name : 'Unemployed'} · Experience {p.experience} · Work history {p.dependability}</dd><dt>Food</dt><dd>{p.meal ? 'Meal ready for next turn' : 'No meal ready'} · Groceries {p.groceries} · {p.owns.fridge ? 'Fridge owned' : 'No fridge'}</dd><dt>Clothes</dt><dd>Casual {p.clothes.casual} · Smart {p.clothes.dress} · Suit {p.clothes.suit}</dd><dt>Housing</dt><dd>Prepaid stock {p.rentStock} · Contract {money(p.rentContract)} · Arrears {money(p.rentDebt)}</dd><dt>Learning</dt><dd>{p.workTime} time worked · Trade School {p.lessons}/10 lessons</dd><dt>Possessions</dt><dd>{Object.entries(p.owns).filter(([, v]) => v).map(([k]) => k).join(', ') || 'None yet'}</dd></dl></Modal>
      : modal === 'menu' ? <Modal title="Take a breather" close={() => setModal(null)}><div className="actions"><button onClick={showExport}>Export save</button><button onClick={() => importInput.current?.click()}>Import save</button><button onClick={() => { setModal(null); setGame(null); }}>Back to start</button></div><p className="save-note">{saveStatus}</p>{error && <p className="error" role="alert">{error}</p>}<p>One current game per browser. Export a copy before starting another.</p></Modal> : null}
  </main>;
}
