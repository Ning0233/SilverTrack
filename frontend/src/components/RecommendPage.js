import React, { useEffect, useState } from 'react';

const API = '/api';

export default function RecommendPage({ onSelectTitle }) {
  const [recs,    setRecs]    = useState([]);
  const [loading, setLoading] = useState(true);
  const [userId,  setUserId]  = useState(1);
  const [users,   setUsers]   = useState([]);

  useEffect(() => {
    fetch(`${API}/users`).then(r => r.json()).then(setUsers);
  }, []);

  useEffect(() => {
    setLoading(true);
    fetch(`${API}/recommendations/${userId}`)
      .then(r => r.json())
      .then(d => { setRecs(d); setLoading(false); });
  }, [userId]);

  return (
    <div>
      <h1 className="page-title">🎯 Personalized Recommendations</h1>

      <div className="search-bar" style={{ marginBottom: '1.5rem' }}>
        <select value={userId} onChange={e => setUserId(Number(e.target.value))}>
          {users.map(u => <option key={u.userId} value={u.userId}>👤 {u.username}</option>)}
        </select>
      </div>

      {loading && <p className="loading">Loading recommendations…</p>}

      {!loading && recs.length === 0 && (
        <p className="empty">No recommendations yet. Start tracking titles to get personalized suggestions!</p>
      )}

      {!loading && recs.length > 0 && (
        <>
          <p style={{ color: '#aaa', marginBottom: '1rem', fontSize: '0.9rem' }}>
            Based on your watch history, you might enjoy:
          </p>
          <div className="grid">
            {recs.map(t => (
              <div key={t.tconst} className="card" onClick={() => onSelectTitle(t.tconst)}>
                <div className="card-title">{t.primaryTitle}</div>
                <div className="card-meta">
                  {t.titleType === 'tvSeries' ? 'TV Series' : 'Movie'} · {t.startYear}
                </div>
                <div className="card-meta" style={{ marginTop: '0.3rem' }}>
                  {t.genres?.split(',').map(g => <span key={g} className="badge">{g}</span>)}
                </div>
                {t.averageRating && (
                  <div className="card-rating" style={{ marginTop: '0.5rem' }}>
                    ⭐ {t.averageRating}
                  </div>
                )}
              </div>
            ))}
          </div>
        </>
      )}
    </div>
  );
}
