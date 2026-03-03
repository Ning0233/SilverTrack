import React, { useEffect, useState } from 'react';
import { CURRENT_USER } from '../App';

const API = '/api';

export default function TrackPage({ onSelectTitle }) {
  const [progress, setProgress] = useState([]);
  const [loading,  setLoading]  = useState(true);
  const [predict,  setPredict]  = useState({});

  useEffect(() => {
    fetch(`${API}/progress/${CURRENT_USER.userId}`)
      .then(r => r.json())
      .then(data => { setProgress(data); setLoading(false); })
      .catch(() => setLoading(false));
  }, []);

  const fetchPrediction = async (tconst) => {
    const res = await fetch(`${API}/progress/${CURRENT_USER.userId}/${tconst}/predict`);
    const data = await res.json();
    setPredict(prev => ({ ...prev, [tconst]: data }));
  };

  if (loading) return <p className="loading">Loading…</p>;

  return (
    <div>
      <h1 className="page-title">📺 My Watch Progress</h1>

      {progress.length === 0 && (
        <p className="empty">No tracking records yet. Find a title and save your progress!</p>
      )}

      {progress.map(p => (
        <div key={p.tconst}>
          <div className="progress-item">
            <div className="pi-title" onClick={() => onSelectTitle(p.tconst)}>
              {p.primaryTitle}
            </div>
            <span className={`pi-status ${p.status}`}>{p.status.replace('_', ' ')}</span>
            {p.titleType === 'tvSeries' && (
              <span className="badge badge-gold">S{p.currentSeason} E{p.currentEpisode}</span>
            )}
            <span className="badge">{p.titleType === 'tvSeries' ? 'TV' : 'Movie'}</span>
            {p.lastWatchedDate && (
              <span style={{ fontSize: '0.78rem', color: '#666' }}>Last: {p.lastWatchedDate}</span>
            )}
            {p.titleType === 'tvSeries' && p.status !== 'finished' && (
              <button
                className="btn btn-outline btn-sm"
                onClick={() => fetchPrediction(p.tconst)}
              >
                Predict Finish
              </button>
            )}
          </div>

          {predict[p.tconst] && !predict[p.tconst].error && (
            <div className="predict-box" style={{ marginBottom: '1rem' }}>
              <h3>📅 Finish Date Prediction – {p.primaryTitle}</h3>
              <div className="predict-stat">
                <span>Remaining episodes</span>
                <span className="predict-val">{predict[p.tconst].remainingEpisodes}</span>
              </div>
              <div className="predict-stat">
                <span>Episodes / day</span>
                <span className="predict-val">{predict[p.tconst].episodesPerDay}</span>
              </div>
              <div className="predict-stat">
                <span>Estimated finish</span>
                <span className="predict-val" style={{ color: '#c9a227' }}>
                  {predict[p.tconst].predictedFinishDate ?? 'N/A'}
                </span>
              </div>
            </div>
          )}
        </div>
      ))}
    </div>
  );
}
