# SilverTrack – Frontend

React single-page application that powers the SilverTrack movie and TV-show tracker.

---

## Table of Contents

1. [Tech Stack](#tech-stack)
2. [Project Structure](#project-structure)
3. [Architecture Overview](#architecture-overview)
4. [Authentication & UserContext](#authentication--usercontext)
5. [Navigation & Routing](#navigation--routing)
6. [Component Reference](#component-reference)
   - [LoginPage](#loginpage)
   - [SearchPage](#searchpage)
   - [TitleDetail](#titledetail)
   - [TrackPage](#trackpage)
   - [ReviewPage](#reviewpage)
   - [TrendingPage](#trendingpage)
   - [RecommendPage](#recommendpage)
   - [BuddyPage](#buddypage)
7. [Styling Guide](#styling-guide)
8. [API Communication](#api-communication)
9. [Running the Frontend](#running-the-frontend)

---

## Tech Stack

| Concern | Technology |
|---------|------------|
| Framework | React 19 (Create React App) |
| State | `useState` / `useEffect` hooks |
| Global state | React Context (`UserContext`) |
| Styling | Plain CSS (`App.css`) — dark theme |
| HTTP | Native `fetch` (proxied to `http://localhost:5000`) |
| Testing | Jest + React Testing Library |

---

## Project Structure

```
frontend/
├── public/               # Static assets served by CRA
├── src/
│   ├── App.js            # Root component – layout, nav, page routing
│   ├── App.css           # Global stylesheet (shared classes & theme)
│   ├── UserContext.js    # React context that holds the logged-in user
│   ├── index.js          # CRA entry point
│   └── components/
│       ├── LoginPage.js      # Sign-in / register form
│       ├── SearchPage.js     # Title search with filters
│       ├── TitleDetail.js    # Full title view + tracking + reviews
│       ├── TrackPage.js      # User's personal watch-progress list
│       ├── ReviewPage.js     # Write and browse reviews
│       ├── TrendingPage.js   # Daily trending titles
│       ├── RecommendPage.js  # Personalised recommendations
│       └── BuddyPage.js      # Watch-buddy management + progress comparison
├── package.json
└── package-lock.json
```

---

## Architecture Overview

```
┌─────────────────────────────────────────────────┐
│  App.js  (root)                                  │
│  ┌──────────────────────┐  ┌──────────────────┐ │
│  │  UserContext.Provider│  │  <header> nav    │ │
│  │  (currentUser)       │  │  (NAV_ITEMS)     │ │
│  └──────────────────────┘  └──────────────────┘ │
│                                                  │
│  Page rendered via renderPage() switch:          │
│    search | detail | track | review              │
│    trending | recommend | buddy                  │
└─────────────────────────────────────────────────┘
         │  all components call
         ▼
    /api  (proxied → Flask :5000)
```

There is no client-side router library. Navigation is handled entirely with a `page` state string in `App.js` and a `renderPage()` switch. The transition from any list page to a title's detail view is performed via a shared `onSelectTitle(tconst)` callback prop.

---

## Authentication & UserContext

**`src/UserContext.js`**

Exports two items:

| Export | Type | Purpose |
|--------|------|---------|
| `UserContext` | `React.Context` | Holds the full user object returned by `POST /api/auth/login` |
| `useUser()` | custom hook | Shorthand for `useContext(UserContext)` — used in every protected component |

The logged-in user object shape (from the API):

```json
{ "userId": 1, "username": "alice" }
```

`App.js` wraps the entire authenticated view in `<UserContext.Provider value={currentUser}>`. Components read the user with `const currentUser = useUser()`.

### Authentication flow

1. `App.js` renders `<LoginPage onLogin={setCurrentUser} />` when `currentUser === null`.
2. On a successful login or registration, `LoginPage` calls `onLogin(userData)`, which sets `currentUser` in App state.
3. The "Logout" button calls `handleLogout()`, which resets `currentUser` to `null` and navigates back to the search page.

---

## Navigation & Routing

Navigation is driven by a single `page` state variable in `App.js`:

| `page` value | Component rendered | Entry point |
|---|---|---|
| `"search"` | `<SearchPage>` | Default / home |
| `"detail"` | `<TitleDetail>` | Via `goToDetail(tconst)` |
| `"track"` | `<TrackPage>` | Nav bar |
| `"review"` | `<ReviewPage>` | Nav bar |
| `"trending"` | `<TrendingPage>` | Nav bar |
| `"recommend"` | `<RecommendPage>` | Nav bar |
| `"buddy"` | `<BuddyPage>` | Nav bar |

The `NAV_ITEMS` array in `App.js` drives the rendered navigation buttons and maps each `key` to a `page` value.

**Navigating to a title detail page:**
Any page that displays titles receives an `onSelectTitle` prop. Calling `onSelectTitle(tconst)` sets `selectedTitle` and switches `page` to `"detail"`. `TitleDetail` renders a "← Back to search" button that calls `onBack`, which resets `page` to `"search"`.

---

## Component Reference

### LoginPage

**File:** `src/components/LoginPage.js`  
**Props:** `onLogin(user)` — called with the authenticated user object on success.

Renders a centered card with two tabs: **Sign In** and **Register**.

| Tab | API call | Behaviour on success |
|-----|----------|----------------------|
| Sign In | `POST /api/auth/login` | Calls `onLogin(data)` |
| Register | `POST /api/users` then `POST /api/auth/login` | Auto-logs in and calls `onLogin(data)` |

**State:**

| Variable | Purpose |
|----------|---------|
| `tab` | Active tab: `'login'` or `'register'` |
| `username`, `email`, `password` | Controlled form inputs |
| `error` | Inline error message |
| `loading` | Disables the submit button during requests |

**Demo accounts** (shown on the sign-in tab): `alice`, `bob`, `carol` — password: `password123`.

---

### SearchPage

**File:** `src/components/SearchPage.js`  
**Props:** `onSelectTitle(tconst)`

The primary discovery page. Users can filter by title text, genre, year, and type (movie / TV Series).

**API:** `GET /api/titles/search?q=&genre=&year=&type=`

**State:**

| Variable | Purpose |
|----------|---------|
| `query` | Free-text title search |
| `genre` | Genre filter (e.g. `Drama`) |
| `year` | Release year filter |
| `ttype` | Type filter: `''` / `'movie'` / `'tvSeries'` |
| `results` | Array of title objects, or `null` before first search |
| `loading` | Shows "Searching…" while request is in flight |

Results are displayed in a responsive grid of cards. Each card shows title, type, year, genre badges, and rating. Pressing **Enter** in any input field triggers the search.

---

### TitleDetail

**File:** `src/components/TitleDetail.js`  
**Props:** `tconst` (IMDb title ID), `onBack()`

Full information page for a single title. Fetches title details and reviews in parallel on mount.

**API calls:**

| Call | Purpose |
|------|---------|
| `GET /api/titles/:tconst` | Title metadata, rating, episode list, cast |
| `GET /api/reviews/:tconst` | All reviews for the title |
| `POST /api/progress` | Save / update watch progress |
| `GET /api/progress/:userId/:tconst/predict` | Finish-date prediction (TV series only) |
| `POST /api/reviews` | Submit a new review |

**Sections rendered:**

1. **Header** — title, type, year, genre badges, rating.
2. **Track Your Progress** — status selector, season/episode inputs (TV series only), episodes-per-day for prediction. Saving triggers a finish-date prediction for TV series.
3. **Finish Date Prediction** — shown after saving progress on a TV series; displays total/watched/remaining episodes and an estimated finish date.
4. **Episodes** — table of season and episode numbers (TV series only).
5. **Cast & Crew** — grid of cards with name, category, and character name.
6. **Write a Review** — rating (0–10) and free-text review form.
7. **Reviews** — list of all submitted reviews with username, rating, text, and date.

---

### TrackPage

**File:** `src/components/TrackPage.js`  
**Props:** `onSelectTitle(tconst)`

Displays the current user's full watch-progress list, loaded from the API on mount.

**API calls:**

| Call | Purpose |
|------|---------|
| `GET /api/progress/:userId` | Load all progress records for the user |
| `GET /api/progress/:userId/:tconst/predict` | On-demand finish-date prediction |

Each progress item shows:
- Clickable title (navigates to `TitleDetail`).
- Status badge (color-coded: `watching` = blue, `finished` = green, `plan to watch` = default).
- Current season/episode for TV series.
- Media type badge.
- Last-watched date.
- **Predict Finish** button for in-progress TV series.

---

### ReviewPage

**File:** `src/components/ReviewPage.js`  
**Props:** `onSelectTitle(tconst)` *(declared but not currently used in the rendered output)*

Two-section page:

1. **Write a Review** — select a title from a dropdown, enter a rating (0–10) and review text, then submit.
2. **Browse Reviews** — select a title and load all its reviews.

Both dropdowns are populated by `GET /api/titles/search` (no filters, returns all seeded titles) on mount.

**API calls:**

| Call | Purpose |
|------|---------|
| `GET /api/titles/search` | Populate title dropdowns |
| `POST /api/reviews` | Submit a review |
| `GET /api/reviews/:tconst` | Load reviews for the selected title |

---

### TrendingPage

**File:** `src/components/TrendingPage.js`  
**Props:** `onSelectTitle(tconst)`

Shows the daily top-watched titles ranked by `activityCount`. The date defaults to `2026-03-02` (the seeded activity date) and can be changed via a date picker.

**API:** `GET /api/trending?date=YYYY-MM-DD`

Each trending item shows its rank, title, type, genre badges, rating, and view count. Clicking an item navigates to its detail page.

---

### RecommendPage

**File:** `src/components/RecommendPage.js`  
**Props:** `onSelectTitle(tconst)`

Fetches personalised title recommendations based on a user's watch history and genre preferences. Defaults to the logged-in user but allows switching to any user via a dropdown (useful for demo / admin exploration).

**API calls:**

| Call | Purpose |
|------|---------|
| `GET /api/users` | Populate user selector dropdown |
| `GET /api/recommendations/:userId` | Fetch recommendations |

Results are displayed in the same card grid used by `SearchPage`.

---

### BuddyPage

**File:** `src/components/BuddyPage.js`  
**Props:** `onSelectTitle(tconst)` *(declared but not currently used in the rendered output)*

Three-section page for social watch-buddy features:

1. **Your Buddies** — list of the current user's existing buddies.
2. **Add a Buddy** — dropdown of all other users; submits a buddy relationship.
3. **Compare Progress** — select a buddy and a title to see both users' watch progress side-by-side.

**API calls:**

| Call | Purpose |
|------|---------|
| `GET /api/buddies/:userId` | Load buddy list |
| `GET /api/users` | Populate the "add buddy" dropdown |
| `GET /api/titles/search` | Populate the title dropdown for comparison |
| `POST /api/buddies` | Add a new buddy |
| `GET /api/buddies/compare?userId=&buddyId=&tconst=` | Side-by-side progress comparison |

The comparison panel renders two side-by-side cards showing each user's current season/episode and status for the selected title.

---

## Styling Guide

All styles live in `src/App.css`. The design follows a **dark cinema theme**:

| Token | Value | Used for |
|-------|-------|----------|
| Background (deep) | `#0d0d0d` | Page background |
| Background (elevated) | `#1a1a2e` | Cards, panels, header |
| Border | `#2a2a4a` | Card/panel borders |
| Accent (gold) | `#c9a227` | Brand, active nav, headings, buttons |
| Text (primary) | `#e8e8e8` | Body text |
| Text (muted) | `#aaa` / `#999` | Labels, metadata |
| Success | `#6ecf6e` | Success messages, "finished" status |
| Error | `#ff6b6b` | Error messages |
| Rating | `#f5c518` | Star ratings |

### Reusable CSS classes

| Class | Element | Description |
|-------|---------|-------------|
| `.app-header` | `<header>` | Sticky top nav bar |
| `.app-nav` | `<nav>` | Flex container for nav buttons |
| `.nav-btn` | `<button>` | Nav/action button; `.active` for current page |
| `.app-main` | `<main>` | Centered, max-width content area |
| `.page-title` | `<h1>` | Gold section title |
| `.card` | `<div>` | Hoverable dark card |
| `.card-title` | inner div | Card heading text |
| `.card-meta` | inner div | Card subtitle / metadata |
| `.card-rating` | inner div | Yellow star rating |
| `.grid` | `<div>` | Responsive auto-fill card grid |
| `.search-bar` | `<div>` | Padded flex container for filters |
| `.form-group` | `<div>` | Label + input wrapper |
| `.btn` | `<button>` | Gold primary button |
| `.btn-outline` | modifier | Outlined variant of `.btn` |
| `.btn-sm` | modifier | Smaller padding variant |
| `.badge` | `<span>` | Pill label (genre, type) |
| `.badge-gold` | modifier | Gold-tinted badge |
| `.section` | `<div>` | Content section with top margin |
| `.predict-box` | `<div>` | Finish-date prediction panel |
| `.predict-stat` | `<div>` | Key-value row inside prediction panel |
| `.buddy-compare` | `<div>` | Flex container for comparison cards |
| `.buddy-card` | `<div>` | Individual user card in comparison |
| `.review-item` | `<div>` | Single review block |
| `.progress-item` | `<div>` | Single watch-progress row |
| `.pi-status` | `<span>` | Color-coded status pill (`.watching`, `.finished`) |
| `.trend-item` | `<div>` | Clickable trending row |
| `.trend-rank` | `<div>` | Large gold rank number |
| `.back-btn` | `<button>` | Inline "← Back" link-style button |
| `.loading` | `<p>` | Centered grey loading message |
| `.empty` | `<p>` | Centered grey empty-state message |
| `.error` | `<p>` | Centered red error message |
| `.success` | `<span>` | Inline green success confirmation |

---

## API Communication

All components use the native `fetch` API. A `proxy` entry in `package.json` forwards every `/api/*` request from the React dev server (`localhost:3000`) to the Flask backend (`localhost:5000`), so no absolute URLs or CORS configuration is needed during development.

```json
"proxy": "http://localhost:5000"
```

All `POST` requests send JSON bodies with `Content-Type: application/json`.

---

## Running the Frontend

### Development

```bash
cd frontend
npm install       # first time only
npm start         # starts on http://localhost:3000
```

The backend must also be running on port 5000 (see the root `README.md`).

### Production build

```bash
npm run build
```

Outputs a static bundle to `frontend/build/` that can be served by any static file server or the Flask app.

### Tests

```bash
npm test          # interactive watch mode
```

Tests are co-located in `src/` with a `.test.js` suffix and use React Testing Library.
