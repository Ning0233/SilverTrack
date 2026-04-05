# SilverTrack — Final Project Report

**Course:** CSC 4710 – Database Systems  
**Stage:** 5 — Demo and Final Report  
**Team:** Nameera Afrose · Tahia Islam · Taaruni Ananya · Ninglan Zhuang  
**Application:** SilverTrack — A Movie & TV-Show Tracker for Cinephiles

---

## Table of Contents

1. [Application Overview](#1-application-overview)
2. [Database Design](#2-database-design)
   - 2.1 [Entity-Relationship Diagram](#21-entity-relationship-diagram)
   - 2.2 [Schema Details](#22-schema-details)
   - 2.3 [Relationships and Integrity Constraints](#23-relationships-and-integrity-constraints)
3. [Technology Stack](#3-technology-stack)
4. [Basic Functions](#4-basic-functions)
   - 4.1 [Insert Records](#41-insert-records)
   - 4.2 [Search and List Results](#42-search-and-list-results)
   - 4.3 [Interesting Queries](#43-interesting-queries)
   - 4.4 [Update Records](#44-update-records)
   - 4.5 [Delete Records](#45-delete-records)
5. [Advanced Functions](#5-advanced-functions)
   - 5.1 [Personalized Recommendation Engine](#51-personalized-recommendation-engine)
   - 5.2 [Finish-Date Prediction Algorithm](#52-finish-date-prediction-algorithm)
   - 5.3 [Community Trending System](#53-community-trending-system)
6. [Sample SQL Queries](#6-sample-sql-queries)
7. [System Architecture](#7-system-architecture)
8. [Lessons Learned and Challenges](#8-lessons-learned-and-challenges)
9. [Conclusion](#9-conclusion)

---

## 1. Application Overview

**SilverTrack** is a full-stack web application that lets users discover, track, review, and discuss movies and TV shows. The name is inspired by the classic "silver screen" of cinema.

### Problem Statement

Existing streaming platforms (Netflix, Hulu, etc.) do not allow cross-platform tracking. A viewer watching *The Bear* on Hulu while rewatching *Breaking Bad* on Netflix has no single place to manage their watchlist, log episodes, compare pace with friends, or get cross-genre recommendations. SilverTrack solves this by providing a **platform-agnostic** tracker backed by the entire IMDB title catalogue.

### Core User Stories

| # | As a… | I want to… | So that… |
|---|--------|-----------|---------|
| 1 | Viewer | Search for any title by keyword, genre, year, or type | I can find what I'm looking for quickly |
| 2 | Viewer | Log which episode I'm on and how fast I watch | I can stay organized across multiple shows |
| 3 | Viewer | Read and write reviews | I can share opinions and discover community sentiment |
| 4 | Social user | Connect with friends (watch buddies) | I can compare progress on the same show |
| 5 | Power user | Get personalized title recommendations | I don't have to hunt for what to watch next |
| 6 | Power user | See a predicted finish date for a show | I can plan my viewing schedule |
| 7 | Any user | See what's trending in the community today | I can discover popular content organically |

---

## 2. Database Design

### 2.1 Entity-Relationship Diagram

```
                         ┌──────────────────┐
                         │  TITLE_BASICS    │
                         │  (tconst PK)     │
                         └────────┬─────────┘
              ┌──────────┬────────┼──────────┬───────────────┐
              │          │        │           │               │
        ┌─────▼──────┐ ┌─▼──────┐ ┌──────────▼──┐ ┌────────▼──────┐
        │TITLE_RATINGS│ │TITLE_  │ │TITLE_EPISODE│ │ TITLE_AKAS    │
        │(tconst PK/FK)│ │ CREW   │ │(tconst PK   │ │(titleId FK,   │
        └────────────┘ │(tconst)│ │ parentTconst│ │ ordering)     │
                       └────────┘ │ FK)         │ └───────────────┘
                                  └─────────────┘
                         ┌─────────────────────┐
                         │  TITLE_PRINCIPALS   │
                         │  (tconst FK,        │
                         │   nconst FK  PK)    │
                         └──────────┬──────────┘
                                    │
                         ┌──────────▼──────────┐
                         │    NAME_BASICS      │
                         │   (nconst PK)       │
                         └─────────────────────┘

              ┌───────────────────────────────────────────┐
              │                  USERS                    │
              │              (userId PK)                  │
              └──────┬──────────┬─────────────┬───────────┘
                     │          │             │
           ┌─────────▼──┐  ┌────▼──────┐  ┌──▼──────────────┐
           │WATCH_PROGRESS│ │  REVIEWS  │  │  WATCH_BUDDIES  │
           │(progressId  │ │(reviewId  │  │(userId1 FK,     │
           │ userId FK   │ │ userId FK │  │ userId2 FK)     │
           │ tconst FK)  │ │ tconst FK)│  └─────────────────┘
           └──────┬──────┘ └───────────┘
                  │
     ┌────────────▼─────────────┐  ┌──────────────────────────┐
     │     DAILY_ACTIVITY       │  │   USER_DAILY_ACTIVITY    │
     │(activityDate, tconst PK  │  │(activityDate, userId,    │
     │ tconst FK)               │  │ tconst PK; FK on both)   │
     └──────────────────────────┘  └──────────────────────────┘
```

### 2.2 Schema Details

The database contains **12 tables** split into two groups:

#### Reference Tables (IMDB-derived, read-only after import)

| Table | Primary Key | Notable Columns | Purpose |
|-------|------------|----------------|---------|
| `TITLE_BASICS` | `tconst` | `titleType`, `primaryTitle`, `startYear`, `genres` | Master record for every title |
| `TITLE_RATINGS` | `tconst` | `averageRating`, `numVotes` | Community rating from IMDB votes |
| `TITLE_EPISODE` | `tconst` | `parentTconst`, `seasonNumber`, `episodeNumber` | Episode-to-series mapping |
| `TITLE_CREW` | `tconst` | `directors`, `writers` | Comma-separated IMDB name IDs |
| `TITLE_AKAS` | (`titleId`, `ordering`) | `title`, `region` | Regional/alternate title names |
| `TITLE_PRINCIPALS` | (`tconst`, `nconst`) | `category`, `characters` | Bridge: titles ↔ people |
| `NAME_BASICS` | `nconst` | `primaryName`, `birthYear`, `primaryProfession` | Actor / director / writer profiles |

#### Application Tables (User-generated, read-write)

| Table | Primary Key | Notable Columns | Purpose |
|-------|------------|----------------|---------|
| `USERS` | `userId` (AUTOINCREMENT) | `username` UNIQUE, `email` UNIQUE, `password` (hashed) | User accounts |
| `WATCH_PROGRESS` | `progressId`; UNIQUE(`userId`, `tconst`) | `status`, `currentSeason`, `currentEpisode`, `episodesPerDay`, `lastWatchedDate` | Per-user watch state |
| `REVIEWS` | `reviewId` (AUTOINCREMENT) | `episodeTconst` (nullable), `rating`, `reviewText`, `createdAt` | Title/episode reviews |
| `WATCH_BUDDIES` | (`userId1`, `userId2`) | — | Bidirectional friend graph |
| `DAILY_ACTIVITY` | (`activityDate`, `tconst`) | `activityCount` | Global trending signal |
| `USER_DAILY_ACTIVITY` | (`activityDate`, `userId`, `tconst`) | `activityCount` | Per-user trending signal |

### 2.3 Relationships and Integrity Constraints

- All foreign keys are enforced (`PRAGMA foreign_keys = ON` for SQLite; `ENGINE=InnoDB` for MySQL).
- `WATCH_PROGRESS.UNIQUE(userId, tconst)` — one progress record per (user, title) pair; supports safe upsert via `ON CONFLICT … DO UPDATE`.
- `WATCH_BUDDIES` stores the pair with `userId1 < userId2` to avoid duplicate rows for the same friendship.
- `TITLE_PRINCIPALS` is a classic many-to-many bridge between `TITLE_BASICS` and `NAME_BASICS`.
- `REVIEWS.episodeTconst` is nullable, enabling reviews on either the whole title or a specific episode.

---

## 3. Technology Stack

| Layer | Technology | Notes |
|-------|------------|-------|
| **Frontend** | React 19 (Create React App) | Component-based SPA; dark cinema theme |
| **Backend** | Python 3 + Flask 3.0 | 14 REST API endpoints; serves React build in production |
| **ORM / Driver** | SQLite3 (stdlib) · PyMySQL 1.1 | Transparent abstraction layer; `?`→`%s` placeholder translation |
| **Database (dev)** | SQLite | Zero-config; file `silvertrack.db` |
| **Database (prod)** | Azure Database for MySQL Flexible Server | Managed MySQL 8.0 |
| **Auth** | Werkzeug `pbkdf2:sha256` | Passwords hashed; never stored in plaintext |
| **CORS** | Flask-CORS | Allows React dev server (port 3000) to call API (port 5001) |
| **Data Source** | IMDB TSV flat files via `load_imdb.py` | Bulk-imported into TITLE_* tables |

---

## 4. Basic Functions

### 4.1 Insert Records

**a) Register a new user** — inserts a row into `USERS` with a hashed password.

```sql
INSERT INTO USERS(username, email, password)
VALUES ('alice', 'alice@example.com', '<pbkdf2-hash>');
```

**b) Save watch progress** — upserts a row in `WATCH_PROGRESS` and increments activity counters.

```sql
INSERT INTO WATCH_PROGRESS
    (userId, tconst, status, currentSeason, currentEpisode, episodesPerDay, lastWatchedDate)
VALUES (1, 'tt0903747', 'watching', 3, 7, 2, date('now'))
ON CONFLICT(userId, tconst) DO UPDATE SET
    status         = excluded.status,
    currentSeason  = excluded.currentSeason,
    currentEpisode = excluded.currentEpisode,
    episodesPerDay = excluded.episodesPerDay,
    lastWatchedDate = date('now');
```

**c) Submit a review** — inserts a row into `REVIEWS` (optionally linked to a specific episode).

```sql
INSERT INTO REVIEWS(userId, tconst, episodeTconst, rating, reviewText)
VALUES (1, 'tt0903747', NULL, 9.5, 'One of the greatest shows ever made.');
```

**d) Add a watch buddy** — inserts into `WATCH_BUDDIES` with canonical pair ordering.

```sql
INSERT INTO WATCH_BUDDIES(userId1, userId2) VALUES (1, 2);
```

### 4.2 Search and List Results

**Search by keyword, genre, year, and/or type** — returns top 50 titles sorted by IMDB rating.

```sql
SELECT tb.tconst, tb.primaryTitle, tb.titleType, tb.startYear, tb.genres,
       tr.averageRating, tr.numVotes
FROM   TITLE_BASICS tb
LEFT JOIN TITLE_RATINGS tr ON tb.tconst = tr.tconst
WHERE  tb.primaryTitle LIKE '%Breaking Bad%'
  AND  tb.genres       LIKE '%Crime%'
  AND  tb.startYear    = 2008
  AND  tb.titleType    = 'tvSeries'
ORDER BY tr.averageRating DESC
LIMIT  50;
```

**List user's watchlist** — joins progress with title metadata.

```sql
SELECT wp.*, tb.primaryTitle, tb.titleType, tb.genres
FROM   WATCH_PROGRESS wp
JOIN   TITLE_BASICS tb ON wp.tconst = tb.tconst
WHERE  wp.userId = 1
ORDER BY wp.lastWatchedDate DESC;
```

**List all reviews for a title** — joins with `USERS` to display the reviewer's username.

```sql
SELECT r.reviewId, r.rating, r.reviewText, r.createdAt, u.username
FROM   REVIEWS r
JOIN   USERS u ON r.userId = u.userId
WHERE  r.tconst = 'tt0903747'
ORDER BY r.createdAt DESC;
```

### 4.3 Interesting Queries

#### Query 1 — Multi-table JOIN: Full title details with cast and crew

This query joins five tables to assemble a complete title page — metadata, rating, episode list, cast, and crew.

```sql
-- Title metadata + rating (JOIN)
SELECT tb.*, tr.averageRating, tr.numVotes
FROM   TITLE_BASICS tb
LEFT JOIN TITLE_RATINGS tr ON tb.tconst = tr.tconst
WHERE  tb.tconst = 'tt0903747';

-- Cast with names (JOIN across bridge table)
SELECT nb.nconst, nb.primaryName, tp.category, tp.characters
FROM   TITLE_PRINCIPALS tp
JOIN   NAME_BASICS nb ON tp.nconst = nb.nconst
WHERE  tp.tconst = 'tt0903747';

-- Episode list ordered by season and episode number
SELECT te.tconst, te.seasonNumber, te.episodeNumber
FROM   TITLE_EPISODE te
WHERE  te.parentTconst = 'tt0903747'
ORDER BY te.seasonNumber, te.episodeNumber;
```

#### Query 2 — AGGREGATE: Trending titles by total community activity

This query uses `JOIN` and aggregated column `activityCount` to rank titles by daily engagement.

```sql
SELECT da.tconst,
       tb.primaryTitle,
       tb.titleType,
       tb.genres,
       tr.averageRating,
       da.activityCount                AS score
FROM   DAILY_ACTIVITY da
JOIN   TITLE_BASICS   tb ON da.tconst = tb.tconst
LEFT JOIN TITLE_RATINGS tr ON da.tconst = tr.tconst
WHERE  da.activityDate = '2026-04-05'
ORDER BY da.activityCount DESC
LIMIT  10;
```

#### Query 3 — AGGREGATE: Average rating per genre across all reviewed titles

This query aggregates user-submitted ratings grouped by their most common genre label.

```sql
SELECT SUBSTR(tb.genres, 1, INSTR(tb.genres || ',', ',') - 1) AS primaryGenre,
       COUNT(r.reviewId)                                        AS reviewCount,
       ROUND(AVG(r.rating), 2)                                  AS avgUserRating,
       ROUND(AVG(tr.averageRating), 2)                          AS avgImdbRating
FROM   REVIEWS r
JOIN   TITLE_BASICS  tb ON r.tconst = tb.tconst
LEFT JOIN TITLE_RATINGS tr ON r.tconst = tr.tconst
WHERE  r.rating IS NOT NULL
GROUP BY primaryGenre
ORDER BY reviewCount DESC;
```

#### Query 4 — Watch-buddy progress comparison (multiple table JOIN)

Retrieves both users' names and progress on the same title in a single round-trip.

```sql
SELECT u1.username   AS user1Name,
       wp1.status    AS user1Status,
       wp1.currentSeason   AS user1Season,
       wp1.currentEpisode  AS user1Episode,
       u2.username   AS user2Name,
       wp2.status    AS user2Status,
       wp2.currentSeason   AS user2Season,
       wp2.currentEpisode  AS user2Episode
FROM   WATCH_BUDDIES wb
JOIN   USERS          u1  ON wb.userId1 = u1.userId
JOIN   USERS          u2  ON wb.userId2 = u2.userId
LEFT JOIN WATCH_PROGRESS wp1 ON wp1.userId = u1.userId AND wp1.tconst = 'tt0903747'
LEFT JOIN WATCH_PROGRESS wp2 ON wp2.userId = u2.userId AND wp2.tconst = 'tt0903747'
WHERE  wb.userId1 = 1 OR wb.userId2 = 1;
```

### 4.4 Update Records

Watch progress is updated in-place via SQL `ON CONFLICT … DO UPDATE` (upsert). A dedicated `PUT`-style call changes only the specified fields.

```sql
-- Update season, episode, pace for an existing progress record
UPDATE WATCH_PROGRESS
SET    currentSeason  = 4,
       currentEpisode = 2,
       episodesPerDay = 3,
       status         = 'watching',
       lastWatchedDate = date('now')
WHERE  userId = 1
  AND  tconst = 'tt0903747';
```

### 4.5 Delete Records

```sql
-- Remove a review
DELETE FROM REVIEWS
WHERE  reviewId = 5
  AND  userId   = 1;          -- ownership check prevents deleting others' reviews

-- Remove a watch-buddy connection
DELETE FROM WATCH_BUDDIES
WHERE  (userId1 = 1 AND userId2 = 2)
    OR (userId1 = 2 AND userId2 = 1);

-- Remove all watch progress for a user (account cleanup)
DELETE FROM WATCH_PROGRESS
WHERE  userId = 1;
```

---

## 5. Advanced Functions

### 5.1 Personalized Recommendation Engine

**What it does:** Suggests up to 10 titles the user has not yet watched, ranked by IMDB rating, filtered to the genre the user watches most often.

**Why it is advanced:**
1. *Useful* — it directly solves the "what to watch next" problem.
2. *Technically challenging* — it requires multi-step query logic: (a) JOIN `WATCH_PROGRESS` with `TITLE_BASICS` to collect genre strings; (b) parse comma-separated genre values in Python to build a frequency map; (c) dynamically construct a SQL `NOT IN (…)` clause with variable-length placeholders; (d) fall back to global top-rated titles when a user has no watch history.
3. *Novel* — most trackers either recommend by rating or by "similar users"; SilverTrack uses the user's own genre affinity computed entirely from their tracked history, without an external recommendation service.

**Key query:**

```sql
SELECT tb.*, tr.averageRating, tr.numVotes
FROM   TITLE_BASICS tb
LEFT JOIN TITLE_RATINGS tr ON tb.tconst = tr.tconst
WHERE  tb.genres LIKE '%Drama%'              -- top genre for this user
  AND  tb.tconst NOT IN ('tt0903747', ...)   -- exclude already-watched titles
ORDER BY tr.averageRating DESC
LIMIT  10;
```

**Algorithm steps:**
1. Fetch all genres from the user's `WATCH_PROGRESS` (joined to `TITLE_BASICS`).
2. Split each comma-separated `genres` string and tally frequency per genre token.
3. Select the genre with the highest count as `top_genre`.
4. Query top-rated unwatched titles in that genre.
5. If the user has no history, fall back to global top-rated titles.

### 5.2 Finish-Date Prediction Algorithm

**What it does:** Given a user's current season/episode and their self-reported viewing pace (`episodesPerDay`), it calculates the exact calendar date they will finish a show.

**Why it is advanced:**
1. *Useful* — viewers planning around events ("I need to finish before the finale airs") get an objective data-driven answer.
2. *Technically challenging* — it requires: (a) counting all episodes in the series from `TITLE_EPISODE`; (b) computing episodes watched using a conditional SQL count (`seasonNumber < current OR (seasonNumber = current AND episodeNumber <= current)`); (c) computing remaining episodes; (d) projecting the finish date with Python `datetime.timedelta`.
3. *Novel* — no standard tracker (Trakt, MyAnimeList) provides personalized finish-date forecasting based on pace.

**Key queries:**

```sql
-- Total episodes in the series
SELECT COUNT(*) AS cnt
FROM   TITLE_EPISODE
WHERE  parentTconst = 'tt0903747';

-- Episodes watched up to current position
SELECT COUNT(*) AS cnt
FROM   TITLE_EPISODE
WHERE  parentTconst = 'tt0903747'
  AND  (seasonNumber < 3
        OR (seasonNumber = 3 AND episodeNumber <= 7));
```

**Prediction formula:**
```
remaining_episodes = total_episodes − watched_episodes
days_left          = remaining_episodes / episodes_per_day
finish_date        = today + timedelta(days = days_left)
```

### 5.3 Community Trending System

**What it does:** Ranks the top 10 titles by total community engagement (watch-progress saves + reviews) for any given date, displayed in a dedicated Trending page.

**Why it is advanced:**
1. *Useful* — readers discover what the community is engaging with right now, not just what has the highest static rating.
2. *Technically challenging* — it requires: (a) a two-level activity tracking schema (`DAILY_ACTIVITY` global, `USER_DAILY_ACTIVITY` per-user); (b) atomic upsert increments on every watch-progress save and review submission; (c) handling the "no data for today yet" edge case by falling back to the latest available date; (d) `JOIN` between activity, title, and rating tables to produce a rich ranked result.
3. *Novel* — it captures real-time engagement momentum rather than static popularity, enabling "sleeper hits" that the community is suddenly binge-watching to surface at the top.

**Key query:**

```sql
SELECT da.tconst,
       tb.primaryTitle,
       tb.titleType,
       tb.genres,
       tr.averageRating,
       da.activityCount AS score
FROM   DAILY_ACTIVITY da
JOIN   TITLE_BASICS   tb ON da.tconst = tb.tconst
LEFT JOIN TITLE_RATINGS tr ON da.tconst = tr.tconst
WHERE  da.activityDate = '2026-04-05'
ORDER BY da.activityCount DESC
LIMIT  10;
```

**Activity increment (upsert):**

```sql
INSERT INTO DAILY_ACTIVITY(activityDate, tconst, activityCount)
VALUES (date('now'), 'tt0903747', 1)
ON CONFLICT(activityDate, tconst)
DO UPDATE SET activityCount = activityCount + 1;
```

---

## 6. Sample SQL Queries

Below is a reference table of the most interesting queries in the application grouped by complexity.

| Query | Type | Tables Joined |
|-------|------|--------------|
| Search titles by keyword + filter | SELECT + WHERE | `TITLE_BASICS`, `TITLE_RATINGS` |
| Full title detail page | Multi-JOIN SELECT | `TITLE_BASICS`, `TITLE_RATINGS`, `TITLE_EPISODE`, `TITLE_PRINCIPALS`, `NAME_BASICS`, `TITLE_CREW` |
| User watchlist | JOIN SELECT | `WATCH_PROGRESS`, `TITLE_BASICS` |
| Reviews with reviewer names | JOIN SELECT | `REVIEWS`, `USERS` |
| Trending top-10 | JOIN + ORDER BY aggregate | `DAILY_ACTIVITY`, `TITLE_BASICS`, `TITLE_RATINGS` |
| Genre average rating | GROUP BY + AVG | `REVIEWS`, `TITLE_BASICS`, `TITLE_RATINGS` |
| Recommendation engine | Dynamic NOT IN + JOIN | `WATCH_PROGRESS`, `TITLE_BASICS`, `TITLE_RATINGS` |
| Finish-date prediction | COUNT with conditional | `TITLE_EPISODE`, `WATCH_PROGRESS` |
| Buddy progress comparison | Multi-self-JOIN | `WATCH_BUDDIES`, `USERS`, `WATCH_PROGRESS` |

---

## 7. System Architecture

```
Browser (React SPA)
     │  HTTP/JSON
     ▼
Flask REST API  (port 5001)
     ├── /api/titles/search        ← FIND
     ├── /api/titles/<tconst>      ← VIEW
     ├── /api/progress             ← TRACK (upsert)
     ├── /api/progress/<id>/predict← PREDICT (advanced)
     ├── /api/reviews              ← REVIEW
     ├── /api/buddies              ← CONNECT (advanced)
     ├── /api/trending             ← TRENDING (advanced)
     ├── /api/recommendations/<id> ← RECOMMEND (advanced)
     ├── /api/users                ← REGISTER
     └── /api/auth/login           ← LOGIN
          │
          ▼
   database.py  (abstraction layer)
          │
    ┌─────┴──────┐
    │            │
  SQLite       MySQL 8
 (local dev)  (Azure prod)
```

**Dual-database abstraction.** The `database.py` module transparently switches between SQLite and MySQL at startup based on the `DB_TYPE` environment variable. The `_MySQLConnectionWrapper` class translates SQLite's `?` placeholders to MySQL's `%s`. The DDL is duplicated in dialect-specific forms (`_SQLITE_DDL`, `_MYSQL_DDL`) to handle syntax differences (`ON CONFLICT` vs `ON DUPLICATE KEY UPDATE`, `TEXT` vs `VARCHAR`, `date('now')` vs `CURDATE()`).

---

## 8. Lessons Learned and Challenges

| Challenge | Solution |
|-----------|---------|
| **IMDB data volume** — raw TSV files are gigabytes; full import is impractical for a demo | Created `seed_data.py` with a curated 30-title sample and a separate `load_imdb.py` for bulk import |
| **Dual-database syntax** — SQLite and MySQL have incompatible upsert syntax | Used `if DB_TYPE == "mysql":` branches for every dialect-specific query |
| **Foreign key enforcement** — SQLite disables FK checks by default | Added `PRAGMA foreign_keys = ON` on every connection open |
| **Variable-length NOT IN** — recommendation query must exclude N already-watched titles | Dynamically generate `?,?,?` placeholder strings in Python |
| **Trending date gaps** — no activity may exist for today if the app was just seeded | Fall back to `MAX(activityDate)` when the requested date returns no rows |
| **React state freshness** — title detail page showed stale progress data | Implemented `useEffect` re-fetch on every tconst change |
| **Cross-origin in development** — React (port 3000) calling Flask (port 5001) | Configured `setupProxy.js` with `http-proxy-middleware` |

---

## 9. Conclusion

SilverTrack delivers a complete movie-and-TV-show tracking experience grounded in a well-normalised 12-table relational schema. The application meets all five basic function requirements (insert, search/list, multi-table joins, aggregates, update, delete) and three advanced functions (personalized recommendations, finish-date prediction, and community trending) that go significantly beyond CRUD. The project also demonstrates production-ready design decisions: password hashing, dual-database portability, graceful fallback logic, and a clean REST API.

Future work includes session-based authentication with JWT tokens, server-side pagination for large result sets, and an admin dashboard for bulk IMDB data import.
