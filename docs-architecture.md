# Architecture of HyperNesting

This document describes the updated architecture and file structure of the HyperNesting application.

## High-Level Structure

```
hypernesting/
├── main.py                   # Application entry point
├── config/
│   └── settings.json         # User-configurable settings
├── ui/                       # User interface components
│   ├── components.py         # MainWindow, menu, common dialogs
│   ├── parts_tab.py          # CAD import and part management
│   ├── sheets_tab.py         # Sheet and remnant management
│   ├── nesting_tab.py        # Nesting configuration and preview
│   └── export_tab.py         # Export and reporting interface
├── core/                     # Core logic and algorithms
│   ├── cad_importer.py       # DXF/DWG import to geometries
│   ├── genetic_algorithm.py  # Configurable genetic algorithm
│   └── nesting_engine.py     # High-level nesting orchestration
├── reports/                  # Report generation logic
│   ├── summary_report.py     # CSV/text summary output
│   └── detailed_report.py    # CSV/text detailed output
├── resources/
│   └── icons/                # QtAwesome icons and assets
├── tests/                    # Pytest unit and integration tests
│   ├── test_parts.py
│   ├── test_sheets.py
│   ├── test_nesting.py
│   └── test_export.py
├── docs/
│   └── architecture.md       # This document
└── requirements.txt          # Python dependencies
```

## Component Interactions

- **main.py** loads settings and initializes `MainWindow` from `ui/components.py`.
- **MainWindow** creates four tabs (`PartsTab`, `SheetsTab`, `NestingTab`, `ExportTab`) passing shared settings.
- **PartsTab** uses `core/cad_importer` to load geometries from DXF/DWG files.
- **SheetsTab** allows defining sheet parameters and quantities.
- **NestingTab** orchestrates nesting via `core/nesting_engine` which employs `core/genetic_algorithm`.
- **ExportTab** invokes report generation in `reports/summary_report` and `reports/detailed_report`, and DXF export logic.
- **Tests** validate import, UI dialogs, algorithm, and report generators.

## Data Flow

1. User imports CAD files in **PartsTab** → geometries loaded.
2. User defines sheets in **SheetsTab** → sheets list created.
3. User configures spacing and strategy in **NestingTab** → `NestingEngine.nest()` returns best layout.
4. Results displayed in **NestingTab**, saved backgrounds.
5. User exports via **ExportTab** → reports generated and DXF files saved.

This modular architecture ensures separation of concerns, testability, and ease of extension.
