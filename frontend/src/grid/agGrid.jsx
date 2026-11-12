// AG Grid for every console grid, loaded on demand (spec D13). Importing this module registers the one
// community module list the console uses (instead of AllCommunityModule), so the entry chunk carries no
// AG Grid code. App.jsx loads the default export with lazy(); TimeEvidenceView, GuideLive, GuideReplay and
// AnalyticsDashboard import the named exports from here so the registration always happens first.
import { useEffect, useMemo, useState } from 'react';
import { AgGridReact as BaseGrid } from 'ag-grid-react';
import {
  CellStyleModule,
  ClientSideRowModelApiModule,
  ClientSideRowModelModule,
  ColumnApiModule,
  CsvExportModule,
  DateFilterModule,
  ModuleRegistry,
  NumberFilterModule,
  QuickFilterModule,
  RowApiModule,
  RowAutoHeightModule,
  RowStyleModule,
  TextFilterModule,
  TooltipModule,
  themeQuartz,
} from 'ag-grid-community';
import { GRID_FLOATING_FILTERS_HEIGHT, gridParams } from '../theme/chartTheme.js';
import { layout } from '../theme/tokens.js';
import './agGrid.css';

export const GRID_MODULES = [
  ClientSideRowModelModule, // rowData
  TextFilterModule, NumberFilterModule, DateFilterModule, // `filter: true` / floating filters by column type
  QuickFilterModule, // quickFilterText
  RowStyleModule, // getRowClass / rowClassRules
  CellStyleModule, // cellClass
  TooltipModule, // headerTooltip
  RowAutoHeightModule, // autoHeight cells
  CsvExportModule, // GuideReplay's "Download CSV" (exportDataAsCsv); without it the call does nothing
  RowApiModule, // GuideReplay's shown-row count (getDisplayedRowCount); without it AG Grid logs error #200
  ClientSideRowModelApiModule, // GuideReplay's phone cards list the filtered rows (forEachNodeAfterFilterAndSort)
  ColumnApiModule, // narrow grids hide a column (setColumnsVisible, AG Grid grid-size); without it AG Grid logs error #200
];
ModuleRegistry.registerModules(GRID_MODULES);

export { themeQuartz, GRID_FLOATING_FILTERS_HEIGHT };

// The console's token-based Quartz theme (theme/chartTheme.js gridParams()); one desktop and one phone instance.
export const consoleGridTheme = (options) => themeQuartz.withParams(gridParams(options));
const CONSOLE_THEME = consoleGridTheme();
const CONSOLE_THEME_PHONE = consoleGridTheme({ phone: true });
const COMPACT_THEME = consoleGridTheme({ compact: true });
const COMPACT_THEME_PHONE = consoleGridTheme({ phone: true, compact: true });
const PHONE_QUERY = `(max-width: ${layout.phone}px)`;

function usePhoneTheme(compact) {
  const [phone, setPhone] = useState(() => typeof window !== 'undefined' && Boolean(window.matchMedia?.(PHONE_QUERY).matches));
  useEffect(() => {
    const query = window.matchMedia?.(PHONE_QUERY);
    if (!query) return undefined;
    const update = () => setPhone(query.matches);
    query.addEventListener('change', update);
    return () => query.removeEventListener('change', update);
  }, []);
  if (compact) return phone ? COMPACT_THEME_PHONE : COMPACT_THEME;
  return phone ? CONSOLE_THEME_PHONE : CONSOLE_THEME;
}

// (F2 2026-11-12, OFFICIAL_FIX_GUIDE s2, AG Grid "theming": themeCssLayer) Every console grid writes its CSS into
// @layer grid, inserted into document.body; index.css declares the layer order (resets before grid), so the console's
// form defaults never reach AG Grid's own inputs, and unlayered console CSS still wins over the grid.
// `theme` may be omitted (console theme), a Quartz theme, or a plain params object merged over the console params;
// `compact` sets the cells at the meta size (14) instead of the grid-cell size (16).
export function AgGridReact({ theme, compact = false, ref, ...props }) {
  const fallback = usePhoneTheme(compact);
  const resolved = useMemo(() => {
    if (!theme) return fallback;
    if (typeof theme === 'object' && typeof theme.withParams !== 'function') return fallback.withParams(theme);
    return theme;
  }, [theme, fallback]);
  return <BaseGrid ref={ref} theme={resolved} themeCssLayer="grid"
    themeStyleContainer={typeof document !== 'undefined' ? document.body : undefined} {...props} />;
}

// Default export for App.jsx's lazy() load: the same wrapper.
export default AgGridReact;
