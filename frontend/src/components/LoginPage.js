import React, { useState } from 'react';

const API = '/api';

export default function LoginPage({ onLogin }) {
  const [tab,      setTab]      = useState('login');   // 'login' | 'register'
  const [username, setUsername] = useState('');
  const [email,    setEmail]    = useState('');
  const [password, setPassword] = useState('');
  const [error,    setError]    = useState('');
  const [loading,  setLoading]  = useState(false);

  const reset = () => { setError(''); };

  const handleLogin = async (e) => {
    e.preventDefault();
    if (!username || !password) { setError('Username and password are required.'); return; }
    setLoading(true);
    setError('');
    try {
      const res = await fetch(`${API}/auth/login`, {
        method:  'POST',
        headers: { 'Content-Type': 'application/json' },
        body:    JSON.stringify({ username, password }),
      });
      const data = await res.json();
      if (!res.ok) { setError(data.error || 'Login failed.'); return; }
      onLogin(data);
    } catch {
      setError('Network error. Is the backend running?');
    } finally {
      setLoading(false);
    }
  };

  const handleRegister = async (e) => {
    e.preventDefault();
    if (!username || !email || !password) { setError('All fields are required.'); return; }
    setLoading(true);
    setError('');
    try {
      const res = await fetch(`${API}/users`, {
        method:  'POST',
        headers: { 'Content-Type': 'application/json' },
        body:    JSON.stringify({ username, email, password }),
      });
      const data = await res.json();
      if (!res.ok) { setError(data.error || 'Registration failed.'); return; }
      // Auto-login after registration
      const loginRes = await fetch(`${API}/auth/login`, {
        method:  'POST',
        headers: { 'Content-Type': 'application/json' },
        body:    JSON.stringify({ username, password }),
      });
      const loginData = await loginRes.json();
      if (loginRes.ok) {
        onLogin(loginData);
      } else {
        // Registration succeeded but auto-login failed – direct the user to sign in
        setTab('login');
        setPassword('');
        setEmail('');
        setError('');
      }
    } catch {
      setError('Network error. Is the backend running?');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{
      minHeight: '100vh',
      background: '#0d0d0d',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
    }}>
      <div style={{
        background: '#1a1a2e',
        border: '1px solid #2a2a4a',
        borderRadius: '12px',
        padding: '2.5rem',
        width: '100%',
        maxWidth: '400px',
      }}>
        {/* Brand */}
        <div style={{ textAlign: 'center', marginBottom: '2rem' }}>
          <div style={{ fontSize: '2.5rem' }}>🎬</div>
          <div style={{ fontSize: '1.8rem', fontWeight: 700, color: '#c9a227', marginTop: '0.25rem' }}>
            SilverTrack
          </div>
          <div style={{ color: '#777', fontSize: '0.85rem', marginTop: '0.25rem' }}>
            Your personal movie &amp; TV tracker
          </div>
        </div>

        {/* Tabs */}
        <div style={{ display: 'flex', marginBottom: '1.5rem', borderBottom: '1px solid #2a2a4a' }}>
          {['login', 'register'].map(t => (
            <button
              key={t}
              onClick={() => { setTab(t); reset(); }}
              style={{
                flex: 1,
                background: 'transparent',
                border: 'none',
                borderBottom: tab === t ? '2px solid #c9a227' : '2px solid transparent',
                color: tab === t ? '#c9a227' : '#888',
                padding: '0.6rem',
                cursor: 'pointer',
                fontWeight: tab === t ? 600 : 400,
                fontSize: '0.95rem',
                textTransform: 'capitalize',
                transition: 'color .2s',
              }}
            >
              {t === 'login' ? '🔑 Sign In' : '✨ Register'}
            </button>
          ))}
        </div>

        {/* Form */}
        <form onSubmit={tab === 'login' ? handleLogin : handleRegister}>
          <div className="form-group">
            <label>Username</label>
            <input
              type="text"
              placeholder={tab === 'login' ? 'e.g. alice' : 'Choose a username'}
              value={username}
              onChange={e => setUsername(e.target.value)}
              autoFocus
            />
          </div>

          {tab === 'register' && (
            <div className="form-group">
              <label>Email</label>
              <input
                type="email"
                placeholder="you@example.com"
                value={email}
                onChange={e => setEmail(e.target.value)}
              />
            </div>
          )}

          <div className="form-group">
            <label>Password</label>
            <input
              type="password"
              placeholder={tab === 'login' ? 'Your password' : 'Choose a password'}
              value={password}
              onChange={e => setPassword(e.target.value)}
            />
          </div>

          {error && (
            <p style={{ color: '#ff6b6b', fontSize: '0.85rem', marginBottom: '0.75rem' }}>{error}</p>
          )}

          <button
            type="submit"
            className="btn"
            disabled={loading}
            style={{ width: '100%', marginTop: '0.25rem', opacity: loading ? 0.7 : 1 }}
          >
            {loading ? 'Please wait…' : tab === 'login' ? 'Sign In' : 'Create Account'}
          </button>
        </form>

        {tab === 'login' && (
          <p style={{ color: '#555', fontSize: '0.78rem', marginTop: '1.5rem', textAlign: 'center' }}>
            Demo accounts: <strong style={{ color: '#888' }}>alice</strong>,{' '}
            <strong style={{ color: '#888' }}>bob</strong>,{' '}
            <strong style={{ color: '#888' }}>carol</strong>{' '}
            — password: <strong style={{ color: '#888' }}>password123</strong>
          </p>
        )}
      </div>
    </div>
  );
}
