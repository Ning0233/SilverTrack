import React, { useEffect, useState } from 'react';
import { CURRENT_USER } from '../App';

const API = '/api';

export default function BuddyPage({ onSelectTitle }) {
  const [buddies,   setBuddies]   = useState([]);
  const [users,     setUsers]     = useState([]);
  const [newBuddy,  setNewBuddy]  = useState('');
  const [addMsg,    setAddMsg]    = useState('');

  // comparison state
  const [cmpBuddy,  setCmpBuddy]  = useState('');
  const [cmpTconst, setCmpTconst] = useState('');
  const [titles,    setTitles]    = useState([]);
  const [cmpResult, setCmpResult] = useState(null);

  const loadBuddies = () =>
    fetch(`${API}/buddies/${CURRENT_USER.userId}`)
      .then(r => r.json())
      .then(setBuddies);

  useEffect(() => {
    loadBuddies();
    fetch(`${API}/users`).then(r => r.json()).then(setUsers);
    fetch(`${API}/titles/search`).then(r => r.json()).then(setTitles);
  }, []); // eslint-disable-line react-hooks/exhaustive-deps

  const addBuddy = async () => {
    if (!newBuddy) return;
    const res = await fetch(`${API}/buddies`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ userId: CURRENT_USER.userId, buddyId: parseInt(newBuddy) }),
    });
    if (res.ok) {
      setAddMsg('Buddy added! ✓');
      loadBuddies();
    } else {
      const d = await res.json();
      setAddMsg(d.error || 'Error adding buddy');
    }
  };

  const compare = async () => {
    if (!cmpBuddy || !cmpTconst) return;
    const params = new URLSearchParams({
      userId:  CURRENT_USER.userId,
      buddyId: cmpBuddy,
      tconst:  cmpTconst,
    });
    const r = await fetch(`${API}/buddies/compare?${params}`).then(res => res.json());
    setCmpResult(r);
  };

  const progressLabel = (prog) => {
    if (!prog) return 'No progress recorded';
    if (prog.titleType === 'tvSeries' || prog.currentSeason > 0)
      return `S${prog.currentSeason} E${prog.currentEpisode} · ${prog.status}`;
    return prog.status;
  };

  const nonSelf = users.filter(u => u.userId !== CURRENT_USER.userId);

  return (
    <div>
      <h1 className="page-title">👥 Watch Buddies</h1>

      {/* Current buddies */}
      <div className="section" style={{ marginTop: 0 }}>
        <h2>Your Buddies</h2>
        {buddies.length === 0
          ? <p className="empty" style={{ textAlign: 'left', paddingLeft: 0 }}>No buddies yet.</p>
          : buddies.map(b => (
              <div key={b.userId} style={{
                display: 'flex', alignItems: 'center', gap: '0.75rem',
                padding: '0.6rem 0', borderBottom: '1px solid #2a2a4a',
              }}>
                <span style={{ fontSize: '1.1rem' }}>👤</span>
                <span style={{ fontWeight: 600 }}>{b.username}</span>
              </div>
            ))
        }
      </div>

      {/* Add buddy */}
      <div className="section">
        <h2>Add a Buddy</h2>
        <div className="search-bar">
          <select value={newBuddy} onChange={e => setNewBuddy(e.target.value)}>
            <option value="">-- select user --</option>
            {nonSelf.map(u => <option key={u.userId} value={u.userId}>{u.username}</option>)}
          </select>
          <button className="btn" onClick={addBuddy}>Add Buddy</button>
        </div>
        {addMsg && <p className="success">{addMsg}</p>}
      </div>

      {/* Compare progress */}
      <div className="section">
        <h2>Compare Progress</h2>
        <div className="search-bar" style={{ flexWrap: 'wrap', gap: '0.5rem' }}>
          <select value={cmpBuddy} onChange={e => setCmpBuddy(e.target.value)}>
            <option value="">-- select buddy --</option>
            {buddies.map(b => <option key={b.userId} value={b.userId}>{b.username}</option>)}
          </select>
          <select value={cmpTconst} onChange={e => setCmpTconst(e.target.value)}>
            <option value="">-- select title --</option>
            {titles.map(t => <option key={t.tconst} value={t.tconst}>{t.primaryTitle}</option>)}
          </select>
          <button className="btn" onClick={compare}>Compare</button>
        </div>

        {cmpResult && (
          <div className="buddy-compare">
            <div className="buddy-card">
              <h3>👤 {cmpResult.user.username ?? 'You'}</h3>
              <p style={{ color: '#ccc', fontSize: '0.9rem' }}>
                {progressLabel(cmpResult.user.progress)}
              </p>
            </div>
            <div className="buddy-card">
              <h3>👤 {cmpResult.buddy.username ?? 'Buddy'}</h3>
              <p style={{ color: '#ccc', fontSize: '0.9rem' }}>
                {progressLabel(cmpResult.buddy.progress)}
              </p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
