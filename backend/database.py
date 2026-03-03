import os
import sqlite3

# ---------------------------------------------------------------------------
# Database configuration
# ---------------------------------------------------------------------------
# Set DB_TYPE=mysql in your environment (or .env file) to use MySQL.
# All other settings default to SQLite for local development convenience.
# ---------------------------------------------------------------------------

DB_TYPE = os.environ.get("DB_TYPE", "sqlite").lower()

# SQLite
SQLITE_PATH = os.path.join(os.path.dirname(__file__), "silvertrack.db")

# MySQL  (read from environment; see .env.example for reference)
MYSQL_HOST     = os.environ.get("MYSQL_HOST",     "localhost")
MYSQL_PORT     = int(os.environ.get("MYSQL_PORT", "3306"))
MYSQL_USER     = os.environ.get("MYSQL_USER",     "silvertrack")
MYSQL_PASSWORD = os.environ.get("MYSQL_PASSWORD", "")
MYSQL_DATABASE = os.environ.get("MYSQL_DATABASE", "silvertrack")


# ---------------------------------------------------------------------------
# Connection helpers
# ---------------------------------------------------------------------------

def get_db():
    """Return an open database connection for the configured DB_TYPE."""
    if DB_TYPE == "mysql":
        import pymysql
        import pymysql.cursors

        conn = pymysql.connect(
            host=MYSQL_HOST,
            port=MYSQL_PORT,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database=MYSQL_DATABASE,
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=False,
        )
        return _MySQLConnectionWrapper(conn)

    # Default: SQLite
    conn = sqlite3.connect(SQLITE_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


# ---------------------------------------------------------------------------
# Thin wrapper so MySQL connections expose the same interface used by the app
# (conn.execute / conn.commit / conn.close)
# ---------------------------------------------------------------------------

class _MySQLConnectionWrapper:
    """Wraps a pymysql connection to mimic the sqlite3 connection API.

    Limitation: the `?` → `%s` substitution is a simple string replacement.
    SQL that contains a literal `?` character inside a string literal or
    comment would be incorrectly modified.  All queries in this codebase use
    `?` only as a positional placeholder, so this is safe in practice.

    Note: SQLite-specific syntax such as `ON CONFLICT … DO UPDATE` is NOT
    automatically translated.  Callers that need upsert behaviour on MySQL
    must use `INSERT INTO … ON DUPLICATE KEY UPDATE` directly, or avoid
    MySQL mode until those queries are ported.
    """

    def __init__(self, conn):
        self._conn = conn
        self._cursor = conn.cursor()

    def execute(self, sql, params=()):
        # Translate SQLite positional placeholders (`?`) to MySQL-style (`%s`).
        sql_mysql = sql.replace("?", "%s")
        self._cursor.execute(sql_mysql, params)
        return self._cursor

    def commit(self):
        self._conn.commit()

    def close(self):
        self._cursor.close()
        self._conn.close()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()


# ---------------------------------------------------------------------------
# Schema creation
# ---------------------------------------------------------------------------

_SQLITE_DDL = """
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
"""

# MySQL DDL – identical structure; MySQL-compatible syntax
_MYSQL_DDL = """
    CREATE TABLE IF NOT EXISTS TITLE_BASICS (
        tconst       VARCHAR(20)  NOT NULL,
        titleType    VARCHAR(20),
        primaryTitle VARCHAR(512) NOT NULL,
        startYear    INT,
        genres       VARCHAR(255),
        PRIMARY KEY (tconst)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

    CREATE TABLE IF NOT EXISTS TITLE_RATINGS (
        tconst        VARCHAR(20) NOT NULL,
        averageRating FLOAT,
        numVotes      INT,
        PRIMARY KEY (tconst),
        FOREIGN KEY (tconst) REFERENCES TITLE_BASICS(tconst)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

    CREATE TABLE IF NOT EXISTS TITLE_EPISODE (
        tconst        VARCHAR(20) NOT NULL,
        parentTconst  VARCHAR(20) NOT NULL,
        seasonNumber  INT,
        episodeNumber INT,
        PRIMARY KEY (tconst),
        FOREIGN KEY (parentTconst) REFERENCES TITLE_BASICS(tconst)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

    CREATE TABLE IF NOT EXISTS NAME_BASICS (
        nconst              VARCHAR(20)  NOT NULL,
        primaryName         VARCHAR(255) NOT NULL,
        birthYear           INT,
        primaryProfession   VARCHAR(255),
        PRIMARY KEY (nconst)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

    CREATE TABLE IF NOT EXISTS TITLE_PRINCIPALS (
        tconst      VARCHAR(20) NOT NULL,
        nconst      VARCHAR(20) NOT NULL,
        category    VARCHAR(100),
        characters  TEXT,
        PRIMARY KEY (tconst, nconst),
        FOREIGN KEY (tconst) REFERENCES TITLE_BASICS(tconst),
        FOREIGN KEY (nconst) REFERENCES NAME_BASICS(nconst)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

    CREATE TABLE IF NOT EXISTS TITLE_CREW (
        tconst    VARCHAR(20) NOT NULL,
        directors TEXT,
        writers   TEXT,
        PRIMARY KEY (tconst),
        FOREIGN KEY (tconst) REFERENCES TITLE_BASICS(tconst)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

    CREATE TABLE IF NOT EXISTS TITLE_AKAS (
        titleId  VARCHAR(20)  NOT NULL,
        ordering INT          NOT NULL,
        title    VARCHAR(512) NOT NULL,
        region   VARCHAR(10),
        PRIMARY KEY (titleId, ordering),
        FOREIGN KEY (titleId) REFERENCES TITLE_BASICS(tconst)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

    CREATE TABLE IF NOT EXISTS USERS (
        userId   INT          NOT NULL AUTO_INCREMENT,
        username VARCHAR(100) NOT NULL,
        email    VARCHAR(255) NOT NULL,
        password VARCHAR(255) NOT NULL,
        PRIMARY KEY (userId),
        UNIQUE KEY uq_username (username),
        UNIQUE KEY uq_email    (email)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

    CREATE TABLE IF NOT EXISTS WATCH_PROGRESS (
        progressId     INT         NOT NULL AUTO_INCREMENT,
        userId         INT         NOT NULL,
        tconst         VARCHAR(20) NOT NULL,
        status         VARCHAR(30) DEFAULT 'watching',
        currentSeason  INT         DEFAULT 1,
        currentEpisode INT         DEFAULT 1,
        episodesPerDay FLOAT       DEFAULT 0,
        lastWatchedDate DATE,
        PRIMARY KEY (progressId),
        UNIQUE KEY uq_user_title (userId, tconst),
        FOREIGN KEY (userId) REFERENCES USERS(userId),
        FOREIGN KEY (tconst) REFERENCES TITLE_BASICS(tconst)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

    CREATE TABLE IF NOT EXISTS REVIEWS (
        reviewId      INT         NOT NULL AUTO_INCREMENT,
        userId        INT         NOT NULL,
        tconst        VARCHAR(20) NOT NULL,
        episodeTconst VARCHAR(20),
        rating        FLOAT,
        reviewText    TEXT,
        createdAt     DATETIME    DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (reviewId),
        FOREIGN KEY (userId) REFERENCES USERS(userId),
        FOREIGN KEY (tconst) REFERENCES TITLE_BASICS(tconst)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

    CREATE TABLE IF NOT EXISTS WATCH_BUDDIES (
        userId1 INT NOT NULL,
        userId2 INT NOT NULL,
        PRIMARY KEY (userId1, userId2),
        FOREIGN KEY (userId1) REFERENCES USERS(userId),
        FOREIGN KEY (userId2) REFERENCES USERS(userId)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

    CREATE TABLE IF NOT EXISTS DAILY_ACTIVITY (
        activityDate DATE        NOT NULL,
        tconst       VARCHAR(20) NOT NULL,
        activityCount INT        DEFAULT 0,
        PRIMARY KEY (activityDate, tconst),
        FOREIGN KEY (tconst) REFERENCES TITLE_BASICS(tconst)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
"""


def init_db():
    """Create all tables for the configured database backend."""
    if DB_TYPE == "mysql":
        import pymysql

        conn = pymysql.connect(
            host=MYSQL_HOST,
            port=MYSQL_PORT,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database=MYSQL_DATABASE,
            autocommit=True,
        )
        cur = conn.cursor()
        for statement in _MYSQL_DDL.strip().split(";"):
            stmt = statement.strip()
            if stmt:
                cur.execute(stmt)
        cur.close()
        conn.close()
        return

    # Default: SQLite
    conn = sqlite3.connect(SQLITE_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    conn.executescript(_SQLITE_DDL)
    conn.commit()
    conn.close()
