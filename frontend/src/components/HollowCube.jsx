import React, { useRef } from 'react';
import { Box } from '@react-three/drei';
import { useFrame, useThree } from '@react-three/fiber';
import * as THREE from 'three';

const HollowCubeFade = ({ size = 1, thickness = 0.1, position = [0, 0, 0] }) => {
  const groupRef = useRef();
  const wallRefs = useRef({});
  const { camera } = useThree();

  const half = size / 2;
  const innerSize = size - 2 * thickness;

  const walls = [
    {
      key: 'top',
      args: [size, thickness, size],
      position: [0, half - thickness / 2, 0],
      outerNormal: new THREE.Vector3(0, 1, 0)
    },
    {
      key: 'bottom',
      args: [size, thickness, size],
      position: [0, -half + thickness / 2, 0],
      outerNormal: new THREE.Vector3(0, -1, 0)
    },
    {
      key: 'front',
      args: [size, innerSize, thickness],
      position: [0, 0, half - thickness / 2],
      outerNormal: new THREE.Vector3(0, 0, 1)
    },
    {
      key: 'back',
      args: [size, innerSize, thickness],
      position: [0, 0, -half + thickness / 2],
      outerNormal: new THREE.Vector3(0, 0, -1)
    },
    {
      key: 'right',
      args: [thickness, innerSize, size],
      position: [half - thickness / 2, 0, 0],
      outerNormal: new THREE.Vector3(1, 0, 0)
    },
    {
      key: 'left',
      args: [thickness, innerSize, size],
      position: [-half + thickness / 2, 0, 0],
      outerNormal: new THREE.Vector3(-1, 0, 0)
    },
  ];

  useFrame((state, delta) => {
    if (!groupRef.current) return;

    const groupWorldPos = new THREE.Vector3();
    groupRef.current.getWorldPosition(groupWorldPos);

    const camDir = new THREE.Vector3();
    camDir.copy(camera.position).sub(groupWorldPos).normalize();

    walls.forEach(wall => {
      const ref = wallRefs.current[wall.key];
      if (ref && ref.material) {
        let targetOpacity = 1;
        if (wall.key !== 'bottom') {
          const dot = camDir.dot(wall.outerNormal);
          targetOpacity = dot <= 0 ? 1 : 0;
        }
        const currentOpacity = ref.material.opacity;
        const newOpacity = THREE.MathUtils.damp(currentOpacity, targetOpacity, 5, delta);
        ref.material.opacity = newOpacity;
        ref.material.transparent = true;
      }
    });
  });

  return (
    <group ref={groupRef} position={position}>
      {walls.map(wall => (
        <Box
          key={wall.key}
          args={wall.args}
          position={wall.position}
          castShadow
          receiveShadow
          ref={el => { wallRefs.current[wall.key] = el; }}
        >
          <meshPhysicalMaterial 
            color="orange"
            opacity={1}
            transparent
            roughness={1}       // Tăng roughness để giảm độ bóng
            metalness={0}       // Loại bỏ hiệu ứng kim loại
            side={THREE.DoubleSide}
            shadowSide={THREE.DoubleSide}
            envMapIntensity={0} // Giảm phản chiếu từ environment map
            clearcoat={0}       // Loại bỏ clearcoat (lớp phủ bóng mịn)
          />
        </Box>
      ))}
    </group>
  );
};

export default HollowCubeFade;
