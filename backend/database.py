import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "silvertrack.db")


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    conn = get_db()
    cur = conn.cursor()

    cur.executescript("""
        CREATE TABLE IF NOT EXISTS TITLE_BASICS (
            tconst      TEXT PRIMARY KEY,
            titleType   TEXT,
            primaryTitle TEXT NOT NULL,
            startYear   INTEGER,
            genres      TEXT
        );

        CREATE TABLE IF NOT EXISTS TITLE_RATINGS (
            tconst          TEXT PRIMARY KEY,
            averageRating   REAL,
            numVotes        INTEGER,
            FOREIGN KEY (tconst) REFERENCES TITLE_BASICS(tconst)
        );

        CREATE TABLE IF NOT EXISTS TITLE_EPISODE (
            tconst          TEXT PRIMARY KEY,
            parentTconst    TEXT NOT NULL,
            seasonNumber    INTEGER,
            episodeNumber   INTEGER,
            FOREIGN KEY (parentTconst) REFERENCES TITLE_BASICS(tconst)
        );

        CREATE TABLE IF NOT EXISTS NAME_BASICS (
            nconst          TEXT PRIMARY KEY,
            primaryName     TEXT NOT NULL,
            birthYear       INTEGER,
            primaryProfession TEXT
        );

        CREATE TABLE IF NOT EXISTS TITLE_PRINCIPALS (
            tconst      TEXT NOT NULL,
            nconst      TEXT NOT NULL,
            category    TEXT,
            characters  TEXT,
            PRIMARY KEY (tconst, nconst),
            FOREIGN KEY (tconst) REFERENCES TITLE_BASICS(tconst),
            FOREIGN KEY (nconst) REFERENCES NAME_BASICS(nconst)
        );

        CREATE TABLE IF NOT EXISTS TITLE_CREW (
            tconst      TEXT PRIMARY KEY,
            directors   TEXT,
            writers     TEXT,
            FOREIGN KEY (tconst) REFERENCES TITLE_BASICS(tconst)
        );

        CREATE TABLE IF NOT EXISTS TITLE_AKAS (
            titleId     TEXT NOT NULL,
            ordering    INTEGER NOT NULL,
            title       TEXT NOT NULL,
            region      TEXT,
            PRIMARY KEY (titleId, ordering),
            FOREIGN KEY (titleId) REFERENCES TITLE_BASICS(tconst)
        );

        CREATE TABLE IF NOT EXISTS USERS (
            userId      INTEGER PRIMARY KEY AUTOINCREMENT,
            username    TEXT UNIQUE NOT NULL,
            email       TEXT UNIQUE NOT NULL,
            password    TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS WATCH_PROGRESS (
            progressId      INTEGER PRIMARY KEY AUTOINCREMENT,
            userId          INTEGER NOT NULL,
            tconst          TEXT NOT NULL,
            status          TEXT DEFAULT 'watching',
            currentSeason   INTEGER DEFAULT 1,
            currentEpisode  INTEGER DEFAULT 1,
            episodesPerDay  REAL DEFAULT 0,
            lastWatchedDate TEXT,
            UNIQUE(userId, tconst),
            FOREIGN KEY (userId) REFERENCES USERS(userId),
            FOREIGN KEY (tconst) REFERENCES TITLE_BASICS(tconst)
        );

        CREATE TABLE IF NOT EXISTS REVIEWS (
            reviewId        INTEGER PRIMARY KEY AUTOINCREMENT,
            userId          INTEGER NOT NULL,
            tconst          TEXT NOT NULL,
            episodeTconst   TEXT,
            rating          REAL,
            reviewText      TEXT,
            createdAt       TEXT DEFAULT (datetime('now')),
            FOREIGN KEY (userId) REFERENCES USERS(userId),
            FOREIGN KEY (tconst) REFERENCES TITLE_BASICS(tconst)
        );

        CREATE TABLE IF NOT EXISTS WATCH_BUDDIES (
            userId1     INTEGER NOT NULL,
            userId2     INTEGER NOT NULL,
            PRIMARY KEY (userId1, userId2),
            FOREIGN KEY (userId1) REFERENCES USERS(userId),
            FOREIGN KEY (userId2) REFERENCES USERS(userId)
        );

        CREATE TABLE IF NOT EXISTS DAILY_ACTIVITY (
            activityDate    TEXT NOT NULL,
            tconst          TEXT NOT NULL,
            activityCount   INTEGER DEFAULT 0,
            PRIMARY KEY (activityDate, tconst),
            FOREIGN KEY (tconst) REFERENCES TITLE_BASICS(tconst)
        );
    """)
    conn.commit()
    conn.close()
