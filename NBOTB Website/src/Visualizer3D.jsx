import { Canvas, useFrame } from "@react-three/fiber";
import { useGLTF, OrbitControls } from "@react-three/drei";
import { useEffect, useRef } from "react";
import * as THREE from "three";

function InstrumentModel({ activeKey }) {
  const { scene } = useGLTF("/models/keytar.glb");
  const groupRef = useRef();
  const glowStrength = useRef(0);

  // Trigger a strong glow pulse whenever the note changes
  useEffect(() => {
    if (activeKey) {
      glowStrength.current = 1;
    }
  }, [activeKey]);

  scene.traverse((child) => {
    if (child.isMesh) {
      child.castShadow = true;
      child.receiveShadow = true;

      if (child.material) {
        child.material = child.material.clone();

        child.material.emissive = new THREE.Color("#6ffcff");
        child.material.emissiveIntensity = 0;
      }
    }
  });

  useFrame(() => {
    if (!groupRef.current) return;

    const reactions = {
      C: { x: -0.14, y: 0.16, z: -0.20 },
      D: { x: -0.10, y: 0.20, z: -0.14 },
      E: { x: -0.06, y: 0.25, z: -0.08 },
      F: { x: 0.00, y: 0.30, z: 0.00 },
      G: { x: 0.06, y: 0.25, z: 0.08 },
      A: { x: 0.10, y: 0.20, z: 0.14 },
      B: { x: 0.14, y: 0.16, z: 0.20 },
    };

    const reaction = reactions[activeKey];

    const targetX = reaction ? reaction.x : 0;
    const targetY = reaction ? reaction.y : 0;
    const targetZ = reaction ? reaction.z : 0;

    // Original movement, but stronger
    groupRef.current.rotation.x +=
      (targetX - groupRef.current.rotation.x) * 0.45;

    groupRef.current.position.y +=
      (targetY - groupRef.current.position.y) * 0.45;

    groupRef.current.rotation.z +=
      (targetZ - groupRef.current.rotation.z) * 0.45;

    // Fade glow
    glowStrength.current *= 0.90;

    const glow = glowStrength.current;

    // Neon emissive glow
    scene.traverse((child) => {
      if (child.isMesh && child.material) {
        child.material.emissiveIntensity = glow * 5;
      }
    });

    // Scale punch
    const pulseScale = 1 + glow * 0.08;

    groupRef.current.scale.set(
      pulseScale,
      pulseScale,
      pulseScale
    );

    // Extra shake
    if (glow > 0.05) {
      groupRef.current.rotation.y =
        Math.sin(Date.now() * 0.03) * glow * 0.08;
    } else {
      groupRef.current.rotation.y *= 0.9;
    }
  });

  return (
    <group ref={groupRef}>
      <primitive object={scene} scale={7} />
    </group>
  );
}

useGLTF.preload("/models/keytar.glb");

export default function Visualizer3D({ activeKey }) {
  return (
    <div style={{ width: "100%", height: "500px" }}>
      <Canvas
        shadows
        camera={{ position: [5, 5, 2.5], fov: 40 }}
      >
        <ambientLight
          intensity={activeKey ? 1.3 : 0.35}
        />

        <directionalLight
          position={[8, 3, 5]}
          intensity={activeKey ? 2.5 : 1.2}
          castShadow
          shadow-mapSize-width={2048}
          shadow-mapSize-height={2048}
        />

        <directionalLight
          position={[-4, 2, -3]}
          intensity={activeKey ? 1.3 : 0.5}
        />

        {/* Cyan flash */}
        <pointLight
          position={[2, 2, 3]}
          intensity={activeKey ? 12 : 0}
          distance={12}
          decay={2}
          color="#6ffcff"
        />

        {/* Pink flash */}
        <pointLight
          position={[-3, 1, -2]}
          intensity={activeKey ? 10 : 0}
          distance={10}
          decay={2}
          color="#ff4fd8"
        />

        {/* Purple flash */}
        <pointLight
          position={[0, 4, -1]}
          intensity={activeKey ? 8 : 0}
          distance={10}
          decay={2}
          color="#a86cff"
        />

        <InstrumentModel activeKey={activeKey} />

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