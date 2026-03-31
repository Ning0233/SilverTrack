"""Seed the database with sample movie and TV show data."""
from datetime import date, timedelta
from werkzeug.security import generate_password_hash
from database import get_db, init_db, DB_TYPE


def _ph():
    """Return DB placeholder token for parameterized SQL."""
    return "%s" if DB_TYPE == "mysql" else "?"


def _insert_ignore():
    """Return DB-specific INSERT IGNORE syntax."""
    return "INSERT IGNORE" if DB_TYPE == "mysql" else "INSERT OR IGNORE"


def _select_all(cur, sql, params=()):
    """Execute a SELECT and return all rows for sqlite and pymysql cursors."""
    cur.execute(sql, params)
    return cur.fetchall()

TITLE_BASICS = [
    ("tt0111161", "movie",    "The Shawshank Redemption", 1994, "Drama"),
    ("tt0068646", "movie",    "The Godfather",             1972, "Crime,Drama"),
    ("tt0468569", "movie",    "The Dark Knight",           2008, "Action,Crime,Drama"),
    ("tt0816692", "movie",    "Interstellar",              2014, "Adventure,Drama,Sci-Fi"),
    ("tt1375666", "movie",    "Inception",                 2010, "Action,Adventure,Sci-Fi"),
    ("tt0944947", "tvSeries", "Game of Thrones",           2011, "Action,Adventure,Drama"),
    ("tt0903747", "tvSeries", "Breaking Bad",              2008, "Crime,Drama,Thriller"),
    ("tt2356777", "tvSeries", "True Detective",            2014, "Crime,Drama,Mystery"),
    ("tt0773262", "tvSeries", "Dexter",                    2006, "Crime,Drama,Mystery"),
    ("tt4574334", "tvSeries", "Stranger Things",           2016, "Drama,Fantasy,Horror"),
    ("tt3581920", "tvSeries", "The Last of Us",            2023, "Action,Adventure,Drama"),
    ("tt0108778", "tvSeries", "Friends",                   1994, "Comedy,Romance"),
]

TITLE_RATINGS = [
    ("tt0111161", 9.3, 2800000),
    ("tt0068646", 9.2, 1900000),
    ("tt0468569", 9.0, 2700000),
    ("tt0816692", 8.7, 2000000),
    ("tt1375666", 8.8, 2400000),
    ("tt0944947", 9.2, 2200000),
    ("tt0903747", 9.5, 2000000),
    ("tt2356777", 8.9,  430000),
    ("tt0773262", 8.6,  670000),
    ("tt4574334", 8.7, 1300000),
    ("tt3581920", 8.8,  540000),
    ("tt0108778", 8.9, 1000000),
]

# Episodes for TV shows  (tconst, parentTconst, season, episode)
EPISODES = [
    # Game of Thrones S1
    ("tt1480055", "tt0944947", 1, 1),
    ("tt1668746", "tt0944947", 1, 2),
    ("tt1829962", "tt0944947", 1, 3),
    ("tt1829963", "tt0944947", 1, 4),
    ("tt1829964", "tt0944947", 1, 5),
    ("tt1829965", "tt0944947", 1, 6),
    ("tt1829966", "tt0944947", 1, 7),
    ("tt1829967", "tt0944947", 1, 8),
    ("tt1829968", "tt0944947", 1, 9),
    ("tt1869761", "tt0944947", 1, 10),
    # Breaking Bad S1
    ("tt0959621", "tt0903747", 1, 1),
    ("tt1054725", "tt0903747", 1, 2),
    ("tt1054726", "tt0903747", 1, 3),
    ("tt1054727", "tt0903747", 1, 4),
    ("tt1054728", "tt0903747", 1, 5),
    ("tt1054729", "tt0903747", 1, 6),
    ("tt1054730", "tt0903747", 1, 7),
    # Breaking Bad S2
    ("tt1232194", "tt0903747", 2, 1),
    ("tt1232195", "tt0903747", 2, 2),
    ("tt1232196", "tt0903747", 2, 3),
    # Stranger Things S1
    ("tt4593118", "tt4574334", 1, 1),
    ("tt4593122", "tt4574334", 1, 2),
    ("tt4593128", "tt4574334", 1, 3),
    ("tt4767898", "tt4574334", 1, 4),
    ("tt4955642", "tt4574334", 1, 5),
    ("tt4955644", "tt4574334", 1, 6),
    ("tt4958812", "tt4574334", 1, 7),
    ("tt4958814", "tt4574334", 1, 8),
    # The Last of Us S1
    ("tt13443470", "tt3581920", 1, 1),
    ("tt13443472", "tt3581920", 1, 2),
    ("tt13443474", "tt3581920", 1, 3),
    ("tt13443476", "tt3581920", 1, 4),
    ("tt13443478", "tt3581920", 1, 5),
    ("tt13443480", "tt3581920", 1, 6),
    ("tt13443482", "tt3581920", 1, 7),
    ("tt13443484", "tt3581920", 1, 8),
    ("tt13443486", "tt3581920", 1, 9),
]

NAME_BASICS = [
    ("nm0000209", "Frank Darabont",    1959, "director,producer,writer"),
    ("nm0000338", "Morgan Freeman",    1937, "actor,producer"),
    ("nm0000351", "Tim Robbins",       1958, "actor,producer,director"),
    ("nm0000338", "Morgan Freeman",    1937, "actor,producer"),
    ("nm0000153", "James Gandolfini",  1961, "actor"),
    ("nm0001104", "Al Pacino",         1940, "actor,producer"),
    ("nm0634240", "Christopher Nolan", 1970, "director,producer,writer"),
    ("nm0000288", "Christian Bale",    1974, "actor,producer"),
    ("nm0000151", "Heath Ledger",      1979, "actor"),
    ("nm0000190", "Matthew McConaughey", 1969, "actor,producer"),
    ("nm0000138", "Leonardo DiCaprio", 1974, "actor,producer"),
    ("nm0000093", "Bryan Cranston",    1956, "actor,producer,director"),
    ("nm0001413", "Aaron Paul",        1979, "actor,producer"),
    ("nm0829032", "Millie Bobby Brown", 2004, "actress,producer"),
    ("nm0001228", "Pedro Pascal",      1975, "actor,producer"),
]

TITLE_PRINCIPALS = [
    ("tt0111161", "nm0000209", "director",   None),
    ("tt0111161", "nm0000338", "actor",      '["Red"]'),
    ("tt0111161", "nm0000351", "actor",      '["Andy Dufresne"]'),
    ("tt0068646", "nm0001104", "actor",      '["Michael Corleone"]'),
    ("tt0468569", "nm0634240", "director",   None),
    ("tt0468569", "nm0000288", "actor",      '["Bruce Wayne"]'),
    ("tt0468569", "nm0000151", "actor",      '["The Joker"]'),
    ("tt0816692", "nm0634240", "director",   None),
    ("tt0816692", "nm0000190", "actor",      '["Cooper"]'),
    ("tt1375666", "nm0634240", "director",   None),
    ("tt1375666", "nm0000138", "actor",      '["Dom Cobb"]'),
    ("tt0903747", "nm0000093", "actor",      '["Walter White"]'),
    ("tt0903747", "nm0001413", "actor",      '["Jesse Pinkman"]'),
    ("tt4574334", "nm0829032", "actress",    '["Eleven"]'),
    ("tt3581920", "nm0001228", "actor",      '["Joel"]'),
]

TITLE_CREW = [
    ("tt0111161", "nm0000209", "nm0000209"),
    ("tt0068646", "nm0000399,nm0000233", "nm0000399,nm0000233"),
    ("tt0468569", "nm0634240", "nm0634240,nm0161108"),
    ("tt0816692", "nm0634240", "nm0634240,nm0161108"),
    ("tt1375666", "nm0634240", "nm0634240"),
    ("tt0903747", "nm0243983", "nm0243983"),
    ("tt4574334", "nm0792049,nm0792050", "nm0792049,nm0792050"),
    ("tt3581920", "nm0000091", "nm0000091"),
]

USERS = [
    ("alice",   "alice@example.com",   generate_password_hash("password123", method="pbkdf2:sha256")),
    ("bob",     "bob@example.com",     generate_password_hash("password123", method="pbkdf2:sha256")),
    ("carol",   "carol@example.com",   generate_password_hash("password123", method="pbkdf2:sha256")),
]

# TRACK – watch progress per user
# (userId, tconst, status, currentSeason, currentEpisode, episodesPerDay, lastWatchedDate)
WATCH_PROGRESS = [
    # alice (id=1): variety of genres — drama movies + crime/drama TV
    (1, "tt0944947", "watching",      1, 5,  2.0, "2026-03-26"),   # GoT S1E5
    (1, "tt0111161", "finished",      1, 1,  0,   "2026-03-10"),   # Shawshank
    (1, "tt0468569", "finished",      1, 1,  0,   "2026-03-05"),   # Dark Knight
    (1, "tt0903747", "watching",      1, 3,  1.0, "2026-03-25"),   # Breaking Bad S1E3
    (1, "tt1375666", "plan_to_watch", 1, 1,  0,   "2026-03-20"),   # Inception (queued)

    # bob (id=2): ahead of alice on GoT; sci-fi + drama
    (2, "tt0944947", "watching",      1, 8,  3.0, "2026-03-27"),   # GoT S1E8 (ahead of alice)
    (2, "tt4574334", "watching",      1, 5,  4.0, "2026-03-26"),   # Stranger Things S1E5
    (2, "tt1375666", "finished",      1, 1,  0,   "2026-03-15"),   # Inception
    (2, "tt0816692", "finished",      1, 1,  0,   "2026-03-18"),   # Interstellar
    (2, "tt3581920", "watching",      1, 3,  2.0, "2026-03-27"),   # The Last of Us S1E3

    # carol (id=3): crime dramas focus
    (3, "tt0903747", "watching",      2, 2,  1.5, "2026-03-27"),   # Breaking Bad S2E2
    (3, "tt3581920", "watching",      1, 5,  2.0, "2026-03-26"),   # Last of Us S1E5
    (3, "tt0068646", "finished",      1, 1,  0,   "2026-03-12"),   # The Godfather
    (3, "tt0111161", "finished",      1, 1,  0,   "2026-03-08"),   # Shawshank
    (3, "tt0773262", "watching",      1, 4,  1.0, "2026-03-25"),   # Dexter S1E4
]

# REVIEW – written while watching or after; some episode-specific
# (userId, tconst, episodeTconst, rating, reviewText)
REVIEWS = [
    # alice reviews
    (1, "tt0111161", None,         9.5, "An absolute masterpiece. Morgan Freeman's narration is perfect."),
    (1, "tt0468569", None,         9.0, "Heath Ledger's Joker is one of cinema's greatest performances."),
    (1, "tt0944947", "tt1668746",  7.5, "Episode 2 slowed down a bit but the world-building is great."),
    (1, "tt0903747", None,         8.5, "The first few episodes feel slow but Walter's arc is fascinating."),

    # bob reviews
    (2, "tt0944947", None,         8.0, "Season 1 is fantastic. The Red Wedding is coming and I'm not ready."),
    (2, "tt4574334", None,         9.0, "Really good atmosphere and acting. Hooked from episode one."),
    (2, "tt1375666", None,         9.5, "Mind-bending from start to finish. A true sci-fi masterpiece."),
    (2, "tt0816692", None,         9.2, "Visually stunning. The docking scene gave me chills."),
    (2, "tt3581920", "tt13443472", 9.3, "Episode 2 (Long Long Time) might be the best episode of TV ever made."),

    # carol reviews
    (3, "tt0903747", None,         9.8, "Breaking Bad is the greatest character study in television history."),
    (3, "tt0068646", None,         9.0, "A cinematic masterpiece. Brando is unforgettable."),
    (3, "tt3581920", None,         9.2, "Pedro Pascal is perfect as Joel. Emotional and gripping."),
    (3, "tt0111161", None,         9.4, "A timeless story about hope. Everyone should watch this."),
    (3, "tt0773262", "tt0773262",  8.0, "Dexter is darkly comedic and I love the premise."),
]

# CONNECT – buddy relationships (userId1 < userId2 always)
WATCH_BUDDIES = [
    (1, 2),   # alice ↔ bob  (both watching GoT – great for Compare)
    (1, 3),   # alice ↔ carol
    (2, 3),   # bob   ↔ carol
]

def build_daily_activity_seed():
    """Build trending seed data for today and the prior two days."""
    today = date.today()

    templates = [
        # day offset, tconst, activityCount
        (0, "tt0944947", 15),
        (0, "tt3581920", 12),
        (0, "tt4574334", 9),
        (0, "tt0903747", 8),
        (0, "tt0111161", 6),
        (0, "tt1375666", 5),
        (0, "tt0816692", 4),
        (0, "tt0773262", 3),
        (1, "tt0944947", 12),
        (1, "tt4574334", 8),
        (1, "tt0903747", 9),
        (1, "tt3581920", 7),
        (1, "tt0111161", 5),
        (2, "tt0903747", 11),
        (2, "tt0816692", 6),
        (2, "tt0944947", 10),
        (2, "tt1375666", 4),
    ]

    return [
        ((today - timedelta(days=offset)).isoformat(), tconst, count)
        for offset, tconst, count in templates
    ]


def build_user_daily_activity_seed():
    """Build user-specific activity rows for personalized trending."""
    today = date.today()

    templates = [
        # day offset, userId, tconst, activityCount
        (0, 1, "tt0944947", 3),
        (0, 1, "tt0903747", 2),
        (0, 1, "tt3581920", 1),
        (0, 2, "tt0944947", 4),
        (0, 2, "tt4574334", 3),
        (0, 2, "tt3581920", 2),
        (0, 3, "tt0903747", 4),
        (0, 3, "tt0773262", 2),
        (0, 3, "tt3581920", 1),
        (1, 1, "tt0944947", 2),
        (1, 1, "tt0111161", 1),
        (1, 2, "tt4574334", 2),
        (1, 2, "tt3581920", 1),
        (1, 3, "tt0903747", 3),
        (1, 3, "tt0068646", 1),
        (2, 1, "tt0903747", 2),
        (2, 2, "tt0944947", 2),
        (2, 3, "tt3581920", 2),
    ]

    return [
        ((today - timedelta(days=offset)).isoformat(), user_id, tconst, count)
        for offset, user_id, tconst, count in templates
    ]


def _upsert_daily_activity(cur, activity_date, tconst, increment_by):
    if DB_TYPE == "mysql":
        cur.execute(
            """INSERT INTO DAILY_ACTIVITY(activityDate, tconst, activityCount)
               VALUES(%s, %s, %s)
               ON DUPLICATE KEY UPDATE activityCount = activityCount + VALUES(activityCount)""",
            (activity_date, tconst, increment_by),
        )
        return

    cur.execute(
        """INSERT INTO DAILY_ACTIVITY(activityDate, tconst, activityCount)
           VALUES(?,?,?)
           ON CONFLICT(activityDate, tconst) DO UPDATE
           SET activityCount = activityCount + excluded.activityCount""",
        (activity_date, tconst, increment_by),
    )


def _upsert_user_daily_activity(cur, activity_date, user_id, tconst, increment_by):
    if DB_TYPE == "mysql":
        cur.execute(
            """INSERT INTO USER_DAILY_ACTIVITY(activityDate, userId, tconst, activityCount)
               VALUES(%s, %s, %s, %s)
               ON DUPLICATE KEY UPDATE activityCount = activityCount + VALUES(activityCount)""",
            (activity_date, user_id, tconst, increment_by),
        )
        return

    cur.execute(
        """INSERT INTO USER_DAILY_ACTIVITY(activityDate, userId, tconst, activityCount)
           VALUES(?,?,?,?)
           ON CONFLICT(activityDate, userId, tconst) DO UPDATE
           SET activityCount = activityCount + excluded.activityCount""",
        (activity_date, user_id, tconst, increment_by),
    )


def backfill_current_user_activity(cur):
    """Add synthetic activity for current users so trending has realistic global counts."""
    today = date.today().isoformat()

    progress_rows = _select_all(cur, "SELECT userId, tconst, status FROM WATCH_PROGRESS")
    review_rows = _select_all(cur, "SELECT userId, tconst FROM REVIEWS")
    all_users = _select_all(cur, "SELECT userId FROM USERS ORDER BY userId")
    fallback_titles = _select_all(
        cur,
        "SELECT tconst FROM TITLE_BASICS ORDER BY startYear DESC LIMIT 3",
    )

    users_with_today_activity = {
        row["userId"]
        for row in _select_all(
            cur,
            f"SELECT DISTINCT userId FROM USER_DAILY_ACTIVITY WHERE activityDate = {_ph()}",
            (today,),
        )
    }

    active_user_ids = set()

    for row in progress_rows:
        status = row["status"]
        if status == "watching":
            delta = 2
        elif status == "finished":
            delta = 1
        else:
            delta = 1

        user_id = row["userId"]
        tconst = row["tconst"]
        if user_id in users_with_today_activity:
            continue
        active_user_ids.add(user_id)
        _upsert_user_daily_activity(cur, today, user_id, tconst, delta)
        _upsert_daily_activity(cur, today, tconst, delta)

    for row in review_rows:
        user_id = row["userId"]
        tconst = row["tconst"]
        if user_id in users_with_today_activity:
            continue
        active_user_ids.add(user_id)
        _upsert_user_daily_activity(cur, today, user_id, tconst, 1)
        _upsert_daily_activity(cur, today, tconst, 1)

    # If a user has no progress/review yet, give a minimal bootstrap activity.
    fallback_tconsts = [r["tconst"] for r in fallback_titles]
    for user_row in all_users:
        user_id = user_row["userId"]
        if user_id in active_user_ids or user_id in users_with_today_activity:
            continue
        for tconst in fallback_tconsts[:2]:
            _upsert_user_daily_activity(cur, today, user_id, tconst, 1)
            _upsert_daily_activity(cur, today, tconst, 1)


def seed():
    init_db()
    conn = get_db()
    cur = conn.cursor()

    # Skip core dataset seeding if title data already exists
    result = cur.execute("SELECT COUNT(*) FROM TITLE_BASICS")
    row = cur.fetchone()
    existing = list(row.values())[0]
    insert_ignore = _insert_ignore()
    ph = _ph()

    if existing == 0:
        cur.executemany(
            f"{insert_ignore} INTO TITLE_BASICS(tconst,titleType,primaryTitle,startYear,genres) VALUES({ph},{ph},{ph},{ph},{ph})",
            TITLE_BASICS,
        )
        cur.executemany(
            f"{insert_ignore} INTO TITLE_RATINGS(tconst,averageRating,numVotes) VALUES({ph},{ph},{ph})",
            TITLE_RATINGS,
        )
        cur.executemany(
            f"{insert_ignore} INTO TITLE_EPISODE(tconst,parentTconst,seasonNumber,episodeNumber) VALUES({ph},{ph},{ph},{ph})",
            EPISODES,
        )
        # NAME_BASICS may have duplicates in seed list – use INSERT OR IGNORE
        seen_nconst = set()
        for row in NAME_BASICS:
            if row[0] not in seen_nconst:
                seen_nconst.add(row[0])
                cur.execute(
                    f"{insert_ignore} INTO NAME_BASICS(nconst,primaryName,birthYear,primaryProfession) VALUES({ph},{ph},{ph},{ph})",
                    row,
                )
        cur.executemany(
            f"{insert_ignore} INTO TITLE_PRINCIPALS(tconst,nconst,category,characters) VALUES({ph},{ph},{ph},{ph})",
            TITLE_PRINCIPALS,
        )
        cur.executemany(
            f"{insert_ignore} INTO TITLE_CREW(tconst,directors,writers) VALUES({ph},{ph},{ph})",
            TITLE_CREW,
        )
        cur.executemany(
            f"{insert_ignore} INTO USERS(username,email,password) VALUES({ph},{ph},{ph})",
            USERS,
        )
        cur.executemany(
            f"{insert_ignore} INTO WATCH_PROGRESS(userId,tconst,status,currentSeason,currentEpisode,episodesPerDay,lastWatchedDate) VALUES({ph},{ph},{ph},{ph},{ph},{ph},{ph})",
            WATCH_PROGRESS,
        )
        cur.executemany(
            f"{insert_ignore} INTO REVIEWS(userId,tconst,episodeTconst,rating,reviewText) VALUES({ph},{ph},{ph},{ph},{ph})",
            REVIEWS,
        )
        cur.executemany(
            f"{insert_ignore} INTO WATCH_BUDDIES(userId1,userId2) VALUES({ph},{ph})",
            WATCH_BUDDIES,
        )

    # Always ensure recent fake trending data exists for the UI demo.
    cur.executemany(
        f"{insert_ignore} INTO DAILY_ACTIVITY(activityDate,tconst,activityCount) VALUES({ph},{ph},{ph})",
        build_daily_activity_seed(),
    )
    cur.executemany(
        f"{insert_ignore} INTO USER_DAILY_ACTIVITY(activityDate,userId,tconst,activityCount) VALUES({ph},{ph},{ph},{ph})",
        build_user_daily_activity_seed(),
    )

    # Ensure global trending reflects activity from current users in this database.
    backfill_current_user_activity(cur)

    conn.commit()
    conn.close()
    print("Database seeded successfully.")


if __name__ == "__main__":
    seed()
