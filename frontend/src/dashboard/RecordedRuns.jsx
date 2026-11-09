// Hosted dashboard: the recorded live Studio runs as one-click "Replay" buttons. Pressing one shows the recorded tool calls
// step by step (agent, tool, recorded milliseconds) and then the recorded answer. Nothing here calls a model or the network;
// it only plays back the committed recording (frontend/src/data/studio_agent_run_v1.json).
import { useEffect, useRef, useState } from 'react';
import { REPLAY_BADGE, recordingLabel, replaySchedule } from './agentRecording.js';
import { plainSummary } from './auditor.js';

export default function RecordedRuns({ recording }) {
  const [active, setActive] = useState(-1);
  const [shown, setShown] = useState(0);
  const timers = useRef([]);
  const stop = () => { timers.current.forEach((id) => window.clearTimeout(id)); timers.current = []; };
  useEffect(() => stop, []);
  if (!recording?.runs?.length) return null;
  const play = (index) => {
    stop();
    const schedule = replaySchedule(recording.runs[index]);
    setActive(index);
    const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    if (reduced) { setShown(schedule.length); return; }
    setShown(0);
    schedule.forEach((step) => timers.current.push(window.setTimeout(() => setShown(step.index + 1), step.at)));
  };
  const run = active >= 0 ? recording.runs[active] : null;
  const schedule = run ? replaySchedule(run) : [];
  const done = run && shown >= schedule.length;
  return <section className="pg-replay" aria-labelledby="pg-replay-title" data-testid="recorded-runs">
    <h2 id="pg-replay-title">Replay a recorded Studio run</h2>
    <p className="pg-replay-note"><strong>{recordingLabel(recording)}</strong></p>
    <div className="pg-replay-buttons" role="group" aria-label="Recorded questions">
      {recording.runs.map((entry, index) => <button key={entry.question} type="button" aria-pressed={active === index} data-testid={`replay-run-${index}`} onClick={() => play(index)}>Replay: {entry.question}</button>)}
    </div>
    <div className="pg-replay-out" role="status" aria-live="polite" data-testid="replay-output">
      {run && <>
        <ol className="pg-replay-steps" data-testid="replay-steps">
          {schedule.slice(0, shown).map((step) => <li key={step.index}><code>{step.tool}</code> <span>{step.agent} agent{Number.isFinite(step.ms) ? `, ${step.ms} ms` : ''}{step.ok ? '' : ', did not finish'}</span></li>)}
        </ol>
        {!done && <p className="pg-replay-wait">Step {shown} of {schedule.length}</p>}
        {done && <p className="pg-replay-answer" data-testid="replay-answer"><strong>Answer then:</strong> {plainSummary(run.reply)} <span className="pg-replay-badge">{REPLAY_BADGE}</span> <span>{run.turns} turn{run.turns === 1 ? '' : 's'}, {(run.duration_ms / 1000).toFixed(1)} s in total.</span></p>}
      </>}
    </div>
  </section>;
}
