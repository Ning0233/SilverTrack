"""Seed the database with sample movie and TV show data."""
from database import get_db, init_db

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
    ("alice",   "alice@example.com",   "hashed_pw_alice"),
    ("bob",     "bob@example.com",     "hashed_pw_bob"),
    ("carol",   "carol@example.com",   "hashed_pw_carol"),
]

WATCH_PROGRESS = [
    # (userId, tconst, status, currentSeason, currentEpisode, episodesPerDay, lastWatchedDate)
    (1, "tt0944947", "watching",  1, 5, 2.0, "2026-03-01"),
    (1, "tt0111161", "finished",  1, 1, 0,   "2026-02-20"),
    (2, "tt0944947", "watching",  1, 8, 3.0, "2026-03-02"),
    (2, "tt4574334", "watching",  1, 3, 4.0, "2026-03-02"),
    (3, "tt0903747", "watching",  2, 2, 1.5, "2026-03-01"),
]

REVIEWS = [
    (1, "tt0111161", None, 9.5, "An absolute masterpiece. Morgan Freeman's narration is perfect."),
    (2, "tt0944947", None, 8.0, "Season 1 is fantastic. Can't wait to see what happens next."),
    (2, "tt4574334", None, 9.0, "Really good atmosphere and acting. Stranger Things hooked me instantly."),
    (3, "tt0903747", None, 9.8, "Breaking Bad is the best TV show I have ever seen."),
    (1, "tt0944947", "tt1668746", 7.5, "Episode 2 slowed down a bit but still setting up nicely."),
]

WATCH_BUDDIES = [
    (1, 2),
    (1, 3),
]

DAILY_ACTIVITY = [
    ("2026-03-02", "tt0944947", 12),
    ("2026-03-02", "tt4574334", 8),
    ("2026-03-02", "tt0903747", 7),
    ("2026-03-02", "tt3581920", 5),
    ("2026-03-02", "tt0111161", 4),
    ("2026-03-01", "tt0944947", 10),
    ("2026-03-01", "tt0903747", 9),
    ("2026-03-01", "tt0816692", 6),
]


def seed():
    init_db()
    conn = get_db()
    cur = conn.cursor()

    # Skip seeding if data already exists
    existing = cur.execute("SELECT COUNT(*) FROM TITLE_BASICS").fetchone()[0]
    if existing > 0:
        conn.close()
        return

    cur.executemany(
        "INSERT OR IGNORE INTO TITLE_BASICS(tconst,titleType,primaryTitle,startYear,genres) VALUES(?,?,?,?,?)",
        TITLE_BASICS,
    )
    cur.executemany(
        "INSERT OR IGNORE INTO TITLE_RATINGS(tconst,averageRating,numVotes) VALUES(?,?,?)",
        TITLE_RATINGS,
    )
    cur.executemany(
        "INSERT OR IGNORE INTO TITLE_EPISODE(tconst,parentTconst,seasonNumber,episodeNumber) VALUES(?,?,?,?)",
        EPISODES,
    )
    # NAME_BASICS may have duplicates in seed list – use INSERT OR IGNORE
    seen_nconst = set()
    for row in NAME_BASICS:
        if row[0] not in seen_nconst:
            seen_nconst.add(row[0])
            cur.execute(
                "INSERT OR IGNORE INTO NAME_BASICS(nconst,primaryName,birthYear,primaryProfession) VALUES(?,?,?,?)",
                row,
            )
    cur.executemany(
        "INSERT OR IGNORE INTO TITLE_PRINCIPALS(tconst,nconst,category,characters) VALUES(?,?,?,?)",
        TITLE_PRINCIPALS,
    )
    cur.executemany(
        "INSERT OR IGNORE INTO TITLE_CREW(tconst,directors,writers) VALUES(?,?,?)",
        TITLE_CREW,
    )
    cur.executemany(
        "INSERT OR IGNORE INTO USERS(username,email,password) VALUES(?,?,?)",
        USERS,
    )
    cur.executemany(
        "INSERT OR IGNORE INTO WATCH_PROGRESS(userId,tconst,status,currentSeason,currentEpisode,episodesPerDay,lastWatchedDate) VALUES(?,?,?,?,?,?,?)",
        WATCH_PROGRESS,
    )
    cur.executemany(
        "INSERT OR IGNORE INTO REVIEWS(userId,tconst,episodeTconst,rating,reviewText) VALUES(?,?,?,?,?)",
        REVIEWS,
    )
    cur.executemany(
        "INSERT OR IGNORE INTO WATCH_BUDDIES(userId1,userId2) VALUES(?,?)",
        WATCH_BUDDIES,
    )
    cur.executemany(
        "INSERT OR IGNORE INTO DAILY_ACTIVITY(activityDate,tconst,activityCount) VALUES(?,?,?)",
        DAILY_ACTIVITY,
    )

    conn.commit()
    conn.close()
    print("Database seeded successfully.")


if __name__ == "__main__":
    seed()
