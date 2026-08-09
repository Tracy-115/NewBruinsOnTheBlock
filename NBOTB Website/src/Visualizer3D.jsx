import { Canvas } from "@react-three/fiber";
import { useGLTF, OrbitControls, ContactShadows } from "@react-three/drei";

function InstrumentModel() {
  const { scene } = useGLTF("/models/keytar.glb");

  scene.traverse((child) => {
    if (child.isMesh) {
      child.castShadow = true;
      child.receiveShadow = true;
    }
  });

  return <primitive object={scene} scale={5} />;
}

useGLTF.preload("/models/keytar.glb");

export default function Visualizer3D() {
  return (
    <div style={{ width: "100%", height: "600px" }}>
      <Canvas
            shadows
            camera={{ position: [3, 2, 2.5], fov: 40 }}
            >
        <ambientLight intensity={0.35} />

            <directionalLight
            position={[5, 8, 5]}
            intensity={1.2}
            castShadow
            shadow-mapSize-width={2048}
            shadow-mapSize-height={2048}
            />

            <directionalLight
            position={[-4, 2, -3]}
            intensity={0.25}
            />
        <InstrumentModel />

        <OrbitControls
            enablePan={true}
            enableZoom={true}
            enableRotate={true}
            target={[0, 0, 0]}
            minDistance={0.5}
            maxDistance={10}
        />
      </Canvas>
    </div>
  );
}