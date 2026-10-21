# Ziyo Impact KPI Dashboard — Operations & Maintenance Guide

**Audience:** the technical/admin staff who will run and maintain the Ziyo KPI
dashboard. No prior Metabase or database experience assumed.

This dashboard runs on **Metabase** (free, open-source). It reads its numbers from
a small **PostgreSQL** database. Both run on your own computer or server using
**Docker** — one command starts everything. There are no licence fees and no cloud
sign-up.

---

## Contents

1. What you received
2. Install Docker (Windows & Mac)
3. Start / stop the dashboard
4. First-time Metabase setup
5. The data model (how the numbers are stored)
6. Updating the numbers each month
7. Adding a brand-new KPI
8. Editing & building dashboards (no code)
9. Backups & restore
10. Moving it to a shared server (optional)
11. Troubleshooting

---

## 1 · What you received

Inside the `metabase/` folder:

| File | Purpose |
|---|---|
| `docker-compose.yml` | Starts PostgreSQL + Metabase together with one command. |
| `ziyo_kpi_metabase.sql` | Creates the tables and loads all KPI data (runs automatically on first start). |
| `METABASE_SETUP.md` | Quick build guide for the charts. |
| `CLIENT_HANDOVER.md` | This document. |

You also have `Ziyo_KPI_Dashboard.html` one level up — the branded, presentation
version of the same numbers. Keep it for showing the ministry / board; use Metabase
for day-to-day, self-service work.

---

## 2 · Install Docker

Docker is the free tool that runs Metabase and the database for you.

### Windows 10 / 11

1. Download **Docker Desktop for Windows** from <https://www.docker.com/products/docker-desktop/>.
2. Run the installer. When asked, **keep "Use WSL 2" enabled** (the default).
   - If it prompts to install **WSL 2**, accept, then **restart the PC** once.
3. Launch **Docker Desktop** from the Start menu. Wait until it says **"Engine running"**
   (whale icon steady in the system tray).
4. Verify: open **PowerShell** and run `docker --version` — you should see a version number.

> Requirements: Windows 10/11 64-bit, virtualization enabled in BIOS (on by default on
> most machines). Docker Desktop installs WSL 2 for you if needed.

### macOS

1. Download **Docker Desktop for Mac** — pick **Apple Silicon** (M1/M2/M3/M4) or
   **Intel** to match your Mac — from <https://www.docker.com/products/docker-desktop/>.
2. Open the `.dmg` and drag **Docker** to **Applications**.
3. Launch **Docker** from Applications. Wait until the menu-bar whale icon stops
   animating = engine ready.
4. Verify: open **Terminal** and run `docker --version`.

---

## 3 · Start / stop the dashboard

Open a terminal (**PowerShell** on Windows, **Terminal** on Mac) and go to the
`metabase` folder. Example:

```
# Windows (adjust the path to where the folder lives)
cd C:\Users\<you>\ZiyoForum\metabase

# Mac
cd ~/Downloads/ZiyoForum/metabase
```

| Action | Command |
|---|---|
| **Start** (run in background) | `docker compose up -d` |
| **Check status** | `docker compose ps` |
| **View logs** | `docker compose logs -f metabase` |
| **Stop** (keeps all data) | `docker compose down` |
| **Restart** | `docker compose restart` |
| **Full reset** (wipes data, reloads the seed) | `docker compose down -v` then `docker compose up -d` |

The **first** start downloads the software (~1–2 GB, a few minutes). Later starts
take seconds. Your saved dashboards and data **persist** across stop/start — only
`down -v` erases them.

---

## 4 · First-time Metabase setup

1. With the stack running, open **http://localhost:3000** in a browser.
   (First boot takes ~1 minute — refresh until the welcome screen appears.)
2. Create the **admin account** (name, email, password). Keep these safe — they
   control the dashboard.
3. Connect the KPI database. If not prompted during setup, go to
   **gear icon → Admin settings → Databases → Add database**:

   | Field | Value |
   |---|---|
   | Database type | **PostgreSQL** |
   | Display name | `Ziyo KPIs` |
   | Host | `db` |
   | Port | `5432` |
   | Database name | `ziyo_kpi` |
   | Username | `ziyo` |
   | Password | `ziyo` |

   Save. Metabase reads the tables within seconds.

> **Change the password** before any real/shared deployment — see §10.

---

## 5 · The data model

Three tables and two helper views. You mostly touch `kpi_values` (monthly numbers).

- **`kpi_layers`** — the five groupings: North Star, Reach, Engagement, Outcome, Operations.
- **`kpi_metrics`** — one row per KPI: its name, `unit`, `target`, whether higher is
  better, definition, and which layer it belongs to. Each has a numeric **`id`**.
- **`kpi_values`** — the monthly history: `metric_id`, `period` (first of the month),
  `value`. **This is what you update over time.**
- **`kpi_latest`** *(view)* — the most recent value of each KPI (auto-calculated).
- **`kpi_with_status`** *(view)* — one row per KPI with its latest value, target,
  percent-of-target, and a **status** (`On track` / `At risk` / `Behind`). Build
  your cards from this; the status colours come for free.

To see every metric's `id`, run (see §6 for how to open the query tool):
```sql
SELECT id, name, layer_key, unit, target FROM kpi_metrics ORDER BY id;
```

---

## 6 · Updating the numbers each month

The dashboard is **live** — add a row and every chart, status colour, and trend
updates automatically. No rebuilds.

**Option A — inside Metabase (no extra tools).** Metabase can run SQL:
**+ New → SQL query → pick "Ziyo KPIs"**, paste, and **Run**.

```sql
-- Record October 2026 for metric 3 (Organic referral rate = 24%)
INSERT INTO kpi_values (metric_id, period, value)
VALUES (3, '2026-10-01', 24);
```

To correct a value you already entered:
```sql
UPDATE kpi_values SET value = 25
WHERE metric_id = 3 AND period = '2026-10-01';
```

**Option B — database console** (for bulk edits):
```
docker compose exec db psql -U ziyo -d ziyo_kpi
```
Then type SQL at the `ziyo_kpi=#` prompt; `\q` to exit.

> Tip: always use the **first day of the month** for `period` (e.g. `2026-11-01`)
> so the monthly trend lines stay tidy.

---

## 7 · Adding a brand-new KPI

Two inserts: define the metric, then give it values.

```sql
-- 1) define it (pick the next free id; layer_key is one of:
--    reach / engage / outcome / ops). higher_is_better = false means "lower is better".
INSERT INTO kpi_metrics (id, layer_key, name, unit, target, higher_is_better, definition, position)
VALUES (26, 'engage', 'Push opt-in rate', '%', 40, true,
        'Share of users who allow push notifications.', 7);

-- 2) add its monthly values
INSERT INTO kpi_values (metric_id, period, value) VALUES
  (26, '2026-09-01', 33),
  (26, '2026-10-01', 38);
```

It appears automatically in `kpi_with_status` and in any chart built on that view.
Then add a card for it (next section).

---

## 8 · Editing & building dashboards (no code)

Everything uses Metabase's **Query Builder** — point and click, no SQL.

**Add a KPI card with status colour**
1. **+ New → Question → Ziyo KPIs → `kpi_with_status`**.
2. Filter **Metric = <your KPI>**.
3. Show the **`latest_value`** field → Visualization **Number**.
4. **Settings → Goal line** → set to the **target** (shows progress).
5. **Conditional formatting** on the `status` field → green `On track`, amber
   `At risk`, red `Behind`.
6. **Save**, then **duplicate** and change the filter to make the next card quickly.

**Edit an existing chart:** open it → **Editor** (top-right) → change the filter,
grouping, or visualization → **Save** (or **Save as** a copy).

**Put cards on a dashboard:** **+ New → Dashboard**, drag cards in, resize, add text
headings for each layer, and add a **Dashboard filter** wired to the `layer` field so
viewers can filter by Reach / Engagement / Outcome / Operations.

**Share with viewers:** invite people under **Admin → People** (give them "view"
access), or enable **public links** per dashboard (Admin → Settings → Public sharing)
if you want a no-login URL.

Full worked steps (North Star, outcome bar chart, filters) are in `METABASE_SETUP.md`.

---

## 9 · Backups & restore

Your work lives in two places: the **KPI data** (Postgres) and your **saved
dashboards/questions** (Metabase's own storage). Back up both.

**Back up the KPI data:**
```
docker compose exec db pg_dump -U ziyo ziyo_kpi > ziyo_kpi_backup.sql
```

**Restore it:**
```
docker compose exec -T db psql -U ziyo -d ziyo_kpi < ziyo_kpi_backup.sql
```

**Back up Metabase's dashboards:** they are stored in the `ziyo_mb` Docker volume.
The simplest safe backup is to copy the whole `metabase/` folder **and** export the
volume:
```
docker run --rm -v metabase_ziyo_mb:/data -v "$PWD":/backup alpine \
  tar czf /backup/metabase_app_backup.tar.gz -C /data .
```
(On Windows PowerShell replace `"$PWD"` with `${PWD}`.)

Keep backups off the machine (shared drive, cloud storage) on a regular schedule.

---

## 10 · Moving it to a shared server (optional)

To let the whole team reach it (not just one laptop):

1. Put these files on a small always-on Linux server or VM (any cloud provider, or
   an office machine). Install Docker Engine, then `docker compose up -d`.
2. Access it at `http://<server-address>:3000`.
3. **Before going live, harden it:**
   - Change the database password: edit `POSTGRES_PASSWORD` in `docker-compose.yml`
     (and re-enter it in Metabase's database settings).
   - Give Metabase a real app database and set a strong admin password.
   - Put it behind HTTPS (a reverse proxy such as Caddy or Nginx) if reachable
     beyond your network.

For a handful of staff, a single modest server (2 CPU / 4 GB RAM) is plenty.

---

## 11 · Troubleshooting

| Symptom | Fix |
|---|---|
| `docker: command not found` | Docker Desktop isn't running — launch it and wait for "Engine running". |
| Browser shows "can't connect" at :3000 | Give Metabase ~1 min on first boot; check `docker compose ps` shows it `running`. |
| **Port 3000 already in use** | Something else uses 3000. Edit `docker-compose.yml`: change `"3000:3000"` to `"3001:3000"`, restart, use :3001. |
| **Port 5432 already in use** (local Postgres) | Change `"5432:5432"` to `"5433:5432"` in `docker-compose.yml` and restart. (Metabase still connects via host `db`, unaffected.) |
| Metabase can't find the database | Host must be **`db`** (not `localhost`) — both run in the same Docker network. |
| Data looks wrong / want a clean slate | `docker compose down -v` then `docker compose up -d` reloads the original seed. **This erases your edits and dashboards** — back up first (§9). |
| Windows: "WSL 2 installation is incomplete" | Run `wsl --install` in an admin PowerShell, restart, reopen Docker Desktop. |
| Mac: app won't open ("unidentified developer") | Right-click Docker in Applications → **Open** → confirm once. |

---

**Summary:** start with `docker compose up -d`, open `http://localhost:3000`, update
numbers by inserting rows into `kpi_values`, and build/edit charts with the point-and-
click Query Builder. Back up regularly (§9). For anything beyond this, the Metabase
documentation at <https://www.metabase.com/docs/latest/> is thorough and free.
