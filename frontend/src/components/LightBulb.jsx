
const intensity = 20;
const distance = 100;
const decay = 1.5;


export default function LightBulb() {
  return (
    <group position={[4, 4, 4]}>
      {/* Quả cầu phát sáng */}
      <mesh>
        <sphereGeometry args={[0.1, 32, 32]} />
        <meshStandardMaterial
          emissive="#ffffff"
          emissiveIntensity={intensity / 2} // Điều chỉnh theo cường độ ánh sáng
          color="#ffffff"
        />
      </mesh>

      {/* Nguồn sáng từ quả cầu */}
      <pointLight
        castShadow
        intensity={intensity}
        distance={distance}
        decay={decay}
        color="#ffffff"
        shadow-mapSize-width={720}
        shadow-mapSize-height={720}
        shadow-bias={-0.001}
        shadow-camera-near={1}
        shadow-camera-far={50}
        shadow-camera-left={-10}
        shadow-camera-right={10}
        shadow-camera-top={10}
        shadow-camera-bottom={-10}
      />
    </group>
  );
}
