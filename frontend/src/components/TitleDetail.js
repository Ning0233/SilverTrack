import React, { useEffect, useState } from 'react';
import { useUser } from '../UserContext';

const API = '/api';

export default function TitleDetail({ tconst, onBack }) {
  const currentUser = useUser();
  const [detail,   setDetail]   = useState(null);
  const [loading,  setLoading]  = useState(true);
  const [error,    setError]    = useState(null);
  const [reviews,  setReviews]  = useState([]);
  const [predict,  setPredict]  = useState(null);

  // track form
  const [trackStatus,  setTrackStatus]  = useState('watching');
  const [trackSeason,  setTrackSeason]  = useState(1);
  const [trackEpisode, setTrackEpisode] = useState(1);
  const [epPerDay,     setEpPerDay]     = useState(2);
  const [trackMsg,     setTrackMsg]     = useState('');

  // review form
  const [revRating, setRevRating] = useState('');
  const [revText,   setRevText]   = useState('');
  const [revMsg,    setRevMsg]    = useState('');

  useEffect(() => {
    if (!tconst) return;
    setLoading(true);
    Promise.all([
      fetch(`${API}/titles/${tconst}`).then(r => r.json()),
      fetch(`${API}/reviews/${tconst}`).then(r => r.json()),
    ]).then(([d, r]) => {
      setDetail(d);
      setReviews(r);
      setLoading(false);
    }).catch(() => { setError('Failed to load title.'); setLoading(false); });
  }, [tconst]);

  const saveProgress = async () => {
    await fetch(`${API}/progress`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        userId: currentUser.userId,
        tconst,
        status: trackStatus,
        currentSeason:  parseInt(trackSeason),
        currentEpisode: parseInt(trackEpisode),
        episodesPerDay: parseFloat(epPerDay),
      }),
    });
    setTrackMsg('Progress saved! ✓');
    // fetch prediction for TV series
    if (detail?.title?.titleType === 'tvSeries') {
      const p = await fetch(`${API}/progress/${currentUser.userId}/${tconst}/predict`).then(r => r.json());
      setPredict(p);
    }
  };

  const submitReview = async () => {
    await fetch(`${API}/reviews`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        userId: currentUser.userId,
        tconst,
        rating:     parseFloat(revRating) || null,
        reviewText: revText,
      }),
    });
    setRevMsg('Review submitted! ✓');
    const r = await fetch(`${API}/reviews/${tconst}`).then(r2 => r2.json());
    setReviews(r);
    setRevRating('');
    setRevText('');
  };

  if (loading) return <p className="loading">Loading…</p>;
  if (error)   return <p className="error">{error}</p>;
  if (!detail) return null;

  const { title, rating, episodes, cast } = detail;
  const isSeries = title?.titleType === 'tvSeries';

  return (
    <div>
      <button className="back-btn" onClick={onBack}>← Back to search</button>

      <div className="detail-header">
        <h1>{title?.primaryTitle}</h1>
        <p className="detail-meta">
          {isSeries ? 'TV Series' : 'Movie'} · {title?.startYear} ·&nbsp;
          {title?.genres?.split(',').map(g => <span key={g} className="badge">{g}</span>)}
        </p>
        {rating && (
          <p className="detail-meta card-rating">
            ⭐ {rating.averageRating} &nbsp;
            <span style={{ color: '#aaa', fontWeight: 400 }}>({(rating.numVotes / 1000).toFixed(0)}K votes)</span>
          </p>
        )}
      </div>

      {/* Track section */}
      <div className="section">
        <h2>📺 Track Your Progress</h2>
        <div className="search-bar" style={{ flexDirection: 'column', gap: '0.75rem' }}>
          <div style={{ display: 'flex', gap: '0.5rem', flexWrap: 'wrap' }}>
            <div className="form-group" style={{ flex: 1 }}>
              <label>Status</label>
              <select value={trackStatus} onChange={e => setTrackStatus(e.target.value)}>
                <option value="watching">Watching</option>
                <option value="finished">Finished</option>
                <option value="plan_to_watch">Plan to Watch</option>
              </select>
            </div>
            {isSeries && (
              <>
                <div className="form-group" style={{ flex: 1 }}>
                  <label>Season</label>
                  <input type="number" min="1" value={trackSeason} onChange={e => setTrackSeason(e.target.value)} />
                </div>
                <div className="form-group" style={{ flex: 1 }}>
                  <label>Episode</label>
                  <input type="number" min="1" value={trackEpisode} onChange={e => setTrackEpisode(e.target.value)} />
                </div>
                <div className="form-group" style={{ flex: 1 }}>
                  <label>Episodes/day</label>
                  <input type="number" min="0.1" step="0.5" value={epPerDay} onChange={e => setEpPerDay(e.target.value)} />
                </div>
              </>
            )}
          </div>
          <div>
            <button className="btn" onClick={saveProgress}>Save Progress</button>
            {trackMsg && <span className="success" style={{ marginLeft: '1rem' }}>{trackMsg}</span>}
          </div>
        </div>

        {predict && (
          <div className="predict-box">
            <h3>📅 Finish Date Prediction</h3>
            <div className="predict-stat"><span>Total episodes</span><span className="predict-val">{predict.totalEpisodes}</span></div>
            <div className="predict-stat"><span>Watched</span><span className="predict-val">{predict.watchedEpisodes}</span></div>
            <div className="predict-stat"><span>Remaining</span><span className="predict-val">{predict.remainingEpisodes}</span></div>
            <div className="predict-stat"><span>Episodes/day</span><span className="predict-val">{predict.episodesPerDay}</span></div>
            <div className="predict-stat">
              <span>Estimated finish</span>
              <span className="predict-val" style={{ color: '#c9a227' }}>{predict.predictedFinishDate ?? 'N/A'}</span>
            </div>
          </div>
        )}
      </div>

      {/* Episodes */}
      {isSeries && episodes.length > 0 && (
        <div className="section">
          <h2>🎞 Episodes ({episodes.length})</h2>
          <table className="episode-table">
            <thead>
              <tr><th>Season</th><th>Episode</th></tr>
            </thead>
            <tbody>
              {episodes.map(ep => (
                <tr key={ep.tconst}>
                  <td>S{ep.seasonNumber}</td>
                  <td>E{ep.episodeNumber}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {/* Cast */}
      {cast.length > 0 && (
        <div className="section">
          <h2>🎭 Cast &amp; Crew</h2>
          <div className="grid">
            {cast.map(c => (
              <div key={c.nconst} className="card" style={{ cursor: 'default' }}>
                <div className="card-title">{c.primaryName}</div>
                <div className="card-meta"><span className="badge">{c.category}</span></div>
                {c.characters && (
                  <div className="card-meta" style={{ marginTop: '0.3rem', color: '#ccc', fontSize: '0.8rem' }}>
                    as {c.characters.replace(/["[\]]/g, '')}
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Write review */}
      <div className="section">
        <h2>✍️ Write a Review</h2>
        <div className="search-bar" style={{ flexDirection: 'column', gap: '0.75rem' }}>
          <div className="form-group">
            <label>Rating (0–10)</label>
            <input type="number" min="0" max="10" step="0.5" placeholder="e.g. 8.5"
              value={revRating} onChange={e => setRevRating(e.target.value)} />
          </div>
          <div className="form-group">
            <label>Your review</label>
            <textarea placeholder="Share your thoughts…" value={revText} onChange={e => setRevText(e.target.value)} />
          </div>
          <div>
            <button className="btn" onClick={submitReview}>Submit Review</button>
            {revMsg && <span className="success" style={{ marginLeft: '1rem' }}>{revMsg}</span>}
          </div>
        </div>
      </div>

      {/* Reviews list */}
      {reviews.length > 0 && (
        <div className="section">
          <h2>💬 Reviews ({reviews.length})</h2>
          {reviews.map(r => (
            <div key={r.reviewId} className="review-item">
              <div className="review-header">
                <span className="review-user">@{r.username}</span>
                {r.rating && <span className="review-rating">⭐ {r.rating}</span>}
              </div>
              <div className="review-text">{r.reviewText}</div>
              <div className="review-date">{r.createdAt}</div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
