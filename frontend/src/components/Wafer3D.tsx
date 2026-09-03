import { useRef } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { OrbitControls, Float, Stars, Sparkles } from '@react-three/drei';
import * as THREE from 'three';

interface WaferProps {
  riskLevel: 'IDLE' | 'SCANNING' | 'LOW' | 'MEDIUM' | 'HIGH';
}

function SemiconductorWafer({ riskLevel }: WaferProps) {
  const meshRef = useRef<THREE.Mesh>(null);

  // Determine colors based on risk level
  const baseColor = riskLevel === 'LOW' ? '#00ff88' 
                  : riskLevel === 'MEDIUM' ? '#ffb700' 
                  : riskLevel === 'HIGH' ? '#ff003c' 
                  : riskLevel === 'SCANNING' ? '#00f0ff' 
                  : '#445566';
                  
  const emissiveIntensity = riskLevel === 'IDLE' ? 0.2 : (riskLevel === 'SCANNING' ? 1.5 : 0.8);
  const rotationSpeed = riskLevel === 'SCANNING' ? 0.05 : 0.005;

  useFrame(() => {
    if (meshRef.current) {
      meshRef.current.rotation.y += rotationSpeed;
    }
  });

  return (
    <Float speed={2} rotationIntensity={0.5} floatIntensity={1}>
      {/* The Silicon Wafer (Cylinder) */}
      <mesh ref={meshRef} rotation={[Math.PI / 4, 0, 0]}>
        <cylinderGeometry args={[2.5, 2.5, 0.1, 64]} />
        <meshPhysicalMaterial 
          color={baseColor}
          metalness={0.9}
          roughness={0.1}
          emissive={baseColor}
          emissiveIntensity={emissiveIntensity}
          clearcoat={1.0}
          clearcoatRoughness={0.1}
        />
        
        {/* Etched Grid Lines on Wafer */}
        <lineSegments>
          <edgesGeometry args={[new THREE.CylinderGeometry(2.5, 2.5, 0.1, 16)]} />
          <lineBasicMaterial color={riskLevel === 'IDLE' ? '#94a3b8' : '#ffffff'} transparent opacity={0.3} />
        </lineSegments>
      </mesh>
      
      {/* Dynamic Sparkles based on scanning/high risk */}
      {(riskLevel === 'SCANNING' || riskLevel === 'HIGH') && (
        <Sparkles 
          count={100} 
          scale={6} 
          size={3} 
          speed={0.4} 
          opacity={0.8} 
          color={baseColor} 
        />
      )}
    </Float>
  );
}

export default function Wafer3DScene({ riskLevel }: WaferProps) {
  return (
    <div style={{ width: '100%', height: '100%', position: 'absolute', top: 0, left: 0 }}>
      <Canvas camera={{ position: [0, 0, 6], fov: 45 }}>
        <color attach="background" args={['transparent']} />
        
        <ambientLight intensity={0.5} />
        <spotLight position={[10, 10, 10]} angle={0.15} penumbra={1} intensity={2} />
        <pointLight position={[-10, -10, -10]} intensity={1} color="#00f0ff" />
        
        <Stars radius={100} depth={50} count={2000} factor={4} saturation={0} fade speed={1} />
        
        <SemiconductorWafer riskLevel={riskLevel} />
        
        <OrbitControls 
          enableZoom={false} 
          enablePan={false}
          autoRotate={false}
          maxPolarAngle={Math.PI / 1.5}
          minPolarAngle={Math.PI / 3}
        />
      </Canvas>
    </div>
  );
}
