import JumpCover from "../assets/jump-cover.png";
import performanceVideo from "../assets/performance.mp4";

export default function Songs() {
  return (
    <section className="songs-showcase">

      <h1 className="songs-title">Songs Presenting</h1>

      <p className="songs-subtitle">
        Our featured performance
      </p>

      <div className="song-feature">

        {/* Album cover + song information */}
        <div className="song-top">

          <img
            src={JumpCover}
            alt="Album cover for Jump by Van Halen"
            className="song-cover"
          />

          <div className="song-info">
            <p className="now-playing">NOW PLAYING</p>

            <h2>Jump</h2>

            <p className="song-artist">
              Van Halen
            </p>

            <p className="song-album">
              1984
            </p>
          </div>

        </div>

        {/* Performance video */}
        <video
          controls
          className="performance-video"
        >
          <source src={performanceVideo} type="video/mp4" />
          Your browser does not support the video tag.
        </video>

      </div>

    </section>
  );
}