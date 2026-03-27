# SilverTrack – Project Sprint Plan

**Course:** CSC 4710 – Database Systems, Phase 2  
**Team:** Nameera Afrose · Tahia Islam · Taaruni Ananya · Ninglan Zhuang  

Each sprint is roughly **one week**. Tasks are sized S (small ≤ 2 h), M (medium 2–4 h), L (large > 4 h).

---

## Sprint 1 – Project Setup & Database Schema
**Goal:** Establish the development environment, agree on the schema, and create the database layer.

| # | Task | Size | Owner | Status |
|---|------|------|-------|--------|
| 1.1 | Set up Git repository and branching strategy | S | All | ✅ Done |
| 1.2 | Define and document the ER diagram | M | All | ✅ Done |
| 1.3 | Write `database.py` – create all 11 tables in SQLite | M | Ninglan | ✅ Done |
| 1.4 | Write `seed_data.py` – sample IMDb-style data (titles, cast, episodes, users) | M | Ninglan | ✅ Done |
| 1.5 | Document MySQL local connection setup | S | Nameera | ✅ Done |
| 1.6 | Update `database.py` to support MySQL via environment variables | M | Nameera | ✅ Done |
| 1.7 | Add `.env.example` with all required config variables | S | Nameera | ✅ Done |
| 1.8 | Write `requirements.txt` (Flask, flask-cors, pymysql) | S | Ninglan | ✅ Done |
| 1.9 | Write `start.sh` convenience startup script | S | Ninglan | ✅ Done |

---

## Sprint 2 – Backend API: Find & View Features
**Goal:** Implement the core read-only API endpoints so the frontend can discover and display titles.

| # | Task | Size | Owner | Status |
|---|------|------|-------|--------|
| 2.1 | `GET /api/titles/search` – filter by title, genre, year, type | M | Tahia | ✅ Done |
| 2.2 | `GET /api/titles/<tconst>` – full detail (title, rating, episodes, cast, crew) | M | Tahia | ✅ Done |
| 2.3 | `GET /api/users` – list registered users | S | Tahia | ✅ Done |
| 2.4 | `POST /api/users` – register a new user | S | Tahia | ✅ Done |
| 2.5 | Add CORS middleware so React dev server can call the API | S | Ninglan | ✅ Done |
| 2.6 | Manual API testing with curl / Postman | S | Tahia | ✅ Done |

---

## Sprint 3 – Backend API: Track & Review Features
**Goal:** Allow users to record watch progress and write reviews.

| # | Task | Size | Owner | Status |
|---|------|------|-------|--------|
| 3.1 | `POST /api/progress` – upsert watch progress (status, season, episode, pace) | M | Taaruni | ✅ Done |
| 3.2 | `GET /api/progress/<userId>` – fetch user's full watch list | S | Taaruni | ✅ Done |
| 3.3 | `GET /api/progress/<userId>/<tconst>/predict` – finish-date prediction | M | Taaruni | ✅ Done |
| 3.4 | `POST /api/reviews` – submit a review with optional rating | S | Nameera | ✅ Done |
| 3.5 | `GET /api/reviews/<tconst>` – fetch all reviews for a title | S | Nameera | ✅ Done |
| 3.6 | Log daily activity on every progress update and review | S | Taaruni | ✅ Done |

---

## Sprint 4 – Backend API: Advanced Features
**Goal:** Implement the three advanced API features (Trending, Recommendations, Watch Buddies).

| # | Task | Size | Owner | Status |
|---|------|------|-------|--------|
| 4.1 | `GET /api/trending?date=` – rank titles by daily activity count | M | Nameera | ✅ Done |
| 4.2 | `GET /api/recommendations/<userId>` – genre-affinity personalised picks | L | Nameera | ✅ Done |
| 4.3 | `GET /api/buddies/<userId>` – list watch-buddies for a user | S | Tahia | ✅ Done |
| 4.4 | `POST /api/buddies` – add a watch-buddy relationship | S | Tahia | ✅ Done |
| 4.5 | `GET /api/buddies/compare` – side-by-side progress comparison | M | Tahia | ✅ Done |
| 4.6 | Backend unit tests for all API routes | L | All | ⬜ To Do |

---

## Sprint 5 – Frontend: Core UI
**Goal:** Build the React shell and the Find / View / Track / Review pages.

| # | Task | Size | Owner | Status |
|---|------|------|-------|--------|
| 5.1 | Bootstrap Create React App project, configure proxy to Flask | S | Taaruni | ✅ Done |
| 5.2 | Design dark cinema theme (`App.css`) | M | Taaruni | ✅ Done |
| 5.3 | `App.js` – navigation shell with active-page highlighting | S | Taaruni | ✅ Done |
| 5.4 | `SearchPage.js` – keyword / genre / year / type search with card grid | M | Nameera | ✅ Done |
| 5.5 | `TitleDetail.js` – rating, episode table, cast cards, track form, review form | L | Nameera | ✅ Done |
| 5.6 | `TrackPage.js` – user's watch list, status badges, predict-finish button | M | Tahia | ✅ Done |
| 5.7 | `ReviewPage.js` – write review, browse all reviews for any title | M | Tahia | ✅ Done |

---

## Sprint 6 – Frontend: Advanced UI & Single-Port Setup
**Goal:** Complete the three advanced-feature pages and make Flask serve the React build.

| # | Task | Size | Owner | Status |
|---|------|------|-------|--------|
| 6.1 | `TrendingPage.js` – date picker + ranked trending list | M | Taaruni | ✅ Done |
| 6.2 | `RecommendPage.js` – per-user personalised recommendation grid | M | Taaruni | ✅ Done |
| 6.3 | `BuddyPage.js` – buddy list, add buddy, side-by-side compare widget | L | Ninglan | ✅ Done |
| 6.4 | Make Flask serve `frontend/build` at `/` (single-port deployment) | M | Ninglan | ✅ Done |
| 6.5 | Switch all React API calls to relative `/api` paths | S | Ninglan | ✅ Done |
| 6.6 | Build React and verify the combined app on `http://localhost:5000` | S | All | ✅ Done |

---

## Sprint 7 – Testing, Security & Polish
**Goal:** Achieve test coverage, fix security issues, and prepare for the final demo.

| # | Task | Size | Owner | Status |
|---|------|------|-------|--------|
| 7.1 | Write / update React component test (`App.test.js`) | S | Taaruni | ✅ Done |
| 7.2 | Add backend pytest tests for all 14 endpoints | L | All | ⬜ To Do |
| 7.3 | Fix Flask debug-mode security alert (use `FLASK_DEBUG` env var) | S | Ninglan | ✅ Done |
| 7.4 | CodeQL scan – resolve all Python and JavaScript alerts | M | Ninglan | ✅ Done |
| 7.5 | Input validation hardening (missing field checks on all POST routes) | M | Nameera | ⬜ To Do |
| 7.6 | Password hashing (replace plain-text storage with `werkzeug.security`) | M | Nameera | ⬜ To Do |
| 7.7 | Pagination support for search and review endpoints | M | Tahia | ⬜ To Do |
| 7.8 | README – final documentation review and API examples | S | All | ⬜ To Do |

---

## Sprint 8 – Phase 2 Deliverables & Presentation
**Goal:** Finalise the report, prepare the demo, and submit Phase 2.

| # | Task | Size | Owner | Status |
|---|------|------|-------|--------|
| 8.1 | Write Phase 2 project report (schema, ER, assumptions, features) | L | All | ⬜ To Do |
| 8.2 | Record / run live demo of all 8 features | M | All | ⬜ To Do |
| 8.3 | Peer review and final merge to main branch | S | All | ⬜ To Do |
| 8.4 | Submit deliverables on course portal | S | All | ⬜ To Do |

---

## Summary

| Sprint | Theme | Tasks | Done |
|--------|-------|-------|------|
| 1 | Setup & Schema | 9 | 9 |
| 2 | Find & View API | 6 | 6 |
| 3 | Track & Review API | 6 | 6 |
| 4 | Advanced API | 6 | 5 |
| 5 | Core UI | 7 | 7 |
| 6 | Advanced UI | 6 | 6 |
| 7 | Testing & Security | 8 | 4 |
| 8 | Deliverables | 4 | 0 |
| **Total** | | **52** | **43** |
