import { useEffect, useState } from "react";
import Visualizer3D from "../Visualizer3D";

export default function Visualizer() {
  const keys = ["C", "D", "E", "F", "G", "A", "B"];
  const [activeKey, setActiveKey] = useState(null);

  useEffect(() => {
    const websocket = new WebSocket("ws://172.22.87.7:8765");

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
        setActiveKey(
          event.data.trim().toUpperCase()
        );
      }
    };

    socket.onclose = () => {
      console.log("Visualizer WebSocket disconnected");
    };

    return () => {
      socket.close();
    };
  }, []);

  return (
    <div>
      <h1 className="visualizer-title">
        Visualizer and Note Display
      </h1>

      <p className="visualizer-subtitle">
        Play the instrument and watch the note appear below. Also use the cursor to rotate the instrument in 3D space.
         The instrument will also respond to the notes being played.
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

      {/* 3D Instrument */}
      <Visualizer3D />
    </div>
  );
}