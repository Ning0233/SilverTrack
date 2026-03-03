import React, { useState } from 'react';

const API = '/api';

export default function SearchPage({ onSelectTitle }) {
  const [query,   setQuery]   = useState('');
  const [genre,   setGenre]   = useState('');
  const [year,    setYear]    = useState('');
  const [ttype,   setTtype]   = useState('');
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);

  const search = async () => {
    setLoading(true);
    const params = new URLSearchParams();
    if (query) params.set('q',     query);
    if (genre) params.set('genre', genre);
    if (year)  params.set('year',  year);
    if (ttype) params.set('type',  ttype);
    const res  = await fetch(`${API}/titles/search?${params}`);
    const data = await res.json();
    setResults(data);
    setLoading(false);
  };

  const handleKey = (e) => { if (e.key === 'Enter') search(); };

  return (
    <div>
      <h1 className="page-title">🔍 Find Movies &amp; Shows</h1>

      <div className="search-bar">
        <input
          placeholder="Search by title…"
          value={query}
          onChange={e => setQuery(e.target.value)}
          onKeyDown={handleKey}
        />
        <input
          placeholder="Genre (e.g. Drama)"
          value={genre}
          onChange={e => setGenre(e.target.value)}
          onKeyDown={handleKey}
        />
        <input
          placeholder="Year"
          type="number"
          value={year}
          onChange={e => setYear(e.target.value)}
          onKeyDown={handleKey}
        />
        <select value={ttype} onChange={e => setTtype(e.target.value)}>
          <option value="">All types</option>
          <option value="movie">Movie</option>
          <option value="tvSeries">TV Series</option>
        </select>
        <button className="btn" onClick={search}>Search</button>
      </div>

      {loading && <p className="loading">Searching…</p>}

      {results !== null && results.length === 0 && (
        <p className="empty">No results found. Try different filters.</p>
      )}

      {results && results.length > 0 && (
        <div className="grid">
          {results.map(t => (
            <div key={t.tconst} className="card" onClick={() => onSelectTitle(t.tconst)}>
              <div className="card-title">{t.primaryTitle}</div>
              <div className="card-meta">
                {t.titleType === 'tvSeries' ? 'TV Series' : 'Movie'} · {t.startYear}
              </div>
              <div className="card-meta" style={{ marginTop: '0.3rem' }}>
                {t.genres && t.genres.split(',').map(g => (
                  <span key={g} className="badge">{g}</span>
                ))}
              </div>
              {t.averageRating && (
                <div className="card-rating" style={{ marginTop: '0.5rem' }}>
                  ⭐ {t.averageRating} <span style={{ color: '#666', fontWeight: 400 }}>({(t.numVotes / 1000).toFixed(0)}K)</span>
                </div>
              )}
            </div>
          ))}
        </div>
      )}

      {results === null && (
        <p className="empty">Enter a search term above to find movies and shows.</p>
      )}
    </div>
  );
}
