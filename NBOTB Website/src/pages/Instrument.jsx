import { useState, useRef } from "react";
import shell from "../assets/cad-shell.png";

export default function Instrument() {
  const [showInfo, setShowInfo] = useState(false);
  const infoRef = useRef(null);

  return (
    <section className="instrument">

      <h1 className="instrument-title">
        Instrument
      </h1>

      <p className="instrument-description">
        The shell was designed look 80s theme and to house all the technological components on the
        inside and the keyboard on the outside. Click on the CAD image for more
        info!
      </p>

      <button
        className="image-button"
        onClick={() => {
          const opening = !showInfo;
          setShowInfo(opening);

          if (opening) {
            setTimeout(() => {
              infoRef.current?.scrollIntoView({
                behavior: "smooth",
                block: "center",
              });
            }, 10);
          }
        }}
      >
        <img
          src={shell}
          alt="CAD Shell"
          className="instrument-image"
        />
      </button>

      {showInfo && (
        <div ref={infoRef} className="info-card">
          <h2>CAD Shell Design</h2>

          <p>
            This CAD shell was modeled in SolidWorks and serves as the enclosure
            for our instrument.
          </p>

          <ul>
            <li>Designed specifically for the Raspberry Pi Pico 2</li>
            <li>This keytar is inspired by 80s theme especially with the retro aesthetic and the lavendar coloring given to the keytar.</li>
            <li>Specific compartments to fit the keyboard</li>
            <li>Mounting points for electronics</li>
            <li>Designed on the CAD software SolidWorks</li>
          </ul>
        </div>
      )}

    </section>
  );
}