import React, { useEffect, useState } from 'react';

const API = '/api';

export default function TrendingPage({ onSelectTitle }) {
  const [trending, setTrending] = useState([]);
  const [loading,  setLoading]  = useState(true);
  const [dateStr,  setDateStr]  = useState('2026-03-02');

  const load = async () => {
    setLoading(true);
    const r = await fetch(`${API}/trending?date=${dateStr}`).then(res => res.json());
    setTrending(r);
    setLoading(false);
  };

  useEffect(() => { load(); }, []); // eslint-disable-line react-hooks/exhaustive-deps

  return (
    <div>
      <h1 className="page-title">🔥 Daily Trending</h1>

      <div className="search-bar" style={{ marginBottom: '1.5rem' }}>
        <input type="date" value={dateStr} onChange={e => setDateStr(e.target.value)} />
        <button className="btn" onClick={load}>Load</button>
      </div>

      {loading && <p className="loading">Loading…</p>}

      {!loading && trending.length === 0 && (
        <p className="empty">No activity recorded for this date.</p>
      )}

      {trending.map((t, idx) => (
        <div key={t.tconst} className="trend-item" onClick={() => onSelectTitle(t.tconst)}>
          <div className="trend-rank">#{idx + 1}</div>
          <div style={{ flex: 1 }}>
            <div style={{ fontWeight: 600 }}>{t.primaryTitle}</div>
            <div style={{ fontSize: '0.8rem', color: '#aaa', marginTop: '0.2rem' }}>
              {t.titleType === 'tvSeries' ? 'TV Series' : 'Movie'} ·&nbsp;
              {t.genres?.split(',').map(g => <span key={g} className="badge">{g}</span>)}
            </div>
          </div>
          {t.averageRating && <div className="card-rating">⭐ {t.averageRating}</div>}
          <div style={{ textAlign: 'right', fontSize: '0.85rem', color: '#c9a227' }}>
            {t.activityCount} <span style={{ color: '#666' }}>views</span>
          </div>
        </div>
      ))}
    </div>
  );
}
