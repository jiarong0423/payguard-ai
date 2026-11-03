// AG Grid for every console grid, loaded on demand (spec D13). Importing this module registers the one
// community module list the console uses (instead of AllCommunityModule), so the entry chunk carries no
// AG Grid code. App.jsx loads the default export with lazy(); TimeEvidenceView, GuideLive, GuideReplay and
// AnalyticsDashboard import the named exports from here so the registration always happens first.
import { useMemo } from 'react';
import { AgGridReact as BaseGrid } from 'ag-grid-react';
import {
  CellStyleModule,
  ClientSideRowModelModule,
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
import { gridParams } from '../theme/chartTheme.js';

export const GRID_MODULES = [
  ClientSideRowModelModule, // rowData
  TextFilterModule, NumberFilterModule, DateFilterModule, // `filter: true` / floating filters by column type
  QuickFilterModule, // quickFilterText
  RowStyleModule, // getRowClass
  CellStyleModule, // cellClass
  TooltipModule, // headerTooltip
  RowAutoHeightModule, // autoHeight cells
  CsvExportModule, // GuideReplay's "Download CSV" (exportDataAsCsv); without it the call does nothing
  RowApiModule, // GuideReplay's shown-row count (getDisplayedRowCount); without it AG Grid logs error #200
];
ModuleRegistry.registerModules(GRID_MODULES);

export { BaseGrid as AgGridReact, themeQuartz };

// The console's token-based Quartz theme (theme/chartTheme.js gridParams()).
export const consoleGridTheme = (options) => themeQuartz.withParams(gridParams(options));

// Default export for App.jsx's lazy() load: same props as AgGridReact, except that
// `theme` may also be a plain params object, which becomes a Quartz theme here (so callers never import AG).
export default function LazyGrid({ theme, ...props }) {
  const resolved = useMemo(() => (theme && typeof theme === 'object' && typeof theme.withParams !== 'function'
    ? themeQuartz.withParams(theme) : theme), [theme]);
  return <BaseGrid theme={resolved} {...props} />;
}
