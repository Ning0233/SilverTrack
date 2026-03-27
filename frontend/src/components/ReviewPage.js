import React, { useEffect, useState } from 'react';
import { useUser } from '../UserContext';

const API = '/api';

export default function ReviewPage({ onSelectTitle }) {
  const currentUser = useUser();
  const [tconst,  setTconst]  = useState('');
  const [rating,  setRating]  = useState('');
  const [text,    setText]    = useState('');
  const [message, setMessage] = useState('');

  // Show all reviews for a title the user specifies
  const [searchTconst, setSearchTconst] = useState('');
  const [reviews,      setReviews]      = useState(null);
  const [titles,       setTitles]       = useState([]);

  useEffect(() => {
    fetch(`${API}/titles/search`)
      .then(r => r.json())
      .then(d => setTitles(d));
  }, []);

  const submit = async () => {
    if (!tconst) { setMessage('Please select a title.'); return; }
    await fetch(`${API}/reviews`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        userId:     currentUser.userId,
        tconst,
        rating:     parseFloat(rating) || null,
        reviewText: text,
      }),
    });
    setMessage('Review submitted! ✓');
    setRating('');
    setText('');
  };

  const loadReviews = async () => {
    if (!searchTconst) return;
    const r = await fetch(`${API}/reviews/${searchTconst}`).then(res => res.json());
    setReviews(r);
  };

  return (
    <div>
      <h1 className="page-title">⭐ Write a Review</h1>

      <div className="search-bar" style={{ flexDirection: 'column', gap: '0.75rem' }}>
        <div className="form-group">
          <label>Select Title</label>
          <select value={tconst} onChange={e => setTconst(e.target.value)}>
            <option value="">-- choose a title --</option>
            {titles.map(t => (
              <option key={t.tconst} value={t.tconst}>{t.primaryTitle}</option>
            ))}
          </select>
        </div>
        <div className="form-group">
          <label>Rating (0–10)</label>
          <input type="number" min="0" max="10" step="0.5" placeholder="e.g. 8.5"
            value={rating} onChange={e => setRating(e.target.value)} />
        </div>
        <div className="form-group">
          <label>Your review</label>
          <textarea placeholder="Share your thoughts…" value={text} onChange={e => setText(e.target.value)} />
        </div>
        <div>
          <button className="btn" onClick={submit}>Submit Review</button>
          {message && <span className="success" style={{ marginLeft: '1rem' }}>{message}</span>}
        </div>
      </div>

      {/* Read reviews for any title */}
      <h1 className="page-title" style={{ marginTop: '2rem' }}>💬 Browse Reviews</h1>
      <div className="search-bar">
        <select value={searchTconst} onChange={e => setSearchTconst(e.target.value)}>
          <option value="">-- choose a title --</option>
          {titles.map(t => (
            <option key={t.tconst} value={t.tconst}>{t.primaryTitle}</option>
          ))}
        </select>
        <button className="btn" onClick={loadReviews}>Load Reviews</button>
      </div>

      {reviews !== null && reviews.length === 0 && <p className="empty">No reviews yet for this title.</p>}

      {reviews && reviews.map(r => (
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
  );
}
