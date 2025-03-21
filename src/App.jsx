import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { useState } from 'react';
import { FaPlay, FaPause, FaRandom, FaShare, FaInfoCircle, FaTimes } from 'react-icons/fa';
import AdminPage from './pages/AdminPage';
import ForgotPasswordPage from './pages/ForgotPasswordPage';
import ResetPasswordPage from './pages/ResetPasswordPage';
import Footer from './components/Footer';
import './App.css';

function App() {
  const [isPlaying, setIsPlaying] = useState(false);
  const [showInfo, setShowInfo] = useState(false);
  const [currentSong, setCurrentSong] = useState({
    artist: "Nome do Artista",
    title: "Nome da Música"
  });

  const togglePlay = () => {
    setIsPlaying(!isPlaying);
  };

  const toggleInfo = () => {
    setShowInfo(!showInfo);
  };

  const handleShare = () => {
    console.log("Compartilhar");
  };

  return (
    <>
      <div className="app">
        <h1>🎵 RADIO IMPORTANTE</h1>
        <div className="controls">
          <button className="control-btn" onClick={togglePlay}>
            <span className="icon-wrapper">
              {isPlaying ? <FaPause /> : <FaPlay />}
            </span>
          </button>
          <button className="control-btn">
            <span className="icon-wrapper">
              <FaRandom />
            </span>
          </button>
          <button className="control-btn" onClick={toggleInfo}>
            <span className="icon-wrapper">
              <FaInfoCircle />
            </span>
          </button>
        </div>
        {showInfo && (
          <div className="info-card">
            <div className="card-content">
              <button className="close-btn" onClick={toggleInfo}>
                <span className="icon-wrapper">
                  <FaTimes />
                </span>
              </button>
              <div className="song-info">
                <p className="artist">{currentSong.artist}</p>
                <h2 className="title">{currentSong.title}</h2>
              </div>
              <button className="share-btn" onClick={handleShare}>
                <span className="icon-wrapper">
                  <FaShare />
                </span>
              </button>
            </div>
          </div>
        )}
      </div>
      <Footer />
    </>
  );
}

export default App;
