# SilverTrack

A full-stack movie and TV-show tracker for cinephiles.

**Team:** Nameera Afrose · Tahia Islam · Taaruni Ananya · Ninglan Zhuang  
**Course:** CSC 4710 – Database Systems, Phase 2

---

## Tech Stack

| Layer     | Technology           |
|-----------|----------------------|
| Frontend  | React (Create React App) |
| Backend   | Python · Flask       |
| Database  | Azure Database for MySQL (Flexible Server) · SQLite fallback for quick local dev |

---

## Features

### Basic
| Feature | Description |
|---------|-------------|
| **Find** | Search movies & TV shows by title, genre, year, or type |
| **View** | Full title details — rating, episode list, cast & crew |
| **Track** | Record watch progress (status, season/episode for TV shows) |
| **Review** | Write and browse reviews at any point in the watch journey |

### Advanced
| Feature | Description |
|---------|-------------|
| **Connect** | Add watch-buddies and compare progress side-by-side |
| **Predict** | Estimated finish date based on viewing pace |
| **Recommend** | Personalised recommendations derived from watch history |
| **Trending** | Daily top-watched titles ranked by community activity |

---

## Database Schema

```
TITLE_BASICS      – core title metadata (tconst, titleType, primaryTitle, startYear, genres)
TITLE_RATINGS     – average rating & vote count
TITLE_EPISODE     – season/episode mapping for TV shows
NAME_BASICS       – person records (actors, directors, writers)
TITLE_PRINCIPALS  – title ↔ person bridge (category, characters)
TITLE_CREW        – director & writer lists per title
TITLE_AKAS        – alternate titles / regional names
USERS             – registered user accounts
WATCH_PROGRESS    – per-user tracking record (status, current S/E, pace)
REVIEWS           – user reviews with optional episode context
WATCH_BUDDIES     – friend/buddy relationships
DAILY_ACTIVITY    – daily interaction counts per title (powers trending)
USER_DAILY_ACTIVITY – per-user daily interaction counts per title
```

---

## Connecting to Azure Database for MySQL

The production database is hosted on **Azure Database for MySQL Flexible Server**.  
The backend connects to it using standard MySQL environment variables — no code changes needed, just configuration.  
SQLite is kept as a zero-configuration fallback for quick local development.

### How it works

`database.py` reads `DB_TYPE` from the environment:

- `DB_TYPE=sqlite` (default) → opens a local `silvertrack.db` file via Python's built-in `sqlite3`.
- `DB_TYPE=mysql` → connects to MySQL using `pymysql` with the `MYSQL_*` env vars below.

Azure Database for MySQL Flexible Server is a fully managed MySQL 8-compatible service. The app treats it exactly like any other MySQL host — the only difference is the server hostname and the requirement for TLS/SSL (enforced by Azure by default).

### 1. Configure environment variables

Copy the example file and fill in your Azure credentials:

```bash
cp .env.example .env
```

```dotenv
DB_TYPE=mysql

# Azure Database for MySQL Flexible Server
MYSQL_HOST=<your-server>.mysql.database.azure.com
MYSQL_PORT=3306
MYSQL_USER=<admin-username>
MYSQL_PASSWORD=<admin-password>
MYSQL_DATABASE=silvertrack
```

> **Azure hostname format:** `<server-name>.mysql.database.azure.com` — find it on the Azure Portal under *Overview* for your Flexible Server resource.

> **SSL:** Azure Flexible Server enforces SSL by default. `pymysql` uses SSL automatically when connecting to Azure hosts; no extra driver flags are required for standard connections.

### 2. Create the database (first time only)

Connect to the server with any MySQL client and run:

```sql
CREATE DATABASE IF NOT EXISTS silvertrack
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;
```

The Flask app will create all 12 tables automatically on first start.

### 3. Install Python dependencies

```bash
pip install -r backend/requirements.txt
```

This installs `pymysql` and `python-dotenv` (already listed in `requirements.txt`).

### 4. Start the backend

```bash
cd backend
PORT=5001 python app.py          # default is 5001; reads .env automatically
```

### 5. Load real IMDB data into Azure (optional)

`backend/load_imdb.py` bulk-loads up to 10,000 recent titles from the official [IMDB TSV datasets](https://developer.imdb.com/non-commercial-datasets/) directly into the Azure database.

**Steps:**

1. Download the following `.tsv.gz` files from IMDB and place them in `~/Downloads/`:
   - `title.basics.tsv.gz`
   - `title.ratings.tsv.gz`
   - `name.basics.tsv.gz`
   - `title.crew.tsv.gz`
   - `title.episode.tsv.gz`

2. Edit `backend/load_imdb.py` to set the correct Azure connection details (host, user, password). **Do not commit credentials to source control** — consider using environment variables or a local config file excluded by `.gitignore`.

3. Run:
   ```bash
   pip install pymysql
   python backend/load_imdb.py
   ```

The script filters to movies and TV series from the most recent years, deduplicates via `INSERT IGNORE`, and prints progress for each table.

### Switching back to SQLite

Set `DB_TYPE=sqlite` (or remove the variable entirely) and restart – no MySQL server or Azure account needed.

---

## Connecting to MySQL Locally (alternative)

If you prefer a local MySQL server instead of Azure:

### 1. Install MySQL

| OS | Command |
|----|---------|
| macOS (Homebrew) | `brew install mysql && brew services start mysql` |
| Ubuntu / Debian | `sudo apt update && sudo apt install mysql-server -y && sudo systemctl start mysql` |
| Windows | Download the [MySQL Installer](https://dev.mysql.com/downloads/installer/) and run it |

### 2. Create the database and user

```sql
CREATE DATABASE IF NOT EXISTS silvertrack
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

CREATE USER IF NOT EXISTS 'silvertrack'@'localhost'
  IDENTIFIED BY 'change_me';

GRANT ALL PRIVILEGES ON silvertrack.* TO 'silvertrack'@'localhost';

FLUSH PRIVILEGES;
```

### 3. Set `.env` for local MySQL

```dotenv
DB_TYPE=mysql

MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=silvertrack
MYSQL_PASSWORD=change_me
MYSQL_DATABASE=silvertrack
```

---

## Quick Start

### Prerequisites
- Python 3.9+
- Node.js 18+
- Azure Database for MySQL **or** SQLite (built into Python, zero setup)

### One-command start (development)
```bash
bash start.sh
```
This installs dependencies, seeds the database, and starts both servers:
- **Backend** → defaults to http://localhost:5001 (auto-falls back to 5002-5010 if busy)
- **Frontend** → defaults to http://localhost:3000 (auto-falls back to 3001-3010 if busy)

### Manual start (development)
```bash
# Backend
cd backend
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
PORT=5001 python app.py

# Frontend (separate terminal)
cd frontend
npm install
npm start              # runs on port 3000 with hot reload
```

The frontend dev server proxies all `/api/*` calls to the Flask backend using `frontend/src/setupProxy.js`.
The proxy target comes from `REACT_APP_API_PROXY_TARGET` and defaults to `http://localhost:5001`.

### Production build

For deployments where Flask serves the React app as static files:

```bash
# 1. Build the React frontend
cd frontend
npm install
npm run build          # outputs to frontend/build/

# 2. Start Flask (it serves frontend/build/ for all non-API routes)
cd ../backend
pip install -r requirements.txt
PORT=5001 python app.py          # http://localhost:5001 serves both API and UI
```

---

## REST API Reference

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/titles/search?q=&genre=&year=&type=` | Search titles |
| GET | `/api/titles/<tconst>` | Full title details |
| GET | `/api/progress/<userId>` | User's watch list |
| POST | `/api/progress` | Save / update progress |
| GET | `/api/progress/<userId>/<tconst>/predict` | Finish-date prediction |
| GET | `/api/reviews/<tconst>` | Reviews for a title |
| POST | `/api/reviews` | Submit a review |
| GET | `/api/buddies/<userId>` | User's buddy list |
| POST | `/api/buddies` | Add a buddy |
| GET | `/api/buddies/compare?userId=&buddyId=&tconst=` | Compare progress |
| GET | `/api/trending?date=YYYY-MM-DD` | Daily trending titles |
| GET | `/api/recommendations/<userId>` | Personalized picks |
| GET | `/api/users` | List users |
| POST | `/api/users` | Register user |
| POST | `/api/auth/login` | Login |

---

## ER Diagram (summary)

```
TITLE_BASICS ─── TITLE_RATINGS        (1:1)
TITLE_BASICS ─── TITLE_CREW           (1:1)
TITLE_BASICS ─── TITLE_EPISODE        (1:N)
TITLE_BASICS ─── TITLE_AKAS           (1:N)
TITLE_BASICS ─── TITLE_PRINCIPALS ─── NAME_BASICS   (M:N via bridge)
USERS        ─── WATCH_PROGRESS ───── TITLE_BASICS
USERS        ─── REVIEWS       ───── TITLE_BASICS
USERS        ─── WATCH_BUDDIES ───── USERS
TITLE_BASICS ─── DAILY_ACTIVITY
USERS        ─── USER_DAILY_ACTIVITY ───── TITLE_BASICS
```

---

## Sprint Plan

See [`SPRINT.md`](SPRINT.md) for the full sprint breakdown with all tasks, sizes, owners, and statuses.

