# SilverTrack — Demo Script (Stage 5)

**Application:** SilverTrack — Movie & TV-Show Tracker  
**Course:** CSC 4710 – Database Systems  
**Team:** Nameera Afrose · Tahia Islam · Taaruni Ananya · Ninglan Zhuang  
**Total Demo Time:** ~20 minutes

---

## Pre-Demo Checklist

Before starting the recording, confirm:

- [ ] `bash start.sh` has been run; backend is running on port 5001
- [ ] Browser is open to `http://localhost:5001` (or the React dev server at `:3000`)
- [ ] The database has been seeded (`seed_data.py` ran at startup — check terminal for "Seeded")
- [ ] At least two demo accounts exist: `alice` / `alice123` and `bob` / `bob123`
- [ ] Browser zoom is at a readable level (125% recommended for screen recording)
- [ ] Terminal window is open (you will paste SQL queries there for illustration)

---

## Demo Outline

| Segment | Content | Time |
|---------|---------|------|
| 0 | Introduction | 1 min |
| 1 | Insert Records | 3 min |
| 2 | Search / List Results | 2 min |
| 3 | Interesting Queries | 4 min |
| 4 | Update Records | 1.5 min |
| 5 | Delete Records | 1.5 min |
| 6 | Advanced — Recommendations | 2 min |
| 7 | Advanced — Finish-Date Prediction | 2 min |
| 8 | Advanced — Community Trending | 2 min |
| 9 | Wrap-up | 1 min |

---

## Segment 0 — Introduction (1 min)

**[Narrator]**  
> "Welcome to our demo of SilverTrack, a platform-agnostic movie and TV-show tracker backed by the full IMDB title catalogue. Our database contains twelve tables — seven IMDB reference tables and five user-generated tables — running on SQLite locally and Azure MySQL in production. We'll walk through all five basic database functions and then showcase three advanced features."

**[Show the app home screen / login page.]**

---

## Segment 1 — Insert Records (3 min)

### 1a. Register a new user (INSERT into USERS)

**[Navigate to the Login page → click "Register" tab.]**

**[Narrator]**  
> "First, we'll insert a new user record. We fill in a username, email, and password. On submit, the backend hashes the password with PBKDF2-SHA256 and executes an INSERT into the USERS table."

**[Type in the form:]**
- Username: `carol`
- Email: `carol@example.com`
- Password: `carol123`

**[Click Register. Show the success message.]**

**[Show the underlying SQL in the report:]**
```sql
INSERT INTO USERS(username, email, password)
VALUES ('carol', 'carol@example.com', '<pbkdf2-hash>');
```

---

### 1b. Save watch progress (INSERT/UPSERT into WATCH_PROGRESS)

**[Log in as `alice` / `alice123`.]**  
**[Use the Search page to find "Breaking Bad".]**  
**[Click on "Breaking Bad" to open its title detail page.]**

**[Narrator]**  
> "Now we'll track Alice's progress on Breaking Bad. We set the status to 'Watching', mark Season 3 Episode 7, and enter a pace of 2 episodes per day. This fires a POST to /api/progress which performs a database upsert — inserting a new row if this is the first time, or updating the existing one if Alice already has a record."

**[Fill in the Track form:]**
- Status: `watching`
- Season: `3`
- Episode: `7`
- Episodes/day: `2`

**[Click Save Progress.]**

---

### 1c. Submit a review (INSERT into REVIEWS)

**[Still on the Breaking Bad detail page, scroll to the Reviews section.]**

**[Narrator]**  
> "Next, we'll insert a review. Alice rates Breaking Bad 9.5 out of 10 and writes a short text review. The backend inserts this into the REVIEWS table and simultaneously increments the DAILY_ACTIVITY counter so the title's trending score goes up."

**[Type:]**
- Rating: `9.5`
- Review: `"One of the greatest shows ever made. Masterful storytelling."`

**[Click Submit Review. Show the review appearing in the list.]**

---

## Segment 2 — Search and List Results (2 min)

### 2a. Keyword + filter search

**[Navigate to the Search page.]**

**[Narrator]**  
> "SilverTrack's search queries two IMDB tables in one LEFT JOIN — TITLE_BASICS for metadata and TITLE_RATINGS for scores — returning up to 50 results sorted by average rating."

**[Demonstrate each filter:]**
1. Type `"The"` in the keyword box → hit Search → show mixed results
2. Add Genre `"Drama"` → re-search → notice results narrow
3. Change Type to `"tvSeries"` → re-search → only TV shows appear
4. Add Year `"2008"` → re-search → notice further filtering

**[Narrator]**  
> "The SQL query builds a dynamic WHERE clause based on whichever filters are active, then joins in TITLE_RATINGS to sort by rating."

---

### 2b. List user's watchlist

**[Navigate to the Track page (My Watchlist).]**

**[Narrator]**  
> "Alice's watchlist joins WATCH_PROGRESS with TITLE_BASICS to show title name, type, genres, current position, and last-watched date — ordered by most recently watched."

**[Show Alice's watchlist with at least 2–3 entries.]**

---

## Segment 3 — Interesting Queries (4 min)

### 3a. Multi-table JOIN: Full title detail page

**[Click on any title from the watchlist — e.g., Breaking Bad.]**

**[Narrator]**  
> "The title detail page is powered by five simultaneous queries joining six tables. Here you can see the title's IMDB rating from TITLE_RATINGS, the full cast and their character names resolved through the TITLE_PRINCIPALS bridge table to NAME_BASICS, director and writer names from TITLE_CREW, and the complete ordered episode list from TITLE_EPISODE. This is our most complex multi-JOIN query."

**[Point out on screen: rating stars, cast list with roles, episode list scrolling through seasons.]**

---

### 3b. JOIN query: Reviews with reviewer username

**[Scroll to the Reviews section on the same title page.]**

**[Narrator]**  
> "All reviews for this title are fetched by joining REVIEWS with USERS so we display the reviewer's username alongside their rating and text. Results are ordered by newest first."

```sql
SELECT r.rating, r.reviewText, r.createdAt, u.username
FROM   REVIEWS r
JOIN   USERS u ON r.userId = u.userId
WHERE  r.tconst = 'tt0903747'
ORDER BY r.createdAt DESC;
```

---

### 3c. AGGREGATE query: Community Trending (activity counts)

**[Navigate to the Trending page.]**

**[Narrator]**  
> "Our trending algorithm is an aggregate query. DAILY_ACTIVITY stores a running activity count per (date, title) pair — incremented on every watch-progress save and review submit. The trending page ranks the top 10 titles by activity count for today, joining in TITLE_BASICS and TITLE_RATINGS for display. This is an aggregate in that the activityCount column is the result of many incremental write operations, producing a total-engagement score."

**[Show the trending list — at least the top 5 entries with their scores.]**

---

### 3d. AGGREGATE query: Average rating per genre (SQL demo in terminal)

**[Switch to terminal window. Open the SQLite DB.]**

```bash
cd backend
sqlite3 silvertrack.db
```

```sql
SELECT SUBSTR(tb.genres, 1, INSTR(tb.genres || ',', ',') - 1) AS primaryGenre,
       COUNT(r.reviewId)              AS reviewCount,
       ROUND(AVG(r.rating), 2)        AS avgUserRating,
       ROUND(AVG(tr.averageRating), 2) AS avgImdbRating
FROM   REVIEWS r
JOIN   TITLE_BASICS  tb ON r.tconst = tb.tconst
LEFT JOIN TITLE_RATINGS tr ON r.tconst = tr.tconst
WHERE  r.rating IS NOT NULL
GROUP BY primaryGenre
ORDER BY reviewCount DESC;
```

**[Narrator]**  
> "This aggregate query groups user-submitted reviews by their title's primary genre, showing review count, average user rating, and average IMDB rating side by side. It demonstrates GROUP BY, AVG, COUNT, and a multi-table JOIN."

**[Show results in terminal, then exit SQLite.]**

---

## Segment 4 — Update Records (1.5 min)

**[In the browser, open Breaking Bad detail page. Alice is at S3E7.]**

**[Narrator]**  
> "To update a record, Alice advances her progress. She's now at Season 4, Episode 2, and picked up her pace to 3 episodes a day. Submitting the form calls the same POST /api/progress endpoint, which fires an ON CONFLICT … DO UPDATE upsert, updating all changed columns in place."

**[Change the form:]**
- Season: `4`
- Episode: `2`
- Episodes/day: `3`

**[Click Save Progress. Return to Track page to confirm the change is reflected.]**

**[Narrator]**  
> "The watchlist now shows Season 4, Episode 2, and the lastWatchedDate has been refreshed to today."

---

## Segment 5 — Delete Records (1.5 min)

**[Open terminal, show direct DELETE for clarity.]**

```bash
sqlite3 backend/silvertrack.db
```

**[Narrator]**  
> "Deletion is demonstrated by removing the review Alice just submitted. The DELETE statement targets a specific reviewId and includes a userId ownership check to prevent deleting another user's review."

```sql
-- See Alice's review IDs
SELECT reviewId, userId, rating, reviewText
FROM   REVIEWS
WHERE  tconst = 'tt0903747';

-- Delete it (ownership check included)
DELETE FROM REVIEWS
WHERE  reviewId = 1
  AND  userId   = 1;

-- Confirm it's gone
SELECT COUNT(*) FROM REVIEWS WHERE tconst = 'tt0903747';
```

**[Show count drops by 1. Return to browser, refresh the title page — the review no longer appears.]**

Also demonstrate removing a watch-buddy:

```sql
DELETE FROM WATCH_BUDDIES
WHERE (userId1 = 1 AND userId2 = 2)
   OR (userId1 = 2 AND userId2 = 1);
```

---

## Segment 6 — Advanced Function 1: Personalized Recommendations (2 min)

**[Navigate to the Recommend page (logged in as Alice).]**

**[Narrator]**  
> "Our first advanced function is a personalized recommendation engine. It analyzes every title Alice has tracked, extracts genre tokens from the comma-separated genres column, and tallies their frequency. Alice watches mostly Drama, so the algorithm queries the top-rated Drama titles she hasn't yet tracked — using a dynamically generated NOT IN clause — and returns them ranked by IMDB rating."

**[Show the recommendation list on screen.]**

**[Narrator]**  
> "What makes this advanced: it requires multi-step query logic, runtime SQL generation with variable-length placeholder lists, and fallback handling for users with no history. Unlike static 'top-rated' lists, this is unique to each user's viewing profile and computed entirely from their own data — no external API needed."

**[Show the algorithm in terminal:]**
```bash
# Show the genre-frequency logic in app.py (line 456-460)
grep -n "genre_counts" backend/app.py
```

---

## Segment 7 — Advanced Function 2: Finish-Date Prediction (2 min)

**[Return to the Breaking Bad title detail page, logged in as Alice (S4E2, 3 eps/day).]**

**[Narrator]**  
> "Our second advanced function predicts when Alice will finish the show. The backend queries TITLE_EPISODE to count all 62 episodes in Breaking Bad, then runs a conditional COUNT to find how many episodes are before her current position — Season 4, Episode 2. The remainder divided by her pace of 3 episodes per day gives the days left, projected onto today's date."

**[Click the 'Predict Finish Date' button. Show the result: e.g., "You'll finish in ~14 days on 2026-04-19."]**

**[Narrator]**  
> "The prediction query uses a compound WHERE clause combining season comparison with episode comparison — a pattern that requires careful SQL reasoning about partial season progress."

```sql
SELECT COUNT(*) AS watched
FROM   TITLE_EPISODE
WHERE  parentTconst = 'tt0903747'
  AND  (seasonNumber < 4
        OR (seasonNumber = 4 AND episodeNumber <= 2));
```

**[Narrator]**  
> "This feature is novel — mainstream trackers show you static progress bars but none provide a personalized, data-driven completion forecast."

---

## Segment 8 — Advanced Function 3: Community Trending (2 min)

**[Navigate to the Trending page.]**

**[Narrator]**  
> "Our third advanced function is community-driven daily trending. Every time any user saves progress or submits a review, the backend atomically increments that title's counter in DAILY_ACTIVITY using an upsert. At query time we JOIN three tables and order by the accumulated activity score."

**[Point out the top trending titles and their scores.]**

**[Narrator]**  
> "We store a two-level activity table — global DAILY_ACTIVITY and per-user USER_DAILY_ACTIVITY — enabling future features like 'most active friend today.' If no activity exists for today (e.g., the database was just seeded), the system falls back to the most recent date that has data, so the page is never empty."

**[Show the date fallback by querying a past date:]**

```bash
# In browser address bar or curl:
curl "http://localhost:5001/api/trending?date=2026-01-01"
# Shows results from the most recent seeded date instead of empty
```

**[Narrator]**  
> "Unlike static popularity rankings, our trending captures engagement momentum — a sleeper hit suddenly binge-watched by the community will rise to the top even if its IMDB rating is modest."

---

## Segment 9 — Wrap-up (1 min)

**[Return to the home/login page for a clean closing frame.]**

**[Narrator]**  
> "That concludes our SilverTrack demo. We've shown all five basic database operations — insert, search and list, multi-table join queries, aggregate queries, update, and delete — as well as three technically advanced features: a personalized genre-affinity recommendation engine, a finish-date prediction algorithm, and a community trending system. Our 12-table schema runs on both SQLite for development and Azure MySQL in production, with a transparent abstraction layer that requires no code changes to switch. Thank you for watching."

---

## Appendix — Quick Reference: API Endpoints Used in Demo

| Segment | Endpoint | Method | Action |
|---------|----------|--------|--------|
| 1a | `/api/users` | POST | Register user |
| 1b | `/api/progress` | POST | Save/upsert watch progress |
| 1c | `/api/reviews` | POST | Submit review |
| 2a | `/api/titles/search?q=&genre=&year=&type=` | GET | Search titles |
| 2b | `/api/progress/<userId>` | GET | List watchlist |
| 3a | `/api/titles/<tconst>` | GET | Full title detail |
| 3b | `/api/reviews/<tconst>` | GET | List reviews |
| 3c | `/api/trending?date=` | GET | Trending titles |
| 4  | `/api/progress` | POST | Update watch progress (upsert) |
| 5  | SQL direct | DELETE | Delete review / buddy |
| 6  | `/api/recommendations/<userId>` | GET | Personalized recommendations |
| 7  | `/api/progress/<userId>/<tconst>/predict` | GET | Finish-date prediction |
| 8  | `/api/trending` | GET | Community trending |

## Appendix — Demo Account Credentials

| Username | Password | Role |
|----------|----------|------|
| `alice` | `alice123` | Primary demo user |
| `bob` | `bob123` | Buddy comparison user |
| `carol` | `carol123` | Newly registered in demo (Segment 1a) |
