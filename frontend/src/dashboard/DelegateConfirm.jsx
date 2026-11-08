// Local live mode only: a question outside the auditor's own set would go to the AI model (paid, capped). Before it is sent,
// this small dialog asks once, in plain words; "Ask the AI" answers the auditor's question for the visitor, which is what
// typing "yes" does.
import { useEffect, useRef } from 'react';
import './DelegateConfirm.css';

const TEXTAREA = '.ag-studio-ai-assistant-textarea';
const SEND_BUTTON = '.ag-studio-ai-assistant-send-button';

// Types the confirmation word into the assistant's message box and presses its Send button, exactly as a visitor would.
export function answerYes(root = document) {
  const box = root.querySelector(TEXTAREA);
  const button = root.querySelector(SEND_BUTTON);
  if (!box || !button) return false;
  Object.getOwnPropertyDescriptor(window.HTMLTextAreaElement.prototype, 'value').set.call(box, 'yes');
  box.dispatchEvent(new Event('input', { bubbles: true }));
  window.setTimeout(() => button.click(), 0);
  return true;
}

export default function DelegateConfirm({ question, onCancel, onSend }) {
  const cancel = useRef(null);
  useEffect(() => {
    if (!question) return undefined;
    cancel.current?.focus();
    const onKey = (event) => { if (event.key === 'Escape') onCancel(); };
    window.addEventListener('keydown', onKey);
    return () => window.removeEventListener('keydown', onKey);
  }, [question, onCancel]);
  if (!question) return null;
  return <div className="pg-confirm-backdrop" data-testid="delegate-confirm-backdrop">
    <div className="pg-confirm" role="dialog" aria-modal="true" aria-labelledby="pg-confirm-title" data-testid="delegate-confirm">
      <h2 id="pg-confirm-title">Ask the AI helper?</h2>
      <p className="pg-confirm-question" data-testid="delegate-confirm-question">&ldquo;{question}&rdquo;</p>
      <p className="pg-confirm-note" data-testid="delegate-confirm-note">This question is outside the ready-made checks, so it goes to an AI model (Gemini). It uses a few paid calls, with 20 a day allowed on this console. It only reads the sample records and decides nothing.</p>
      <div className="pg-confirm-actions">
        <button type="button" ref={cancel} className="pg-confirm-cancel" data-testid="delegate-confirm-cancel" onClick={onCancel}>Cancel</button>
        <button type="button" className="pg-confirm-send" data-testid="delegate-confirm-send" onClick={onSend}>Ask the AI</button>
      </div>
    </div>
  </div>;
}
