import Visualizer3D from "../Visualizer3D";

export default function Visualizer() {
  return (
    <div>
      <h1 className="visualizer-title">Visualizer</h1>
      <p className="visualizer-subtitle">Our 3D music visualizer, use your cursor to interact with the visualization.</p>

      <Visualizer3D />
    </div>
  );
}