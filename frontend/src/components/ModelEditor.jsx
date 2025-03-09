import React, { useRef, useState, useEffect, Suspense } from 'react'
import { Canvas } from '@react-three/fiber'
import {
  ContactShadows,
  OrbitControls,
  TransformControls,
  useGLTF,
  useHelper
} from '@react-three/drei'
import * as THREE from 'three'
import { BoxHelper } from 'three'
import { GLTFExporter } from 'three/examples/jsm/exporters/GLTFExporter.js'

import LightBulb from './LightBulb'
import HollowCube from './HollowCube'

function ModelItem({ path, onLeftClick, onRightClick, selectedRef, position = [0, 0, 0] }) {
  const { scene } = useGLTF(path)
  const itemRef = useRef()

  const isSelected = selectedRef === itemRef
  useHelper(isSelected ? itemRef : null, BoxHelper, 'orange')

  const handlePointerDown = (e) => {
    if (e.button === 0) {
      e.stopPropagation()
      onLeftClick(itemRef)
    } else if (e.button === 2) {
      e.stopPropagation()
      e.nativeEvent.preventDefault()
      onRightClick(e, itemRef)
      onLeftClick(itemRef)
    }
  } 
  
  useEffect(() => {
    // Đệ quy qua tất cả các mesh trong model để bật shadow
    scene.traverse((child) => {
      if (child.isMesh) {
        child.castShadow = true;
        child.receiveShadow = true;
        if (child.material) {
          child.material.shadowSide = THREE.DoubleSide;
        }
      }
    });
  }, [scene]);

  return (
    <group ref={itemRef} position={position} onPointerDown={handlePointerDown}>
      <primitive object={scene} />
    </group>
  )
}

export default function ModelEditor({ models }) {
  const [selectedRef, setSelectedRef] = useState(null)
  const [mode, setMode] = useState('translate')
  const transformRef = useRef()
  const orbitRef = useRef()
  const userModelsRef = useRef()
  // Thêm ref cho HollowCube
  const hollowCubeRef = useRef()

  const [history, setHistory] = useState([])
  const dragStartDataRef = useRef(null)
  const [ROOMSIZE, setROOMSIZE] = useState(5)
  const [ROOMTHICKNESS, setROOMTHICKNESS] = useState(0.1)

  const handleUndo = () => {
    setHistory((prev) => {
      if (!prev.length) return prev
      const last = prev[prev.length - 1]
      const { ref, oldTransform } = last
      if (ref?.current) {
        ref.current.position.copy(oldTransform.position)
        ref.current.rotation.copy(oldTransform.rotation)
        ref.current.scale.copy(oldTransform.scale)
      }
      return prev.slice(0, -1)
    })
  }

  useEffect(() => {
    if (!transformRef.current) return
    const controls = transformRef.current

    const handleDraggingChanged = () => {
      if (!selectedRef?.current) return
      if (controls.dragging) {
        const obj = selectedRef.current
        dragStartDataRef.current = {
          ref: selectedRef,
          oldTransform: {
            position: obj.position.clone(),
            rotation: obj.rotation.clone(),
            scale: obj.scale.clone()
          }
        }
      } else {
        if (dragStartDataRef.current) {
          const obj = selectedRef.current
          const newTransform = {
            position: obj.position.clone(),
            rotation: obj.rotation.clone(),
            scale: obj.scale.clone()
          }
          const historyItem = {
            ...dragStartDataRef.current,
            newTransform
          }
          setHistory((prev) => [...prev, historyItem])
          dragStartDataRef.current = null
        }
      }
    }

    controls.addEventListener('dragging-changed', handleDraggingChanged)
    return () => {
      controls.removeEventListener('dragging-changed', handleDraggingChanged)
    }
  }, [selectedRef])

  const [contextMenu, setContextMenu] = useState({
    show: false,
    x: 0,
    y: 0,
    modelRef: null
  })

  const handleRightClick = (e, modelRef) => {
    setContextMenu({
      show: true,
      x: e.clientX,
      y: e.clientY,
      modelRef
    })
  }
  const handleSelectMode = (newMode) => {
    setMode(newMode)
    if (contextMenu.modelRef) {
      setSelectedRef(contextMenu.modelRef)
    }
    setContextMenu((prev) => ({ ...prev, show: false }))
  }
  const handleClickOutside = () => {
    if (contextMenu.show) {
      setContextMenu((prev) => ({ ...prev, show: false }))
    }
  }

  // Hàm xuất file GLTF đã được chỉnh sửa
  const exportAsGltf = () => {
    // Kiểm tra cả hai ref có tồn tại hay không
    if (!userModelsRef.current || !hollowCubeRef.current) return
    const yes = window.confirm('Xuất tất cả mô hình sang file .gltf? (Bỏ qua camera, lights)')
    if (!yes) return

    // Cập nhật matrix cho cả 2 nhóm
    hollowCubeRef.current.updateMatrixWorld(true)
    userModelsRef.current.updateMatrixWorld(true)

    // Tạo một group mới để chứa cả hollowcube và các mô hình của người dùng
    const combinedGroup = new THREE.Group()

    // Clone các group để không ảnh hưởng đến scene gốc
    const hollowCubeClone = hollowCubeRef.current.clone()
    const userModelsClone = userModelsRef.current.clone()

    combinedGroup.add(hollowCubeClone)
    combinedGroup.add(userModelsClone)
    combinedGroup.updateMatrixWorld(true)

    const exporter = new GLTFExporter()
    exporter.parse(
      combinedGroup,
      (gltfJson) => {
        const dataStr = JSON.stringify(gltfJson, null, 2)
        const blob = new Blob([dataStr], { type: 'application/json' })
        const url = URL.createObjectURL(blob)
        const link = document.createElement('a')
        link.style.display = 'none'
        link.href = url
        link.download = 'user_models.gltf'
        document.body.appendChild(link)
        link.click()
        document.body.removeChild(link)
        URL.revokeObjectURL(url)
      },
      {
        binary: false,
        embedImages: true,
      }
    )
  }

  useEffect(() => {
    const handleKeyDown = (e) => {
      if (e.ctrlKey && e.key === 'k') {
        e.preventDefault();
        console.log('[k] pressed: setSelectedRef(null) + detach transform')
        setSelectedRef(null)
        if (transformRef.current) {
          transformRef.current.detach()
          transformRef.current.object = null
          transformRef.current.enabled = false
          transformRef.current.visible = false
          console.log('>>> transformControls after K pressed:', transformRef.current)
        }
      }
      if (e.ctrlKey && e.key === 'z') {
        e.preventDefault();
        console.log('[z] pressed => Undo last transform')
        e.stop
        handleUndo()
      }
      if (e.ctrlKey && e.key === 'd') {
        e.preventDefault();
        exportAsGltf()
      }
    }
    window.addEventListener('keydown', handleKeyDown)
    return () => window.removeEventListener('keydown', handleKeyDown)
  }, [])

  return (
    <div style={{ width: '100vw', height: '100vh', backgroundColor: "#f0f0f0" , position:"relative" }} onClick={handleClickOutside}>
      <Canvas shadows>
        <color attach="background" args={['#15151a']} />
        <OrbitControls ref={orbitRef} />
        <hemisphereLight intensity={0.5} />
        <ContactShadows resolution={1024} frames={1} position={[0, -1.16, 0]} scale={15} blur={0.5} opacity={1} far={20} />
        <LightBulb />
        <axesHelper args={[6]} />
        <Suspense fallback={null}>
          <TransformControls
            ref={transformRef}
            mode={mode}
            object={selectedRef?.current || null}
            onChange={() => {
              if (transformRef.current) {
                orbitRef.current.enabled = !transformRef.current.dragging
              }
            }}
          />
          {/* Bọc HollowCube trong một group có ref */}
          <group ref={hollowCubeRef}>
            <HollowCube
              size={ROOMSIZE}
              thickness={ROOMTHICKNESS}
              position={[
                ROOMSIZE / 2 - ROOMTHICKNESS,
                ROOMSIZE / 2 - ROOMTHICKNESS,
                ROOMSIZE / 2 - ROOMTHICKNESS
              ]}
            />
          </group>
          <group ref={userModelsRef}>
            {models.map(({ id, path, position }) => (
              <ModelItem
                key={id}
                path={path}
                position={position}
                selectedRef={selectedRef}
                onLeftClick={(ref) => {
                  setSelectedRef(ref)
                  if (transformRef.current) {
                    transformRef.current.enabled = true
                    transformRef.current.visible = true
                  }
                }}
                onRightClick={handleRightClick}
              />
            ))}
          </group>
        </Suspense>
      </Canvas>
      <div
        style={{
          position: 'absolute',
          bottom: 0,
          right: 10,
          background: 'rgba(255,255,255,0.5)',
          padding: '8px',
          borderRadius: '4px',
          transform : "translateY(-100%)",
          zIndex: 999
        }}
      >
        <div>
        </div>
        <div style={{ marginTop: 8 }}>
          <div>[ctr] + [k] : Unhighlight</div>
          <div>[ctr] + [z] : Undo</div>
          <div>[ctr] + [d] : Download .gltf</div>
        </div>
      </div>
      {contextMenu.show && (
        <div
          style={{
            position: 'absolute',
            top: contextMenu.y,
            left: contextMenu.x,
            background: '#fff',
            border: '1px solid #ccc',
            borderRadius: '4px',
            padding: '8px',
            zIndex: 9999,
            cursor: 'pointer'
          }}
        >
          <div onClick={() => handleSelectMode('translate')}>Translate</div>
          <div onClick={() => handleSelectMode('rotate')}>Rotate</div>
          <div onClick={() => handleSelectMode('scale')}>Scale</div>
        </div>
      )}
    </div>
  )
}
