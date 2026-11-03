// Optional Bryntum Scheduler view of the time evidence. It is compiled in only when
// the MIT Community package is installed locally (see ./vitePlugin.js);
// otherwise this component renders nothing and the ordered list stays the only view.
import { useEffect, useMemo, useRef, useState } from 'react';
import { buildTimelineModel } from './timelineModel.js';

// Replaced at build time by the Vite plugin. Without the plugin the flag is undefined.
const BUILT_WITH_BRYNTUM = typeof __PAYGUARD_BRYNTUM_TIMELINE__ !== 'undefined' && __PAYGUARD_BRYNTUM_TIMELINE__ === true;

const ROW_HEIGHT = 40;

function escapeHtml(value) {
  return String(value).replace(/[&<>"']/g, (char) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[char]);
}

function BryntumTimeline({ evidence }) {
  const hostRef = useRef(null);
  const [state, setState] = useState('loading');
  const model = useMemo(() => buildTimelineModel(evidence), [evidence]);

  useEffect(() => {
    if (!model || !hostRef.current) return undefined;
    setState('loading');
    let scheduler = null;
    let cancelled = false;
    import('virtual:payguard-optional-timeline')
      .then(({ Scheduler, available }) => {
        if (cancelled) return;
        if (!available || !Scheduler) { setState('unavailable'); return; }
        scheduler = new Scheduler({
          appendTo: hostRef.current,
          autoHeight: true,
          readOnly: true,
          // Fonts are bundled locally; never fetch a CDN fallback.
          detectCSSCompatibilityIssues: false,
          startDate: model.startDate,
          endDate: model.endDate,
          viewPreset: model.viewPreset,
          forceFit: true,
          rowHeight: ROW_HEIGHT,
          barMargin: 8,
          milestoneLayoutMode: 'estimate',
          milestoneTextPosition: 'outside',
          zoomOnMouseWheel: false,
          zoomOnTimeAxisDoubleClick: false,
          useInitialAnimation: false,
          columns: [{ text: 'Record', field: 'name', width: 140 }],
          resources: model.resources,
          events: model.events,
          features: {
            cellEdit: false,
            eventDrag: false,
            eventDragCreate: false,
            eventEdit: false,
            eventMenu: false,
            eventResize: false,
            scheduleMenu: false,
            eventTooltip: {
              template: ({ eventRecord }) => `<strong>${escapeHtml(eventRecord.name)}</strong><br>${escapeHtml(eventRecord.get('at'))}<br>${escapeHtml(eventRecord.get('source'))}`,
            },
          },
        });
        setState('ready');
      })
      .catch(() => { if (!cancelled) setState('unavailable'); });
    return () => {
      cancelled = true;
      if (scheduler && !scheduler.isDestroyed) scheduler.destroy();
    };
  }, [model]);

  if (!model || state === 'unavailable') return null;
  return (
    <figure className="time-timeline" data-testid="time-evidence-timeline" data-state={state}>
      <figcaption>Timeline view · axis in UTC · same records as the list above · Bryntum Scheduler Community (MIT)</figcaption>
      <div ref={hostRef} className="time-timeline-host" />
    </figure>
  );
}

export default function OptionalTimeline({ evidence }) {
  return BUILT_WITH_BRYNTUM ? <BryntumTimeline evidence={evidence} /> : null;
}
