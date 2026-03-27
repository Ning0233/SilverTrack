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
| Database  | MySQL (local) · SQLite fallback for quick local dev |

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
```

---

## Connecting to MySQL Locally

The backend supports **MySQL** as its primary database.  
SQLite is kept as a zero-configuration fallback for quick local development.

### 1. Install MySQL

| OS | Command |
|----|---------|
| macOS (Homebrew) | `brew install mysql && brew services start mysql` |
| Ubuntu / Debian | `sudo apt update && sudo apt install mysql-server -y && sudo systemctl start mysql` |
| Windows | Download the [MySQL Installer](https://dev.mysql.com/downloads/installer/) and run it |

### 2. Create the database and user

Log in as the MySQL root user and run:

```sql
CREATE DATABASE IF NOT EXISTS silvertrack
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

CREATE USER IF NOT EXISTS 'silvertrack'@'localhost'
  IDENTIFIED BY 'change_me';

GRANT ALL PRIVILEGES ON silvertrack.* TO 'silvertrack'@'localhost';

FLUSH PRIVILEGES;
```

> **Tip:** Replace `change_me` with a strong password and update `.env` accordingly.

### 3. Configure environment variables

Copy the provided example file and edit it:

```bash
cp .env.example .env
```

Set the following values in `.env`:

```dotenv
DB_TYPE=mysql

MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=silvertrack
MYSQL_PASSWORD=change_me
MYSQL_DATABASE=silvertrack
```

### 4. Install the Python MySQL driver

```bash
pip install -r backend/requirements.txt
```

This installs `pymysql` (already listed in `requirements.txt`).

### 5. Start the app

```bash
# Load .env automatically before starting Flask
export $(grep -v '^#' .env | xargs)   # macOS / Linux
# On Windows PowerShell use: Get-Content .env | ForEach-Object { $env:$($_.Split('=')[0]) = $_.Split('=')[1] }

cd backend
python app.py
```

The app will create all 11 tables in the `silvertrack` MySQL database on first run and seed them with sample data.

### Switching back to SQLite

Set `DB_TYPE=sqlite` (or remove the variable entirely) and restart – no MySQL server needed.

---

## Quick Start

### Prerequisites
- Python 3.9+
- Node.js 18+
- MySQL 8.0+ **or** SQLite (built into Python, zero setup)

### One-command start
```bash
bash start.sh
```
This installs dependencies, seeds the database, and starts both servers:
- **Backend** → http://localhost:5000
- **Frontend** → http://localhost:3000

### Manual start
```bash
# Backend
cd backend
pip install -r requirements.txt
python app.py          # runs on port 5000

# Frontend (separate terminal)
cd frontend
npm install
npm start              # runs on port 3000
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
```

---

## Sprint Plan

See [`SPRINT.md`](SPRINT.md) for the full sprint breakdown with all tasks, sizes, owners, and statuses.

