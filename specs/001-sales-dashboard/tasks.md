# Tasks: ShopSmart Sales Analytics Dashboard

**Input**: Design documents from `specs/001-sales-dashboard/`
**Branch**: `001-sales-dashboard`
**Spec**: [spec.md](spec.md)
**Constitution**: [constitution.md](../../.specify/memory/constitution.md)

## Format: `[ID] [P?] [Story?] Description`

- **[P]**: Can run in parallel (different files, no blocking dependencies)
- **[Story]**: Which user story this task belongs to (US1–US5)
- File paths are exact — create files at the specified locations

## Tech Stack (from constitution)

- **Language**: Python 3.11+
- **UI**: Streamlit (latest stable)
- **Charts**: Plotly Express + Graph Objects overrides
- **Data**: Pandas
- **Deps**: uv only (`pip` / `poetry` prohibited)
- **Tests**: pytest; `tests/` mirrors source tree
- **Deploy**: Streamlit Community Cloud
- **Commit format**: `ECOM-N: description` (Jira traceability)

## Project Structure

```text
dashboard.py               ← layout orchestration only; no business logic
data/
├── __init__.py
├── loader.py              ← CSV load + DataLoadError; @st.cache_data
└── transforms.py          ← all aggregation functions
components/
├── __init__.py
├── kpi_cards.py           ← render_kpi_cards()
├── trend_chart.py         ← build_trend_chart()
├── category_chart.py      ← build_category_chart()
└── region_chart.py        ← build_region_chart()
tests/
├── conftest.py            ← shared sample DataFrame fixture
├── data/
│   ├── __init__.py
│   ├── test_loader.py
│   └── test_transforms.py
└── components/
    ├── __init__.py
    ├── test_kpi_cards.py
    ├── test_trend_chart.py
    ├── test_category_chart.py
    └── test_region_chart.py
pyproject.toml
uv.lock
data/
└── sales-data.csv         ← read-only; never modified at runtime
```

**Layer import rules** (constitution Principle IV):
- `data/` MUST NOT import from `components/` or `dashboard.py`
- `components/` MAY import from `data/`; MUST NOT import from `dashboard.py`
- `dashboard.py` MAY import from both layers

---

## Phase 1: Setup

**Purpose**: Project initialization — uv environment, directory structure, test infrastructure

- [X] T001 Run `uv init` in repo root, then `uv add streamlit plotly pandas` and `uv add --dev pytest` — commit `pyproject.toml` and `uv.lock` together (ECOM-1)
- [X] T002 [P] Create directory structure: `data/`, `components/`, `tests/data/`, `tests/components/` with `__init__.py` in each (ECOM-1)
- [X] T003 Add `[tool.pytest.ini_options]` section to `pyproject.toml` (testpaths = ["tests"]) and create `tests/conftest.py` with a shared `sample_df` pytest fixture containing at least 10 rows matching the sales CSV schema (date, order_id, product, category, region, quantity, unit_price, total_amount)

**Checkpoint**: `uv run pytest` runs and collects 0 tests without error

---

## Phase 2: Foundational — Data Loader

**Purpose**: `data/loader.py` is the single dependency blocking all user stories — must be complete before any story begins

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

### Tests (write first — confirm failing before T006)

- [ ] T004 [P] Write failing test: `load_sales_data()` with a valid CSV path returns a pandas DataFrame with the expected columns in `tests/data/test_loader.py`
- [ ] T005 [P] Write failing test: `load_sales_data()` with a missing file path raises `DataLoadError` in `tests/data/test_loader.py`

### Implementation (after T004 and T005 are confirmed failing)

- [ ] T006 Implement `DataLoadError(Exception)` custom exception and `load_sales_data(path: str) -> pd.DataFrame` decorated with `@st.cache_data` in `data/loader.py` — raises `DataLoadError` on missing file; returns raw DataFrame on success (depends on T004, T005)

**Checkpoint**: `uv run pytest tests/data/test_loader.py` — T004 and T005 pass; all other tests still at 0

---

## Phase 3: User Story 1 — View KPI Summary (Priority: P1) 🎯 MVP

**Goal**: Two labeled metric cards — Total Sales (currency) and Total Orders (integer) — render at the top of the dashboard from real CSV data.

**Independent Test**: Load dashboard with `sales-data.csv`; confirm two labeled cards appear at the top with values matching manual CSV calculations (~$672K and 482).

### Tests for US1 (write first — confirm failing before T009)

> **RED phase**: Run these tests and verify they FAIL before writing any implementation

- [ ] T007 [P] [US1] Write failing test: `get_kpi_metrics(df)` returns a dict with keys `total_sales` (float) and `total_orders` (int) matching known fixture values in `tests/data/test_transforms.py`
- [ ] T008 [P] [US1] Write failing test: `render_kpi_cards()` component returns/renders without error when called with valid total_sales and total_orders values in `tests/components/test_kpi_cards.py`

### Implementation for US1 (GREEN phase — after T007 and T008 confirmed failing)

- [ ] T009 [US1] Implement `get_kpi_metrics(df: pd.DataFrame) -> dict` in `data/transforms.py` — returns `{"total_sales": float, "total_orders": int}` (depends on T007)
- [ ] T010 [US1] Implement `render_kpi_cards(total_sales: float, total_orders: int) -> None` in `components/kpi_cards.py` — renders two Streamlit metric elements with labels "Total Sales" (formatted `$X,XXX`) and "Total Orders" (integer) (depends on T008, T009)
- [ ] T011 [US1] Create `dashboard.py` — import `load_sales_data`, `get_kpi_metrics`, `render_kpi_cards`; wrap data load in try/except (stub error display for now); call `render_kpi_cards()` at top of page (depends on T010)

**Checkpoint**: `uv run streamlit run dashboard.py` shows two KPI cards with correct values; `uv run pytest tests/data/test_transforms.py tests/components/test_kpi_cards.py` passes

---

## Phase 4: User Story 2 — Sales Trend Over Time (Priority: P2) 🎯 MVP

**Goal**: Line chart showing total sales aggregated by calendar month, with months in chronological order on x-axis and interactive hover tooltips.

**Independent Test**: Chart renders with 12 monthly data points in chronological order; hovering any point shows exact month and sales value.

### Tests for US2 (write first — confirm failing before T014)

> **RED phase**: Run these tests and verify they FAIL before writing any implementation

- [ ] T012 [P] [US2] Write failing test: `get_monthly_sales(df)` returns a DataFrame with columns `month` and `total_sales`, sorted chronologically, with correct aggregated values matching fixture data in `tests/data/test_transforms.py`
- [ ] T013 [P] [US2] Write failing component contract test: `build_trend_chart(df)` returns a `plotly.graph_objects.Figure` with exactly one trace of type `scatter` in `tests/components/test_trend_chart.py`

### Implementation for US2 (GREEN phase — after T012 and T013 confirmed failing)

- [ ] T014 [P] [US2] Implement `get_monthly_sales(df: pd.DataFrame) -> pd.DataFrame` in `data/transforms.py` — groups by calendar month, sums `total_amount`, sorts chronologically (depends on T012)
- [ ] T015 [US2] Implement `build_trend_chart(df: pd.DataFrame) -> go.Figure` in `components/trend_chart.py` — use Plotly Express `px.line` as base; apply Graph Objects `.update_layout()` for axis labels and `.update_traces()` for tooltip format showing month and sales value (depends on T013, T014)
- [ ] T016 [US2] Add trend chart section to `dashboard.py` below KPI cards — call `get_monthly_sales()` then `build_trend_chart()` and render with `st.plotly_chart()` (depends on T015)

**Checkpoint**: Dashboard shows KPI cards + trend line chart; `uv run pytest` passes all tests so far

---

## Phase 5: User Story 5 — Handle Data Errors Clearly (Priority: P5) 🎯 MVP

**Goal**: Missing, unreadable, or schema-invalid CSV shows a clear plain-language error message — no KPI cards or charts render.

**Independent Test**: Remove or corrupt `data/sales-data.csv`; dashboard displays descriptive error message with no charts or $0 values visible.

### Tests for US5 (write first — confirm failing before T019)

> **RED phase**: Run these tests and verify they FAIL before writing any implementation

- [ ] T017 [P] [US5] Write failing test: `load_sales_data()` with a CSV missing required columns raises `DataLoadError` with a descriptive message in `tests/data/test_loader.py`
- [ ] T018 [P] [US5] Write failing test: `load_sales_data()` with a CSV where `total_amount` contains all nulls raises `DataLoadError` in `tests/data/test_loader.py`

### Implementation for US5 (GREEN phase — after T017 and T018 confirmed failing)

- [ ] T019 [US5] Extend `data/loader.py` — after loading CSV, validate required columns exist and `total_amount` has at least one non-null value; raise `DataLoadError` with plain-language message on failure (depends on T017, T018)
- [ ] T020 [US5] Update `dashboard.py` try/except block — catch `DataLoadError` and render `st.error()` with the exception message; confirm no KPI cards, charts, or $0 values render when error is active (depends on T019)

**Checkpoint**: `uv run pytest` passes all tests; dashboard shows error message when CSV is removed; dashboard shows full content when CSV is present

---

## 🚀 MVP CHECKPOINT — Deploy after Phase 5

US1 (KPI cards) + US2 (trend chart) + US5 (error handling) are complete.

- [ ] T021 Deploy to Streamlit Community Cloud — connect GitHub repo, set main file to `dashboard.py`, verify public URL loads dashboard with correct KPI values and trend chart (ECOM-6)

---

## Phase 6: User Story 3 — Sales by Product Category (Priority: P3)

**Goal**: Bar chart showing total sales per category, sorted highest to lowest, with hover tooltips — in left column of two-column layout.

**Independent Test**: Chart renders with 5 category bars sorted descending; hovering any bar shows exact category name and sales total.

### Tests for US3 (write first — confirm failing before T023)

> **RED phase**: Run these tests and verify they FAIL before writing any implementation

- [ ] T022 [P] [US3] Write failing test: `get_category_sales(df)` returns a DataFrame with columns `category` and `total_sales`, sorted descending by `total_sales`, with correct values matching fixture data in `tests/data/test_transforms.py`
- [ ] T023 [P] [US3] Write failing component contract test: `build_category_chart(df)` returns a `plotly.graph_objects.Figure` with one bar trace and y-axis values sorted descending in `tests/components/test_category_chart.py`

### Implementation for US3 (GREEN phase — after T022 and T023 confirmed failing)

- [ ] T024 [P] [US3] Implement `get_category_sales(df: pd.DataFrame) -> pd.DataFrame` in `data/transforms.py` — groups by `category`, sums `total_amount`, sorts descending (depends on T022)
- [ ] T025 [US3] Implement `build_category_chart(df: pd.DataFrame) -> go.Figure` in `components/category_chart.py` — use `px.bar` as base; apply Graph Objects overrides for axis labels and tooltip showing category name and sales value (depends on T023, T024)
- [ ] T026 [US3] Add two-column layout to `dashboard.py` below trend chart — place category chart in left column using `st.columns(2)`; leave right column placeholder for US4 (depends on T025)

**Checkpoint**: Dashboard shows KPI cards + trend chart + category bar chart in left column; all tests pass

---

## Phase 7: User Story 4 — Sales by Region (Priority: P4)

**Goal**: Bar chart showing total sales per region, sorted highest to lowest, with hover tooltips — in right column alongside category chart. Follows same pattern established by US3.

**Independent Test**: Chart renders with 4 region bars sorted descending; hovering any bar shows exact region name and sales total.

### Tests for US4 (write first — confirm failing before T028)

> **RED phase**: Run these tests and verify they FAIL before writing any implementation

- [ ] T027 [P] [US4] Write failing test: `get_region_sales(df)` returns a DataFrame with columns `region` and `total_sales`, sorted descending by `total_sales`, matching fixture data in `tests/data/test_transforms.py`
- [ ] T028 [P] [US4] Write failing component contract test: `build_region_chart(df)` returns a `plotly.graph_objects.Figure` with one bar trace and y-axis values sorted descending in `tests/components/test_region_chart.py`

### Implementation for US4 (GREEN phase — after T027 and T028 confirmed failing)

- [ ] T029 [P] [US4] Implement `get_region_sales(df: pd.DataFrame) -> pd.DataFrame` in `data/transforms.py` — same pattern as `get_category_sales()` using `region` column (depends on T027)
- [ ] T030 [US4] Implement `build_region_chart(df: pd.DataFrame) -> go.Figure` in `components/region_chart.py` — same pattern as `build_category_chart()` using region data (depends on T028, T029)
- [ ] T031 [US4] Fill right column in `dashboard.py` two-column layout with region chart, replacing the US3 placeholder (depends on T030)

**Checkpoint**: Full dashboard complete — all 5 user stories functional; `uv run pytest` passes all tests

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Presentation, deployment verification, and constitution compliance sign-off

- [ ] T032 [P] Add `st.set_page_config(page_title="ShopSmart Sales Dashboard", layout="wide")` and a page title header to `dashboard.py`
- [ ] T033 [P] Verify all 4 charts satisfy Constitution Principle III (Interactivity-First) — confirm hover tooltips work in browser for KPI cards, trend chart, category chart, and region chart
- [ ] T034 [P] Run full test suite with `uv run pytest -v` — confirm all tests pass and no warnings
- [ ] T035 Redeploy updated dashboard to Streamlit Community Cloud — verify public URL reflects all 5 user stories and matches expected values (~$650K–$700K Total Sales, 482 Total Orders, 5 categories, 4 regions)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1 (Setup)**: No dependencies — start immediately
- **Phase 2 (Foundational)**: Depends on Phase 1 — BLOCKS all user stories
- **Phase 3 (US1)**: Depends on Phase 2
- **Phase 4 (US2)**: Depends on Phase 2; can start in parallel with Phase 3
- **Phase 5 (US5)**: Depends on Phase 3 + Phase 4 (error handling wires into existing dashboard.py structure)
- **MVP Deploy (T021)**: Depends on Phase 5 completion
- **Phase 6 (US3)**: Depends on MVP deploy checkpoint
- **Phase 7 (US4)**: Depends on Phase 6 (extends bar chart pattern)
- **Phase 8 (Polish)**: Depends on Phase 7

### User Story Dependencies

- **US1 (P1)**: Foundational complete → no story dependencies
- **US2 (P2)**: Foundational complete → no story dependencies; can parallel with US1
- **US5 (P5)**: US1 + US2 complete (needs dashboard.py structure in place)
- **US3 (P3)**: MVP deploy complete
- **US4 (P4)**: US3 complete (reuses bar chart pattern)

### Within Each Phase

1. Write tests → confirm FAILING (Red)
2. Write implementation → confirm PASSING (Green)
3. Refactor if needed → confirm still PASSING
4. Commit with Jira key (e.g., `ECOM-3: implement KPI cards`)

### Parallel Opportunities

- T002 and T003 (setup) can run in parallel after T001
- T004 and T005 (foundational tests) can run in parallel
- T007 and T008 (US1 tests) can run in parallel
- T012 and T013 (US2 tests) can run in parallel; also parallel with T007/T008
- T017 and T018 (US5 tests) can run in parallel
- T022, T023 (US3 tests) can run in parallel
- T027, T028 (US4 tests) can run in parallel
- T032, T033, T034 (polish) can run in parallel

---

## Implementation Strategy

### MVP First (US1 + US2 + US5)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational data loader
3. Complete Phase 3: US1 KPI cards → validate independently
4. Complete Phase 4: US2 trend chart → validate independently
5. Complete Phase 5: US5 error handling → validate with missing CSV
6. **DEPLOY → T021**: Share URL with stakeholders
7. Gather feedback before continuing to US3/US4

### Incremental Delivery

Each phase checkpoint is a demo-able, deployable increment:

| After Phase | What's Live |
|-------------|-------------|
| Phase 3 | KPI cards only |
| Phase 4 | KPI cards + trend chart |
| Phase 5 | Full MVP — safe for exec demo |
| Phase 6 | + Category breakdown |
| Phase 7 | + Region breakdown (full feature) |
| Phase 8 | Polished, production-ready |

---

## Notes

- `[P]` tasks = different files, no blocking dependencies — safe to run in parallel
- `[USN]` label maps each task to its user story for Jira traceability
- Every test task MUST be run and confirmed FAILING before its paired implementation task starts (constitution Principle II)
- `data/sales-data.csv` is read-only — never write to it (constitution Principle I)
- Commit `uv.lock` in the same commit that adds/removes any dependency (constitution Principle V)
- Each component MUST have at least one interactive element (hover tooltip) before its task is marked complete (constitution Principle III)
- Commit messages MUST reference the Jira issue key: `ECOM-N: description`
