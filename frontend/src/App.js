import React, { useState } from 'react';
import './App.css';
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

// Global "current user" for demo purposes (user 1 = alice)
export const CURRENT_USER = { userId: 1, username: 'alice' };

function App() {
  const [page, setPage]           = useState('search');
  const [selectedTitle, setSelectedTitle] = useState(null);

  const goToDetail = (tconst) => {
    setSelectedTitle(tconst);
    setPage('detail');
  };

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
        <div className="user-badge">👤 {CURRENT_USER.username}</div>
      </header>
      <main className="app-main">{renderPage()}</main>
    </div>
  );
}

export default App;
