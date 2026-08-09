import { Link } from "react-router-dom";
import bear from "../assets/botb-bear.png";

export default function Home() {
  return (
    <section className="hero home-page">

      <img
        src={bear}
        alt="BOTB Bear"
        className="hero-image"
      />

      <h1 className="home-title">New Bruins On The Block</h1>

      <p className="home-subtitle">
        The most perfect synthesizer custom built with a Raspberry Pi Pico 2,
        React, and modern electronics.
      </p>

      <Link to="/instrument" className="hero-button">
        Explore Our Instrument
      </Link>

    </section>
  );
}