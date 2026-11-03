// Wrapper for the dispute stage: the existing time evidence view, then the optional
// Bryntum timeline. Without @bryntum/scheduler-community installed, OptionalTimeline
// renders nothing, so the output is exactly <TimeEvidenceView />.
import TimeEvidenceView from '../TimeEvidenceView.jsx';
import OptionalTimeline from './OptionalTimeline.jsx';

export default function TimeEvidenceWithTimeline({ evidence }) {
  if (!evidence || !Array.isArray(evidence.events)) return null;
  return (
    <>
      <TimeEvidenceView evidence={evidence} />
      <OptionalTimeline evidence={evidence} />
    </>
  );
}
