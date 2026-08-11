import { useEffect, useState, useRef } from "react";
import Visualizer3D from "../Visualizer3D";

export default function Visualizer() {
  const keys = ["C", "D", "E", "F", "G", "A", "B"];
  const [activeKey, setActiveKey] = useState(null);
  const [notePulse, setNotePulse] = useState(false);

  const audioRef = useRef(null);
  const [musicVolume, setMusicVolume] = useState(0.25);

  // Control background music volume
  useEffect(() => {
    if (audioRef.current) {
      audioRef.current.volume = musicVolume;
    }
  }, [musicVolume]);

  // Connect to WebSocket
  useEffect(() => {
    const socket = new WebSocket(
      `ws://${window.location.hostname}:8765`
    );

    socket.onopen = () => {
      console.log("Visualizer connected to WebSocket");
    };

    socket.onmessage = (event) => {
      console.log("Received:", event.data);

      try {
        const data = JSON.parse(event.data);

        if (data.original_message) {
          setActiveKey(
            data.original_message.trim().toUpperCase()
          );
        }
      } catch {
        setActiveKey(event.data.trim().toUpperCase());
      }
    };

    socket.onclose = () => {
      console.log("Visualizer WebSocket disconnected");
    };

    return () => {
      socket.close();
    };
  }, []);

  // Glow / flash whenever a note is received
  useEffect(() => {
    if (!activeKey) return;

    setNotePulse(true);

    const timer = setTimeout(() => {
      setNotePulse(false);
    }, 180);

    return () => clearTimeout(timer);
  }, [activeKey]);




// TEMPORARY TESTING WITH COMPUTER KEYBOARD
useEffect(() => {
  const handleKeyDown = (event) => {
    const note = event.key.toUpperCase();

    if (keys.includes(note)) {
      setActiveKey(note);
    }
  };

  const handleKeyUp = (event) => {
    const note = event.key.toUpperCase();

    if (keys.includes(note)) {
      setActiveKey(null);
    }
  };

  window.addEventListener("keydown", handleKeyDown);
  window.addEventListener("keyup", handleKeyUp);

  return () => {
    window.removeEventListener("keydown", handleKeyDown);
    window.removeEventListener("keyup", handleKeyUp);
  };
}, []);
















  return (
  <div
    className={`visualizer-page ${
      notePulse ? "visualizer-pulse" : ""
    } ${activeKey ? `note-${activeKey.toLowerCase()}` : ""}`}
  >
    <h1>Visualizer and Note Display</h1>
      <p className="visualizer-subtitle">
        Play the instrument and watch the note appear below. Also use the
        cursor to rotate the instrument in 3D space. The instrument will
        also respond to the notes being played.
      </p>

      {/* Instrument note display */}
      <div className="note-container">
        {keys.map((note) => (
          <div
            key={note}
            className={`note-key ${
              activeKey === note ? "note-active" : ""
            }`}
          >
            {note}
          </div>
        ))}
      </div>

      {/* Background Music */}
      <div className="backing-track">
        <h3>Background Music</h3>

        <audio
          ref={audioRef}
          src="/music/background.mov"
          controls
          loop
        />

        <div className="music-volume">
          <label htmlFor="musicVolume">
            Background Music Volume: {Math.round(musicVolume * 100)}%
          </label>

          

          <input
            id="musicVolume"
            type="range"
            min="0"
            max="1"
            step="0.05"
            value={musicVolume}
            onChange={(e) =>
              setMusicVolume(Number(e.target.value))
            }
          />
        </div>
      </div>

      {/* 3D Instrument */}
      <div
        className={`visualizer-stage ${
          notePulse ? "stage-pulse" : ""
        }`}
      >
        <Visualizer3D activeKey={activeKey} />
      </div>
    </div>
  );
}