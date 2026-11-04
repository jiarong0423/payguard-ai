// (r31 J4 P1-1 A2) "Session resumed" names only what the resumed server state really holds. After Reset demo and a
// reload the session is empty, and the old fixed text still said "loaded samples and dispute drafts are back" over
// an empty page. Nothing held -> null, and the console shows no message at all.
const counted = (count, word) => `${count} ${word}${count === 1 ? '' : 's'}`;

export function resumedNotice(state, drafts = []) {
  const parts = [];
  if (state?.transactions?.length) parts.push({ text: 'sample sales', plural: true });
  const cases = state?.disputes?.length || 0;
  if (cases) parts.push({ text: counted(cases, 'dispute case'), plural: cases !== 1 });
  const prepared = Array.isArray(drafts) ? drafts.length : 0;
  if (prepared) parts.push({ text: counted(prepared, 'evidence draft'), plural: prepared !== 1 });
  const reviewed = (state?.disputes || []).filter((row) => row.status === 'local_draft_reviewed').length;
  if (reviewed) parts.push({ text: counted(reviewed, 'recorded local review'), plural: reviewed !== 1 });
  if (!parts.length) return null;
  const words = parts.map((part) => part.text);
  const list = words.length === 1 ? words[0] : `${words.slice(0, -1).join(', ')} and ${words[words.length - 1]}`;
  const verb = parts.length === 1 && !parts[0].plural ? 'is' : 'are';
  return `Session resumed: ${list} ${verb} back. Policy and country check results are not kept; run them again.`;
}
