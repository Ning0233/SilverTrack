"""SilverTrack – Flask REST API backend."""
import os
from datetime import date, timedelta
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash

from database import get_db, init_db
from seed_data import seed as seed_db

FRONTEND_BUILD = os.path.join(os.path.dirname(__file__), "..", "frontend", "build")

app = Flask(__name__, static_folder=FRONTEND_BUILD, static_url_path="")
CORS(app)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def row_to_dict(row):
    return dict(row) if row else None


def rows_to_list(rows):
    return [dict(r) for r in rows]


# ---------------------------------------------------------------------------
# Startup
# ---------------------------------------------------------------------------

with app.app_context():
    init_db()
    seed_db()


# ===========================================================================
# 1. FIND – Search titles
# ===========================================================================

@app.route("/api/titles/search", methods=["GET"])
def search_titles():
    """Search titles by keyword, genre, year, or type."""
    q      = request.args.get("q", "").strip()
    genre  = request.args.get("genre", "").strip()
    year   = request.args.get("year", "").strip()
    ttype  = request.args.get("type", "").strip()

    sql    = "SELECT tb.*, tr.averageRating, tr.numVotes FROM TITLE_BASICS tb LEFT JOIN TITLE_RATINGS tr ON tb.tconst = tr.tconst WHERE 1=1"
    params = []

    if q:
        sql += " AND tb.primaryTitle LIKE ?"
        params.append(f"%{q}%")
    if genre:
        sql += " AND tb.genres LIKE ?"
        params.append(f"%{genre}%")
    if year:
        sql += " AND tb.startYear = ?"
        params.append(int(year))
    if ttype:
        sql += " AND tb.titleType = ?"
        params.append(ttype)

    sql += " ORDER BY tr.averageRating DESC LIMIT 50"

    conn = get_db()
    rows = conn.execute(sql, params).fetchall()
    conn.close()
    return jsonify(rows_to_list(rows))


# ===========================================================================
# 2. VIEW – Title details
# ===========================================================================

@app.route("/api/titles/<tconst>", methods=["GET"])
def title_detail(tconst):
    """Return full details for a single title."""
    conn = get_db()

    title = conn.execute(
        "SELECT * FROM TITLE_BASICS WHERE tconst = ?", (tconst,)
    ).fetchone()
    if not title:
        conn.close()
        return jsonify({"error": "Title not found"}), 404

    rating = conn.execute(
        "SELECT * FROM TITLE_RATINGS WHERE tconst = ?", (tconst,)
    ).fetchone()

    episodes = conn.execute(
        """SELECT te.tconst, te.seasonNumber, te.episodeNumber
           FROM TITLE_EPISODE te
           WHERE te.parentTconst = ?
           ORDER BY te.seasonNumber, te.episodeNumber""",
        (tconst,),
    ).fetchall()

    cast = conn.execute(
        """SELECT nb.nconst, nb.primaryName, tp.category, tp.characters
           FROM TITLE_PRINCIPALS tp
           JOIN NAME_BASICS nb ON tp.nconst = nb.nconst
           WHERE tp.tconst = ?""",
        (tconst,),
    ).fetchall()

    crew = conn.execute(
        "SELECT * FROM TITLE_CREW WHERE tconst = ?", (tconst,)
    ).fetchone()

    conn.close()
    return jsonify({
        "title":    row_to_dict(title),
        "rating":   row_to_dict(rating),
        "episodes": rows_to_list(episodes),
        "cast":     rows_to_list(cast),
        "crew":     row_to_dict(crew),
    })


# ===========================================================================
# 3. TRACK – Watch progress
# ===========================================================================

@app.route("/api/progress", methods=["POST"])
def upsert_progress():
    """Create or update watch progress for a user on a title."""
    data   = request.get_json(force=True)
    userId = data.get("userId")
    tconst = data.get("tconst")

    if not userId or not tconst:
        return jsonify({"error": "userId and tconst are required"}), 400

    conn = get_db()

    # Verify title exists
    title = conn.execute("SELECT tconst FROM TITLE_BASICS WHERE tconst = ?", (tconst,)).fetchone()
    if not title:
        conn.close()
        return jsonify({"error": "Title not found"}), 404

    conn.execute(
        """INSERT INTO WATCH_PROGRESS
               (userId, tconst, status, currentSeason, currentEpisode, episodesPerDay, lastWatchedDate)
           VALUES (?, ?, ?, ?, ?, ?, date('now'))
           ON CONFLICT(userId, tconst) DO UPDATE SET
               status         = excluded.status,
               currentSeason  = excluded.currentSeason,
               currentEpisode = excluded.currentEpisode,
               episodesPerDay = excluded.episodesPerDay,
               lastWatchedDate = date('now')""",
        (
            userId,
            tconst,
            data.get("status", "watching"),
            data.get("currentSeason", 1),
            data.get("currentEpisode", 1),
            data.get("episodesPerDay", 0),
        ),
    )

    # Log daily activity
    today = date.today().isoformat()
    conn.execute(
        """INSERT INTO DAILY_ACTIVITY(activityDate, tconst, activityCount) VALUES(?,?,1)
           ON CONFLICT(activityDate, tconst) DO UPDATE SET activityCount = activityCount + 1""",
        (today, tconst),
    )

    conn.commit()
    conn.close()
    return jsonify({"message": "Progress saved"})


@app.route("/api/progress/<int:user_id>", methods=["GET"])
def get_progress(user_id):
    """Return all watch progress records for a user."""
    conn = get_db()
    rows = conn.execute(
        """SELECT wp.*, tb.primaryTitle, tb.titleType, tb.genres
           FROM WATCH_PROGRESS wp
           JOIN TITLE_BASICS tb ON wp.tconst = tb.tconst
           WHERE wp.userId = ?
           ORDER BY wp.lastWatchedDate DESC""",
        (user_id,),
    ).fetchall()
    conn.close()
    return jsonify(rows_to_list(rows))


@app.route("/api/progress/<int:user_id>/<tconst>/predict", methods=["GET"])
def predict_finish(user_id, tconst):
    """Predict finish date for a TV show based on current pace."""
    conn = get_db()

    progress = conn.execute(
        "SELECT * FROM WATCH_PROGRESS WHERE userId = ? AND tconst = ?",
        (user_id, tconst),
    ).fetchone()

    if not progress:
        conn.close()
        return jsonify({"error": "No progress record found"}), 404

    total_episodes = conn.execute(
        "SELECT COUNT(*) AS cnt FROM TITLE_EPISODE WHERE parentTconst = ?", (tconst,)
    ).fetchone()["cnt"]

    episodes_per_day = progress["episodesPerDay"] or 1
    watched = conn.execute(
        """SELECT COUNT(*) AS cnt FROM TITLE_EPISODE
           WHERE parentTconst = ?
             AND (seasonNumber < ? OR (seasonNumber = ? AND episodeNumber <= ?))""",
        (tconst,
         progress["currentSeason"], progress["currentSeason"], progress["currentEpisode"]),
    ).fetchone()["cnt"]

    remaining = max(total_episodes - watched, 0)
    days_left  = remaining / episodes_per_day if episodes_per_day > 0 else None

    finish_date = None
    if days_left is not None:
        finish_date = (date.today() + timedelta(days=int(days_left))).isoformat()

    conn.close()
    return jsonify({
        "totalEpisodes":   total_episodes,
        "watchedEpisodes": watched,
        "remainingEpisodes": remaining,
        "episodesPerDay":  episodes_per_day,
        "estimatedDaysLeft": days_left,
        "predictedFinishDate": finish_date,
    })


# ===========================================================================
# 4. REVIEW – Write and read feedback
# ===========================================================================

@app.route("/api/reviews", methods=["POST"])
def add_review():
    """Add a new review."""
    data = request.get_json(force=True)
    userId = data.get("userId")
    tconst = data.get("tconst")

    if not userId or not tconst:
        return jsonify({"error": "userId and tconst are required"}), 400

    conn = get_db()
    conn.execute(
        """INSERT INTO REVIEWS(userId, tconst, episodeTconst, rating, reviewText)
           VALUES(?, ?, ?, ?, ?)""",
        (userId, tconst, data.get("episodeTconst"), data.get("rating"), data.get("reviewText")),
    )

    # Log daily activity
    today = date.today().isoformat()
    conn.execute(
        """INSERT INTO DAILY_ACTIVITY(activityDate, tconst, activityCount) VALUES(?,?,1)
           ON CONFLICT(activityDate, tconst) DO UPDATE SET activityCount = activityCount + 1""",
        (today, tconst),
    )

    conn.commit()
    conn.close()
    return jsonify({"message": "Review added"}), 201


@app.route("/api/reviews/<tconst>", methods=["GET"])
def get_reviews(tconst):
    """Return all reviews for a title."""
    conn = get_db()
    rows = conn.execute(
        """SELECT r.*, u.username
           FROM REVIEWS r
           JOIN USERS u ON r.userId = u.userId
           WHERE r.tconst = ?
           ORDER BY r.createdAt DESC""",
        (tconst,),
    ).fetchall()
    conn.close()
    return jsonify(rows_to_list(rows))


# ===========================================================================
# 5. CONNECT – Watch-buddy progress comparison
# ===========================================================================

@app.route("/api/buddies/<int:user_id>", methods=["GET"])
def get_buddies(user_id):
    """Return a list of watch-buddy usernames for a user."""
    conn = get_db()
    rows = conn.execute(
        """SELECT u.userId, u.username
           FROM WATCH_BUDDIES wb
           JOIN USERS u ON (wb.userId2 = u.userId AND wb.userId1 = ?)
                        OR (wb.userId1 = u.userId AND wb.userId2 = ?)
           WHERE u.userId != ?""",
        (user_id, user_id, user_id),
    ).fetchall()
    conn.close()
    return jsonify(rows_to_list(rows))


@app.route("/api/buddies", methods=["POST"])
def add_buddy():
    """Add a watch-buddy relationship."""
    data    = request.get_json(force=True)
    user_id = data.get("userId")
    buddy_id = data.get("buddyId")

    if not user_id or not buddy_id or user_id == buddy_id:
        return jsonify({"error": "Invalid userId or buddyId"}), 400

    u1, u2 = (user_id, buddy_id) if user_id < buddy_id else (buddy_id, user_id)
    conn = get_db()
    try:
        conn.execute("INSERT INTO WATCH_BUDDIES(userId1, userId2) VALUES(?,?)", (u1, u2))
        conn.commit()
    except Exception:
        conn.close()
        return jsonify({"error": "Buddy relationship already exists"}), 409
    conn.close()
    return jsonify({"message": "Buddy added"}), 201


@app.route("/api/buddies/compare", methods=["GET"])
def compare_buddies():
    """Compare progress between two users on the same title."""
    user_id  = request.args.get("userId",  type=int)
    buddy_id = request.args.get("buddyId", type=int)
    tconst   = request.args.get("tconst", "").strip()

    if not user_id or not buddy_id or not tconst:
        return jsonify({"error": "userId, buddyId, and tconst are required"}), 400

    conn = get_db()
    user_prog  = row_to_dict(conn.execute(
        "SELECT * FROM WATCH_PROGRESS WHERE userId = ? AND tconst = ?", (user_id,  tconst)
    ).fetchone())
    buddy_prog = row_to_dict(conn.execute(
        "SELECT * FROM WATCH_PROGRESS WHERE userId = ? AND tconst = ?", (buddy_id, tconst)
    ).fetchone())

    user_name  = row_to_dict(conn.execute(
        "SELECT username FROM USERS WHERE userId = ?", (user_id,)
    ).fetchone())
    buddy_name = row_to_dict(conn.execute(
        "SELECT username FROM USERS WHERE userId = ?", (buddy_id,)
    ).fetchone())

    conn.close()
    return jsonify({
        "user":  {"username": user_name["username"]  if user_name  else None, "progress": user_prog},
        "buddy": {"username": buddy_name["username"] if buddy_name else None, "progress": buddy_prog},
    })


# ===========================================================================
# 6. TRENDING – Daily top-watched titles
# ===========================================================================

@app.route("/api/trending", methods=["GET"])
def trending():
    """Return today's top-trending titles by activity count."""
    trend_date = request.args.get("date", date.today().isoformat())
    conn = get_db()
    rows = conn.execute(
        """SELECT da.tconst, tb.primaryTitle, tb.titleType, tb.genres,
                  tr.averageRating, da.activityCount
           FROM DAILY_ACTIVITY da
           JOIN TITLE_BASICS tb ON da.tconst = tb.tconst
           LEFT JOIN TITLE_RATINGS tr ON da.tconst = tr.tconst
           WHERE da.activityDate = ?
           ORDER BY da.activityCount DESC
           LIMIT 10""",
        (trend_date,),
    ).fetchall()
    conn.close()
    return jsonify(rows_to_list(rows))


# ===========================================================================
# 7. RECOMMENDATIONS – Personalized suggestions
# ===========================================================================

@app.route("/api/recommendations/<int:user_id>", methods=["GET"])
def recommendations(user_id):
    """Recommend titles based on genres the user has watched."""
    conn = get_db()

    # Gather genres from titles the user has tracked
    watched = conn.execute(
        "SELECT tb.genres FROM WATCH_PROGRESS wp JOIN TITLE_BASICS tb ON wp.tconst = tb.tconst WHERE wp.userId = ?",
        (user_id,),
    ).fetchall()

    watched_tconsts = [r["tconst"] for r in conn.execute(
        "SELECT tconst FROM WATCH_PROGRESS WHERE userId = ?", (user_id,)
    ).fetchall()]

    genre_counts: dict = {}
    for row in watched:
        if row["genres"]:
            for g in row["genres"].split(","):
                genre_counts[g.strip()] = genre_counts.get(g.strip(), 0) + 1

    if not genre_counts:
        # Fall back to top-rated titles
        rows = conn.execute(
            "SELECT tb.*, tr.averageRating, tr.numVotes FROM TITLE_BASICS tb LEFT JOIN TITLE_RATINGS tr ON tb.tconst = tr.tconst ORDER BY tr.averageRating DESC LIMIT 10"
        ).fetchall()
        conn.close()
        return jsonify(rows_to_list(rows))

    top_genre = max(genre_counts, key=genre_counts.get)

    placeholders = ",".join("?" * len(watched_tconsts)) if watched_tconsts else "''"
    exclude_clause = f"AND tb.tconst NOT IN ({placeholders})" if watched_tconsts else ""

    rows = conn.execute(
        f"""SELECT tb.*, tr.averageRating, tr.numVotes
            FROM TITLE_BASICS tb
            LEFT JOIN TITLE_RATINGS tr ON tb.tconst = tr.tconst
            WHERE tb.genres LIKE ?
            {exclude_clause}
            ORDER BY tr.averageRating DESC
            LIMIT 10""",
        [f"%{top_genre}%"] + watched_tconsts,
    ).fetchall()
    conn.close()
    return jsonify(rows_to_list(rows))


# ===========================================================================
# 8. USER management (minimal)
# ===========================================================================

@app.route("/api/users", methods=["GET"])
def list_users():
    conn = get_db()
    rows = conn.execute("SELECT userId, username, email FROM USERS").fetchall()
    conn.close()
    return jsonify(rows_to_list(rows))


@app.route("/api/users", methods=["POST"])
def register_user():
    data = request.get_json(force=True)
    username = data.get("username", "").strip()
    email    = data.get("email",    "").strip()
    password = data.get("password", "").strip()

    if not username or not email or not password:
        return jsonify({"error": "username, email, and password are required"}), 400

    conn = get_db()
    try:
        conn.execute(
            "INSERT INTO USERS(username, email, password) VALUES(?,?,?)",
            (username, email, generate_password_hash(password)),
        )
        conn.commit()
    except Exception:
        conn.close()
        return jsonify({"error": "Username or email already exists"}), 409
    conn.close()
    return jsonify({"message": "User registered"}), 201


# ===========================================================================
# 9. AUTH – Login
# ===========================================================================

@app.route("/api/auth/login", methods=["POST"])
def login():
    """Authenticate a user by username and password."""
    data     = request.get_json(force=True)
    username = data.get("username", "").strip()
    password = data.get("password", "").strip()

    if not username or not password:
        return jsonify({"error": "username and password are required"}), 400

    conn = get_db()
    user = conn.execute(
        "SELECT userId, username, email, password FROM USERS WHERE username = ?",
        (username,),
    ).fetchone()
    conn.close()

    if not user:
        return jsonify({"error": "Invalid username or password"}), 401

    stored = dict(user)["password"]
    # Support both werkzeug hashed passwords and legacy plain-text seeds
    valid = (
        check_password_hash(stored, password)
        if stored.startswith(("pbkdf2:", "scrypt:", "argon2:"))
        else stored == password
    )
    if not valid:
        return jsonify({"error": "Invalid username or password"}), 401

    return jsonify({
        "userId":   dict(user)["userId"],
        "username": dict(user)["username"],
        "email":    dict(user)["email"],
    })


# Serve React frontend for any non-API route
@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve_frontend(path):
    if path and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    return send_from_directory(app.static_folder, "index.html")


if __name__ == "__main__":
    debug = os.environ.get("FLASK_DEBUG", "0") == "1"
    app.run(debug=debug, port=5000)
