import "./App.css";
import { BrowserRouter, Routes, Route, Link } from "react-router-dom";

import Home from "./pages/Home";
import Instrument from "./pages/Instrument";
import About from "./pages/About";
import Songs from "./pages/Songs";
import Visualizer from "./pages/Visualizer";

function App() {
  return (
    <BrowserRouter>
      <div>
        <nav className="navbar">
          <h2 className="logo">New Bruins On The 
            Block</h2>

          <ul>
            <li>
              <Link to="/">Home</Link>
            </li>

            <li>
              <Link to="/instrument">Instrument</Link>
            </li>

            <li>
              <Link to="/about">About the Creators</Link>
            </li>

            <li>
              <Link to="/songs">Songs Presenting</Link>
            </li>

            <li>
              <Link to="/visualizer">Visualizer</Link>
            </li>
          </ul>
        </nav>

        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/instrument" element={<Instrument />} />
          <Route path="/about" element={<About />} />
          <Route path="/songs" element={<Songs />} />
          <Route path="/visualizer" element={<Visualizer />} />
        </Routes>
      </div>
    </BrowserRouter>
  );
}

export default App;