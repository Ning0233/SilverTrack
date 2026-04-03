import React, { useState } from 'react';
import './App.css';
import { UserContext } from './UserContext';
import LoginPage from './components/LoginPage';
import SearchPage from './components/SearchPage';
import TitleDetail from './components/TitleDetail';
import TrackPage from './components/TrackPage';
import ReviewPage from './components/ReviewPage';
import TrendingPage from './components/TrendingPage';
import BuddyPage from './components/BuddyPage';
import RecommendPage from './components/RecommendPage';

const NAV_ITEMS = [
  { key: 'search',    label: '🔍 Find'        },
  { key: 'track',     label: '📺 Track'        },
  { key: 'review',    label: '⭐ Review'       },
  { key: 'trending',  label: '🔥 Trending'     },
  { key: 'recommend', label: '🎯 For You'      },
  { key: 'buddy',     label: '👥 Watch Buddy'  },
];

function App() {
  const [currentUser, setCurrentUser] = useState(null);
  const [page, setPage]               = useState('search');
  const [selectedTitle, setSelectedTitle] = useState(null);

  const goToDetail = (tconst) => {
    setSelectedTitle(tconst);
    setPage('detail');
  };

  const handleLogout = () => {
    setCurrentUser(null);
    setPage('search');
    setSelectedTitle(null);
  };

  if (!currentUser) {
    return <LoginPage onLogin={setCurrentUser} />;
  }

  const renderPage = () => {
    switch (page) {
      case 'search':    return <SearchPage onSelectTitle={goToDetail} />;
      case 'detail':    return <TitleDetail tconst={selectedTitle} onBack={() => setPage('search')} />;
      case 'track':     return <TrackPage onSelectTitle={goToDetail} />;
      case 'review':    return <ReviewPage onSelectTitle={goToDetail} />;
      case 'trending':  return <TrendingPage onSelectTitle={goToDetail} />;
      case 'recommend': return <RecommendPage onSelectTitle={goToDetail} />;
      case 'buddy':     return <BuddyPage onSelectTitle={goToDetail} />;
      default:          return <SearchPage onSelectTitle={goToDetail} />;
    }
  };

  return (
    <UserContext.Provider value={currentUser}>
      <div className="app">
        <header className="app-header">
          <div className="brand" onClick={() => setPage('search')}>🎬 SilverTrack</div>
          <nav className="app-nav">
            {NAV_ITEMS.map(item => (
              <button
                key={item.key}
                className={`nav-btn${page === item.key ? ' active' : ''}`}
                onClick={() => setPage(item.key)}
              >
                {item.label}
              </button>
            ))}
          </nav>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
            <div className="user-badge">👤 {currentUser.username}</div>
            <button className="nav-btn" onClick={handleLogout} title="Sign out">
              ↩ Logout
            </button>
          </div>
        </header>
        <main className="app-main">{renderPage()}</main>
      </div>
    </UserContext.Provider>
  );
}

export default App;
