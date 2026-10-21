# Ziyo KPI Dashboard → Metabase

Port the Ziyo KPI dashboard to **Metabase** (free, open-source) so the client can
view and build dashboards themselves — no code, no license fee.

This folder contains everything needed:

| File | What it is |
|---|---|
| `ziyo_kpi_metabase.sql` | Postgres schema + all KPI data (generated from the dashboard). |
| `docker-compose.yml` | One command to run Postgres + Metabase locally, fully free. |
| `METABASE_SETUP.md` | This guide. |

---

## Is Metabase really free?

Yes — **Metabase Open Source** is free forever, self-hosted (AGPL licence). It is
the no-code tool where non-technical users build charts by clicking. Only
*Metabase Cloud* is paid — we don't use it here.

---

## 1 · Start it (one command)

Requires Docker Desktop (free).

```bash
cd metabase
docker compose up -d
# wait ~1 minute on first boot, then:
open http://localhost:3000
```

This starts two containers:
- **Postgres** — auto-loaded with the KPI data from `ziyo_kpi_metabase.sql`.
- **Metabase** — the dashboard app.

Create your admin account in the browser when prompted.

> No Docker? Alternatives: run the Metabase JAR (`java -jar metabase.jar`, needs
> Java 21) and load `ziyo_kpi_metabase.sql` into any Postgres — including a free
> cloud one (Neon, Supabase, Railway). Then connect Metabase to it (step 2).

---

## 2 · Connect Metabase to the data

In Metabase: **Settings (gear) → Admin → Databases → Add database → PostgreSQL**

| Field | Value |
|---|---|
| Display name | `Ziyo KPIs` |
| Host | `db` *(if using docker compose)* — otherwise your Postgres host |
| Port | `5432` |
| Database name | `ziyo_kpi` |
| Username | `ziyo` |
| Password | `ziyo` |

Save. Metabase scans the tables in a few seconds.

---

## 3 · What's in the database

Three tables + two ready-made views (the views do the hard work so cards are one click):

- **`kpi_layers`** — the four framework layers + North Star (name, question, order).
- **`kpi_metrics`** — one row per metric: `name, unit, target, higher_is_better, definition, layer`.
- **`kpi_values`** — monthly history: `metric_id, period, value` (the trend data).
- **`kpi_latest`** *(view)* — latest value per metric.
- **`kpi_with_status`** *(view)* — **the one to build cards from.** One row per
  metric with `latest_value`, `target`, `pct_of_target`, and a `status` label
  (`On track` / `At risk` / `Behind` / `North Star`) already computed — matching
  the HTML dashboard's logic exactly, including "lower is better" metrics.

---

## 4 · Build the dashboard (no code)

Everything below uses the **Query Builder** (the "+ New → Question" button → "Pick
your starting data"). No SQL needed.

### 4a · North Star — big number + trend
1. **+ New → Question → Ziyo KPIs → `kpi_values`**.
2. Filter: **Metric id = 1** (Active Beneficiaries).
3. Summarize: **Sum of value**, grouped by **Period: Month** → **Visualization: Line**.
   This is the trend.
4. Save as **"North Star — trend"**.
5. For the headline number: new Question on **`kpi_with_status`**, filter
   **Metric = Active Beneficiaries**, show **latest_value** → **Visualization: Number**.
   Save as **"North Star — now"**.

### 4b · KPI cards with target + status colour
For any metric (e.g. *Organic referral rate*):
1. **+ New → Question → `kpi_with_status`**, filter **Metric = …**.
2. Pick the **`latest_value`** column → **Visualization: Number**.
3. Click **Settings → Goal line**: set it to the **target** value → the card shows
   progress toward goal.
4. **Conditional formatting** (gear on the column): colour by the `status` column —
   green `On track`, amber `At risk`, red `Behind`. (This reproduces the status pills.)
5. Add the **`definition`** field as the card description.

Tip: do this once, then **duplicate** the card and change the metric filter — fast
for all 24 KPIs.

### 4c · Status overview table (fastest win)
1. **+ New → Question → `kpi_with_status`**, no filter.
2. **Visualization: Table.** Show `layer, metric, latest_value, target, pct_of_target, status`.
3. Conditional formatting on `status` (green/amber/red) or on `pct_of_target`
   (colour scale). One table = the whole scorecard.

### 4d · Outcome vs Target bar chart
1. **+ New → Question → `kpi_with_status`**, filter **Layer = Outcome** and
   **unit = %** (comparable metrics).
2. Summarize: show **latest_value** by **metric** → **Visualization: Bar**.
3. **Settings → Goal line** → set to target, or add `target` as a second series.

### 4e · Assemble + filter by layer
1. **+ New → Dashboard → "Ziyo Impact KPIs"**. Add the saved questions.
2. Group cards into sections with text cards: **North Star**, **Reach**,
   **Engagement**, **Outcome (reported to donors)**, **Operations**.
3. Add a **Dashboard filter → Text/Category**, wired to the **`layer`** field of each
   card — now the client can filter the whole board by layer (like the HTML tabs).
4. Or use **Dashboard tabs**: one tab per layer.

---

## 5 · Keeping data fresh

The dashboard reads live from Postgres, so updating a number = inserting a row:

```sql
-- this month's value for metric 3 (Organic referral rate)
INSERT INTO kpi_values (metric_id, period, value)
VALUES (3, '2026-11-01', 24);
```

The cards, status colours, and trends update automatically. Point the dev team's
pipeline at these tables (or let staff edit via a simple admin form) and the board
stays current with zero rebuilds.

---

## What ports 1:1 and what doesn't

- **Ports cleanly:** every metric, target, status rule, trend, and the layer grouping.
- **Approximate:** the exact branded look (custom hero, pills, ordinal greens).
  Metabase applies its own styling — functionally identical, visually its own.

**Recommended split:** keep the polished HTML dashboard (`../Ziyo_KPI_Dashboard.html`)
as the presentation view for the ministry/CEO; use Metabase as the team's live,
self-service tool. Both read the same numbers.
