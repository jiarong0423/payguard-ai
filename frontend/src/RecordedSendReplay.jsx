// Hosted demo only: lets a reviewer click through the real send as it happened at 2026-11-04 17:16 UTC (2026-11-05 in UTC+8), without sending anything.
// It shows the same two steps the console asks for (tick, Continue, wait three seconds, Send) and then the receipt of
// the real Sandbox send, text only, from proof_facts_v1.json. It calls nothing: no fetch, no API, no session, and it
// never reaches the evidence route, which the hosted demo keeps closed.
import { useEffect, useRef, useState } from 'react';
import facts from './data/proof_facts_v1.json';
import './RecordedSendReplay.css';

export const REPLAY_WAIT_SECONDS = 3;

export default function RecordedSendReplay() {
  const send = facts.recorded_send;
  const [phase, setPhase] = useState('idle'); // idle | confirm | waiting | ready | done
  const [ticked, setTicked] = useState(false);
  const [left, setLeft] = useState(REPLAY_WAIT_SECONDS);
  const timer = useRef(null);
  useEffect(() => () => { if (timer.current) window.clearInterval(timer.current); }, []);
  if (!send) return null;

  const reset = () => { if (timer.current) window.clearInterval(timer.current); setPhase('idle'); setTicked(false); setLeft(REPLAY_WAIT_SECONDS); };
  const next = () => {
    setPhase('waiting');
    setLeft(REPLAY_WAIT_SECONDS);
    timer.current = window.setInterval(() => {
      setLeft((value) => {
        if (value <= 1) { window.clearInterval(timer.current); timer.current = null; setPhase('ready'); return 0; }
        return value - 1;
      });
    }, 1000);
  };

  return <section className="recorded-replay tg-block" data-testid="recorded-replay" aria-labelledby="recorded-replay-title">
    <h4 id="recorded-replay-title">Try the send: a recorded replay <span className="recorded-replay-chip" data-testid="recorded-replay-chip">Recorded, nothing is sent</span></h4>
    <p className="recorded-replay-note">Nothing on this page sends anything to PayPal. This walks through the same two steps the local console asks for, then shows what the real Sandbox send recorded at 2026-11-04 17:16 UTC (2026-11-05 in UTC+8). Press the buttons: nothing leaves this page.</p>
    {phase === 'idle' && <button type="button" className="recorded-replay-button" data-testid="recorded-replay-start" onClick={() => setPhase('confirm')}>Start the replay</button>}
    {(phase === 'confirm' || phase === 'waiting' || phase === 'ready') && <div className="recorded-replay-dialog" role="group" aria-label="Replay of the two-step send">
      <label className="recorded-replay-tick"><input type="checkbox" data-testid="recorded-replay-tick" checked={ticked} disabled={phase !== 'confirm'} onChange={(event) => setTicked(event.target.checked)} />
        I reviewed the draft and the request (replay)</label>
      {phase === 'confirm' && <button type="button" className="recorded-replay-button" data-testid="recorded-replay-continue" disabled={!ticked} onClick={next}>Continue</button>}
      {phase === 'waiting' && <button type="button" className="recorded-replay-button" data-testid="recorded-replay-wait" disabled>Send in {left}</button>}
      {phase === 'ready' && <button type="button" className="recorded-replay-send" data-testid="recorded-replay-send" onClick={() => setPhase('done')}>Send (replay)</button>}
      <button type="button" className="recorded-replay-link" onClick={reset}>Cancel</button>
    </div>}
    {phase === 'done' && <div className="recorded-replay-result" data-testid="recorded-replay-result" role="status">
      <p className="recorded-replay-stamp"><strong>Replay of a recorded real send.</strong> Nothing was sent just now.</p>
      <ol className="recorded-replay-steps">{send.steps.map((step) => <li key={step.at}><span className="recorded-replay-at">{step.at}</span><span>{step.what}</span></li>)}</ol>
      <p>{send.file_note}</p>
      <p>{send.limit}</p>
      <p className="recorded-replay-source">Source: <code>{send.receipt}</code>, masked as committed.</p>
      <button type="button" className="recorded-replay-link" onClick={reset}>Replay again</button>
    </div>}
  </section>;
}
