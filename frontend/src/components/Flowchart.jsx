import React, { useState } from 'react';
import sendDataBackend from '../ultis/sendtobackend';
import {
  ReactFlow,
  useNodesState,
  useEdgesState,
  Background,
  MiniMap,
  Controls,
  Handle,
} from '@xyflow/react';
import '@xyflow/react/dist/style.css';
import './Flowchart.css';


// -------------------------
// (Các biến modelsData và placementsData được định nghĩa như cũ)
const modelsData = {
  "bed": [
      "bed_1",
      "bed_simple",
      "poliform_bed",
      "queen-bed"
  ],
  "chair": [
      "fly_dinner_chair",
      "gaming_chair",
      "ikea_markus_office_chair",
      "office_chair",
      "quersus_gaming_chair_vaos.3.1_pearl_white"
  ],
  "decorateFurniture": [
      "lewie_console_table",
      "shelf",
      "table_furniture",
      "wooden_cupboard_with_door"
  ],
  "door": [
      "door_with_cardreader",
      "modern_door",
      "modern_door_1",
      "modern_metal_windowed_door",
      "modern_wood_door"
  ],
  "rug": [
      "bhadoi_rug",
      "kuuma_ye_rug_by_kristiina_lassus"
  ],
  "table": [
      "desk",
      "folding_table",
      "industrial_table",
      "modern_industrial_desk",
      
      "office_desk_140x60",
      "simple_office_table",
      "soviet_table",
      "table",
      "table_1"
  ],
  "wardrobe": [
      "celestine_four_door_wardrobeobj",
      "wardrobe_classic",
      "wardrobe_low_poly"
  ],
  "window": [
      "pvc_still_window_with_sill",
      "window_1",
      "window_3",
      "window_4",
      "window_5"
  ]
};

const placementsData = {"bed": [["NextToWallRule None ['N', 'W'] left", "SameDirectionWall None ['N', 'W']"], ["NextToWallRule None ['N', 'E'] left", "SameDirectionWall None ['N', 'E']"], ["NextToWallRule None ['E', 'N'] left", "SameDirectionWall None ['E', 'N']"], ["NextToWallRule None ['E', 'S'] left", "SameDirectionWall None ['E', 'S']"], ["NextToWallRule None ['S', 'E'] left", "SameDirectionWall None ['S', 'E']"], ["NextToWallRule None ['S', 'W'] left", "SameDirectionWall None ['S', 'W']"], ["NextToWallRule None ['W', 'N'] left", "SameDirectionWall None ['W', 'N']"], ["NextToWallRule None ['W', 'S'] left", "SameDirectionWall None ['W', 'S']"], ["InCenterWall None ['N'] left", "SameDirectionWall None ['N']"], ["InCenterWall None ['E'] left", "SameDirectionWall None ['E']"], ["InCenterWall None ['S'] left", "SameDirectionWall None ['S']"], ["InCenterWall None ['W'] left", "SameDirectionWall None ['W']"]], "table": [["NextToWallRule None ['N', 'W'] left", "SameDirectionWall None ['N', 'W']"], ["NextToWallRule None ['N', 'E'] left", "SameDirectionWall None ['N', 'E']"], ["NextToWallRule None ['E', 'N'] left", "SameDirectionWall None ['E', 'N']"], ["NextToWallRule None ['E', 'S'] left", "SameDirectionWall None ['E', 'S']"], ["NextToWallRule None ['S', 'E'] left", "SameDirectionWall None ['S', 'E']"], ["NextToWallRule None ['S', 'W'] left", "SameDirectionWall None ['S', 'W']"], ["NextToWallRule None ['W', 'N'] left", "SameDirectionWall None ['W', 'N']"], ["NextToWallRule None ['W', 'S'] left", "SameDirectionWall None ['W', 'S']"], ["InCenterWall None ['N'] left", "SameDirectionWall None ['N']"], ["InCenterWall None ['E'] left", "SameDirectionWall None ['E']"], ["InCenterWall None ['S'] left", "SameDirectionWall None ['S']"], ["InCenterWall None ['W'] left", "SameDirectionWall None ['W']"], ["RightOfFurnitureRule bed [] left", "SameDirection bed []"], ["LeftOfFurnitureRule bed [] left", "SameDirection bed []"]], "chair": [["BehindFurnitureRule table [] center", "SameDirection table []"]], "wardrobe": [["NextToWallRule None ['N', 'W'] left", "OppostieDirectionWall None ['N', 'W']"], ["NextToWallRule None ['N', 'E'] left", "OppostieDirectionWall None ['N', 'E']"], ["NextToWallRule None ['E', 'N'] left", "OppostieDirectionWall None ['E', 'N']"], ["NextToWallRule None ['E', 'S'] left", "OppostieDirectionWall None ['E', 'S']"], ["NextToWallRule None ['S', 'E'] left", "OppostieDirectionWall None ['S', 'E']"], ["NextToWallRule None ['S', 'W'] left", "OppostieDirectionWall None ['S', 'W']"], ["NextToWallRule None ['W', 'N'] left", "OppostieDirectionWall None ['W', 'N']"], ["NextToWallRule None ['W', 'S'] left", "OppostieDirectionWall None ['W', 'S']"], ["InCenterWall None ['N'] left", "OppostieDirectionWall None ['N']"], ["InCenterWall None ['E'] left", "OppostieDirectionWall None ['E']"], ["InCenterWall None ['S'] left", "OppostieDirectionWall None ['S']"], ["InCenterWall None ['W'] left", "OppostieDirectionWall None ['W']"], ["BehindFurnitureRule bed [] left", "PerpendicularPositive bed []"], ["NextToWallRule None ['E', 'S'] left", "OppostieDirectionWall None ['E', 'S']"], ["NextToWallRule None ['W', 'S'] left", "OppostieDirectionWall None ['W', 'S']"], ["InCenterWall None ['N'] left", "OppostieDirectionWall None ['N']"], ["InCenterWall None ['E'] left", "OppostieDirectionWall None ['E']"], ["InCenterWall None ['S'] left", "OppostieDirectionWall None ['S']"], ["InCenterWall None ['W'] left", "OppostieDirectionWall None ['W']"]], "door": [["NextToWallRule None ['N', 'W'] left", "SameDirectionWall None ['N', 'W']"], ["NextToWallRule None ['N', 'E'] left", "SameDirectionWall None ['N', 'E']"], ["NextToWallRule None ['E', 'N'] left", "SameDirectionWall None ['E', 'N']"], ["NextToWallRule None ['E', 'S'] left", "SameDirectionWall None ['E', 'S']"], ["NextToWallRule None ['S', 'E'] left", "SameDirectionWall None ['S', 'E']"], ["NextToWallRule None ['S', 'W'] left", "SameDirectionWall None ['S', 'W']"], ["NextToWallRule None ['W', 'N'] left", "SameDirectionWall None ['W', 'N']"], ["NextToWallRule None ['W', 'S'] left", "SameDirectionWall None ['W', 'S']"], ["InCenterWall None ['N'] left", "SameDirectionWall None ['N']"], ["InCenterWall None ['E'] left", "SameDirectionWall None ['E']"], ["InCenterWall None ['S'] left", "SameDirectionWall None ['S']"], ["InCenterWall None ['W'] left", "SameDirectionWall None ['W']"]], "window": [["OnAboveFurnitureRule bed [] left", "OppositeDirection bed []"], ["OnAboveFurnitureRule table [] left", "OppositeDirection table []"], ["NextToWallRule None ['W'] left", "OppostieDirectionWall None ['W']"], ["NextToWallRule None ['E'] left", "OppostieDirectionWall None ['E']"], ["NextToWallRule None ['S'] left", "OppostieDirectionWall None ['S']"], ["NextToWallRule None ['N'] left", "OppostieDirectionWall None ['N']"], ["InCenterWall None ['N'] left", "OppostieDirectionWall None ['N']"], ["InCenterWall None ['E'] left", "OppostieDirectionWall None ['E']"], ["InCenterWall None ['S'] left", "OppostieDirectionWall None ['S']"], ["InCenterWall None ['W'] left", "OppostieDirectionWall None ['W']"]], "rug": [["NextToWallRule None ['N', 'W'] left", "SameDirectionWall None ['N', 'W']"], ["NextToWallRule None ['N', 'E'] left", "SameDirectionWall None ['N', 'E']"], ["NextToWallRule None ['E', 'N'] left", "SameDirectionWall None ['E', 'N']"], ["NextToWallRule None ['E', 'S'] left", "SameDirectionWall None ['E', 'S']"], ["NextToWallRule None ['S', 'E'] left", "SameDirectionWall None ['S', 'E']"], ["NextToWallRule None ['S', 'W'] left", "SameDirectionWall None ['S', 'W']"], ["NextToWallRule None ['W', 'N'] left", "SameDirectionWall None ['W', 'N']"], ["NextToWallRule None ['W', 'S'] left", "SameDirectionWall None ['W', 'S']"], ["InCenterWall None ['N'] left", "SameDirectionWall None ['N']"], ["InCenterWall None ['E'] left", "SameDirectionWall None ['E']"], ["InCenterWall None ['S'] left", "SameDirectionWall None ['S']"], ["InCenterWall None ['W'] left", "SameDirectionWall None ['W']"], ["RightOfFurnitureRule bed [] left", "PerpendicularPositive bed []"], ["LeftOfFurnitureRule bed [] left", "PerpendicularPositive bed []"], ["BehindFurnitureRule bed [] left", "SameDirection bed []"], ["BehindFurnitureRule door [] center", "SameDirection door []"]], "decorateFurniture": [["NextToWallRule None ['N', 'W'] left", "SameDirectionWall None ['N', 'W']"], ["NextToWallRule None ['N', 'E'] left", "SameDirectionWall None ['N', 'E']"], ["NextToWallRule None ['E', 'N'] left", "SameDirectionWall None ['E', 'N']"], ["NextToWallRule None ['E', 'S'] left", "SameDirectionWall None ['E', 'S']"], ["NextToWallRule None ['S', 'E'] left", "SameDirectionWall None ['S', 'E']"], ["NextToWallRule None ['S', 'W'] left", "SameDirectionWall None ['S', 'W']"], ["NextToWallRule None ['W', 'N'] left", "SameDirectionWall None ['W', 'N']"], ["NextToWallRule None ['W', 'S'] left", "SameDirectionWall None ['W', 'S']"], ["InCenterWall None ['N'] left", "SameDirectionWall None ['N']"], ["InCenterWall None ['E'] left", "SameDirectionWall None ['E']"], ["InCenterWall None ['S'] left", "SameDirectionWall None ['S']"], ["InCenterWall None ['W'] left", "SameDirectionWall None ['W']"]]}


// Các danh sách texture cho floor và wall
const floorTextures = ["wood", "tile", "marble"];
const wallTextures = ["brick", "paint", "wallpaper"];

// -------------------------
// Component RoomNode (chỉnh sửa thêm mục floor, wall, dimension)
const RoomNode = ({ id, data }) => {
  const { onRoomUpdate } = data;
  const [floor, setFloor] = useState(data.floor || "");
  const [wall, setWall] = useState(data.wall || "");
  const [dimension, setDimension] = useState(data.dimension || "");

  const handleFloorChange = (e) => {
    setFloor(e.target.value);
    onRoomUpdate({ floor: e.target.value, wall, dimension });
  };

  const handleWallChange = (e) => {
    setWall(e.target.value);
    onRoomUpdate({ floor, wall: e.target.value, dimension });
  };

  const handleDimensionChange = (e) => {
    setDimension(e.target.value);
    onRoomUpdate({ floor, wall, dimension: e.target.value });
  };

  return (
    <div
      data-nodeid={id}
      style={{
        padding: 10,
        width: 250,
        background: '#050305',
        borderRadius: '8px',
        border: '2px solid transparent',
        borderImage: 'linear-gradient(90deg, #36123F, #624343, #8F37B1) 1',
        boxShadow: '0 0 10px #624343, 0 0 20px #8F37B1',
        color: '#8F37B1',
        fontFamily: 'Telegraf, sans-serif',
        fontWeight: 'bold',
        textShadow: '0 0 10px #8F37B1',
      }}
    >
      <div style={{ textAlign: 'center', marginBottom: 8 }}>{data.label}</div>
      <div style={{ marginBottom: 8 }}>
        <label style={{ fontSize: '12px' }}>
          <strong>Floor:</strong>
        </label>
        <select
          value={floor}
          onChange={handleFloorChange}
          style={{
            width: '100%',
            backgroundColor: '#050305',
            color: '#8F37B1',
            border: '1px solid #36123F',
            borderRadius: '4px',
            padding: '4px',
            fontSize: '12px',
            textAlign: 'center'
          }}
        >
          <option value="">choose texture floor</option>
          {floorTextures.map((tex, idx) => (
            <option key={idx} value={tex}>{tex}</option>
          ))}
        </select>
      </div>
      <div style={{ marginBottom: 8 }}>
        <label style={{ fontSize: '12px' }}>
          <strong>Wall:</strong>
        </label>
        <select
          value={wall}
          onChange={handleWallChange}
          style={{
            width: '100%',
            backgroundColor: '#050305',
            color: '#8F37B1',
            border: '1px solid #36123F',
            borderRadius: '4px',
            padding: '4px',
            fontSize: '12px',
            textAlign: 'center'
          }}
        >
          <option value="">choose texture wall</option>
          {wallTextures.map((tex, idx) => (
            <option key={idx} value={tex}>{tex}</option>
          ))}
        </select>
      </div>
      <div style={{ marginBottom: 8 }}>
        <label style={{ fontSize: '12px' }}>
          <strong>Dimension:</strong>
        </label>
        <input
          type="text"
          value={dimension}
          onChange={handleDimensionChange}
          placeholder="input dimension"
          style={{
            width: '100%',
            backgroundColor: '#050305',
            color: '#8F37B1',
            border: '1px solid #36123F',
            borderRadius: '4px',
            padding: '4px',
            fontSize: '12px',
            textAlign: 'center',
            
          }}
        />
      </div>
      <Handle 
        type="source" 
        position="right" 
        id="a" 
        style={{ background: '#8F37B1', width: 12, height: 12 }} 
      />
    </div>
  );
};

// -------------------------
// Component ObjectNode (không thay đổi phần này)
const ObjectNode = ({ id, data }) => {
  const { onUpdate, initialType = "", initialModel = "", initialPlacement = [] } = data;
  const [objectType, setObjectType] = useState(initialType);
  const [model, setModel] = useState(initialModel);
  const [placement, setPlacement] = useState(initialPlacement);

  const handleTypeChange = (e) => {
    const newType = e.target.value;
    setObjectType(newType);
    setModel("");
    setPlacement([]);
    onUpdate(id, { type: newType, model: "", placement: [] });
  };

  const handleModelChange = (e) => {
    const newModel = e.target.value;
    setModel(newModel);
    onUpdate(id, { type: objectType, model: newModel, placement });
  };

  const handlePlacementChange = (e) => {
    const value = e.target.value;
    let newPlacement = [];
    if (value !== "") {
      newPlacement = JSON.parse(value);
    }
    setPlacement(newPlacement);
    onUpdate(id, { type: objectType, model, placement: newPlacement });
  };

  const modelOptions = objectType ? (modelsData[objectType] || []) : [];
  const placementOptions = objectType ? (placementsData[objectType] || []) : [];

  return (
    <div
      data-nodeid={id}
      style={{
        padding: 10,
        borderRadius: '8px',
        background: '#050305',
        width: 300,
        height: 200,
        border: '2px solid transparent',
        borderImage: 'linear-gradient(90deg, #36123F, #624343, #8F37B1) 1',
        boxShadow: '0 0 10px #36123F, 0 0 20px #624343',
        color: '#8F37B1',
        fontFamily: 'Telegraf, sans-serif',
        fontWeight: 'bold',
        textShadow: '0 0 10px #8F37B1',
        textAlign: 'center',
        position: 'relative'
      }}
      
    >
      <Handle 
        type="target" 
        position="left" 
        id="target" 
        style={{ background: '#8F37B1', width: 12, height: 12 }} 
      />
      <div style={{ marginBottom: 8 }}>
        <label style={{ fontSize: '14px', display: 'block' }}>
          <strong>type of furniture:</strong>
        </label>
        <select
          value={objectType}
          onChange={handleTypeChange}
          style={{
            width: '100%',
            maxWidth: '280px',
            backgroundColor: '#050305',
            color: '#8F37B1',
            border: '1px solid #36123F',
            borderRadius: '4px',
            padding: '4px',
            fontSize: '14px',
            textAlign: 'center'
          }}
        >
          <option value="">Choose type</option>
          {Object.keys(modelsData).map((key) => (
            <option key={key} value={key}>{key}</option>
          ))}
        </select>
      </div>
      <div style={{ marginBottom: 8 }}>
        <label style={{ fontSize: '14px', display: 'block' }}>
          <strong>model name :</strong>
        </label>
        <select
          value={model}
          onChange={handleModelChange}
          disabled={!objectType}
          style={{
            width: '100%',
            maxWidth: '280px',
            backgroundColor: '#050305',
            color: '#8F37B1',
            border: '1px solid #36123F',
            borderRadius: '4px',
            padding: '4px',
            fontSize: '14px',
            textAlign: 'center'
          }}
        >
          <option value="">choose model</option>
          {modelOptions.map((m) => (
            <option key={m} value={m}>{m}</option>
          ))}
        </select>
      </div>
      <div>
        <label style={{ fontSize: '14px', display: 'block' }}>
          <strong>choose placement</strong>
        </label>
        <div style={{ width: '100%', maxWidth: '280px', margin: '0 auto', position: 'relative' }}>
          <select
            value={placement.length > 0 ? JSON.stringify(placement) : ""}
            onChange={handlePlacementChange}
            disabled={!objectType}
            style={{
              width: '100%',
              backgroundColor: '#050305',
              color: '#8F37B1',
              border: '1px solid #36123F',
              borderRadius: '4px',
              padding: '4px',
              fontSize: '14px',
              overflow: 'hidden',
              textOverflow: 'ellipsis',
              whiteSpace: 'nowrap',
              textAlign: 'center'
            }}
          >
            <option value="">Choose placement</option>
            {placementOptions.map((p, index) => (
              <option key={index} value={JSON.stringify(p)}>
                {p.join(" | ")}
              </option>
            ))}
          </select>
        </div>
      </div>
    </div>
  );
};

function Flowchart() {
  // State lưu trữ cấu hình của room và các objectNode (furnitures)
  const [roomSettings, setRoomSettings] = useState({ floor: "", wall: "", dimension: "" });
  const [placementData, setPlacementData] = useState({ room: [] });
  const [selectedNodeId, setSelectedNodeId] = useState(null);
  const [contextMenu, setContextMenu] = useState({ visible: false, x: 0, y: 0 });

  // Callback cập nhật dữ liệu của room node
  const updateRoomData = (newRoomData) => {
    setRoomSettings(newRoomData);
  };

  const initialNodes = [
    {
      id: "room",
      type: "roomNode",
      position: { x: 250, y: 50 },
      data: { 
        label: "ROOM",
        floor: "",
        wall: "",
        dimension: "",
        onRoomUpdate: updateRoomData
      },
    },
  ];
  const initialEdges = [];

  const [nodes, setNodes, onNodesChange] = useNodesState(initialNodes);
  const [edges, setEdges, onEdgesChange] = useEdgesState(initialEdges);

  const updateObjectData = (id, newData) => {
    if (id !== "room") {
      setPlacementData(prev => {
        const roomArr = prev.room ? [...prev.room] : [];
        const index = roomArr.findIndex(item => item.id === id);
        if (index >= 0) {
          roomArr[index] = { id, ...newData };
        } else {
          roomArr.push({ id, ...newData });
        }
        return { room: roomArr };
      });
    }
  };

  const addNode = () => {
    const newId = `object_${Date.now()}`;
    const newNode = {
      id: newId,
      type: "objectNode",
      position: { x: Math.random() * 400 + 50, y: Math.random() * 300 + 150 },
      data: {
        id: newId,
        onUpdate: updateObjectData,
        onContextMenu: onNodeContextMenu,
        initialType: "",
        initialModel: "",
        initialPlacement: [],
      },
    };
    setNodes(nds => nds.concat(newNode));
    const newEdge = {
      id: `e-room-${newId}`,
      source: "room",
      target: newId,
      sourceHandle: "a",
      targetHandle: "target",
      style: { stroke: '#8F37B1', strokeWidth: 2 }
    };
    setEdges(eds => eds.concat(newEdge));
  };

  const deleteNode = () => {
    if (selectedNodeId && selectedNodeId !== "room") {
      setNodes(nds => nds.filter(n => n.id !== selectedNodeId));
      setEdges(eds => eds.filter(e => e.source !== selectedNodeId && e.target !== selectedNodeId));
      setPlacementData(prev => ({
        room: prev.room.filter(item => item.id !== selectedNodeId)
      }));
      setSelectedNodeId(null);
    }
  };

  const undoLastNode = () => {
    const objectNodes = nodes.filter(n => n.id !== "room");
    if (objectNodes.length > 0) {
      const lastNode = objectNodes[objectNodes.length - 1];
      setNodes(nds => nds.filter(n => n.id !== lastNode.id));
      setEdges(eds => eds.filter(e => e.source !== lastNode.id && e.target !== lastNode.id));
      setPlacementData(prev => ({
        room: prev.room.filter(item => item.id !== lastNode.id)
      }));
    }
  };

  // Hàm xử lý chuyển đổi chuỗi dimension thành mảng
  const parseDimensions = (str) => {
    if (!str) return [];
    return str.split(',').map(s => s.trim());
  };

  // Tính năng autolayout: sắp xếp các node từ trái sang phải với gốc là node room.
  const autoLayout = () => {
    setNodes((nds) => {
      const roomNode = nds.find((n) => n.id === "room");
      if (!roomNode) return nds;
  
      const nodeWidth = 300;  // Giả sử chiều rộng của object node
      const nodeHeight = 200; // Giả sử chiều cao của object node
      const gap = nodeHeight / 4; // Khoảng cách giữa các node = 1/4 chiều cao = 50px
  
      const spacingX = nodeWidth + gap; // Khoảng cách ngang giữa các cột
      const spacingY = nodeHeight + gap; // Khoảng cách dọc giữa các hàng
  
      // Bắt đầu sắp xếp bên phải node room (giả sử room node có width = 250px)
      const roomWidth = 250;
      const startX = roomNode.position.x + roomWidth + gap;
      const startY = roomNode.position.y;
  
      // Lấy tất cả object node (loại trừ room)
      const objectNodes = nds.filter((n) => n.id !== "room");
  
      return nds.map((node) => {
        if (node.id === "room") return node;
        const index = objectNodes.findIndex((n) => n.id === node.id);
        // Sắp xếp theo cột: mỗi cột có 3 hàng (tức, 3 node)
        const row = index % 3;       // Hàng (0, 1, 2)
        const col = Math.floor(index / 3); // Cột (0, 1, 2, ...)
  
        return {
          ...node,
          position: {
            x: startX + col * spacingX,
            y: startY + row * spacingY,
          },
        };
      });
    });
  };
  

  // Khi in ra thông tin:
  // - Console: placement của từng furniture sẽ là index của cách đặt trong placementsData
  // - Alert: placement sẽ là nội dung (string) của cách đặt người dùng chọn
  const startFlow = () => {
    const consoleData = {
      room: {
        floor: roomSettings.floor,
        wall: roomSettings.wall,
        dimension: parseDimensions(roomSettings.dimension)
      },
      furnitures: placementData.room.map(item => {
        const placementIndex = placementsData[item.type]
          ? placementsData[item.type].findIndex(p =>
              JSON.stringify(p) === JSON.stringify(item.placement)
            )
          : -1;
        return {
          type: item.type,
          model: item.model,
          placement: placementIndex
        };
      })
    };

    const alertData = {
      room: {
        floor: roomSettings.floor,
        wall: roomSettings.wall,
        dimension: parseDimensions(roomSettings.dimension)
      },
      furnitures: placementData.room.map(item => {
        return {
          type: item.type,
          model: item.model,
          placement: item.placement.length > 0 ? item.placement.join(" | ") : ""
        };
      })
    };

    console.log("Flow Data:", consoleData);
    // alert(JSON.stringify(alertData, null, 2));
    // console.log(JSON.stringify(alertData, null, 2));
    const res = sendDataBackend({flag : 'flowchart',status : "start" ,data: consoleData});
    
  };

  const handleContextMenu = (event) => {
    event.preventDefault();
    const nodeElement = event.target.closest('[data-nodeid]');
    if (nodeElement) {
      const nodeId = nodeElement.getAttribute('data-nodeid');
      setSelectedNodeId(nodeId);
    } else {
      setSelectedNodeId(null);
    }
    setContextMenu({ visible: true, x: event.clientX, y: event.clientY });
  };

  const handleClick = () => {
    if (contextMenu.visible) setContextMenu({ ...contextMenu, visible: false });
  };

  const onNodeContextMenu = (event, node) => {
    event.preventDefault();
    setSelectedNodeId(node.id);
    setContextMenu({ visible: true, x: event.clientX, y: event.clientY });
  };

  const nodeTypes = { 
    objectNode: ObjectNode, 
    roomNode: RoomNode 
  };

  const contextMenuItemStyle = {
    padding: "4px 8px",
    cursor: "pointer",
    borderBottom: "1px solid #8F37B1",
    fontWeight: "bold",
    textShadow: "0 0 8px #8F37B1",
  };

  return (
    <div
      style={{
        height: "100vh",
        width: "100vw",
        backgroundColor: "#050305",
        fontFamily: "Telegraf, sans-serif",
        fontSize: "16px",
        position: "relative",
      }}
      onContextMenu={handleContextMenu}
      onClick={handleClick}
    >
      <ReactFlow
        nodes={nodes}
        edges={edges}
        onNodesChange={onNodesChange}
        onEdgesChange={onEdgesChange}
        nodeTypes={nodeTypes}
      >
        <Background color="#050305" gap={16} />
        <MiniMap nodeColor={(n) => n.type === 'roomNode' ? '#36123F' : '#8F37B1'} />
        <Controls />
      </ReactFlow>
      {contextMenu.visible && (
        <div
          style={{
            position: "absolute",
            top: contextMenu.y,
            left: contextMenu.x,
            backgroundColor: "#050305",
            border: "1px solid #8F37B1",
            borderRadius: "8px",
            padding: "8px",
            zIndex: 10,
            color: "#8F37B1",
            fontWeight: "bold",
            textShadow: "0 0 8px #8F37B1",
          }}
        >
          <div
            style={contextMenuItemStyle}
            onClick={() => { addNode(); setContextMenu({ ...contextMenu, visible: false }); }}
          >
            add furniture
          </div>
          <div
            style={contextMenuItemStyle}
            onClick={() => { deleteNode(); setContextMenu({ ...contextMenu, visible: false }); }}
          >
            delete 
          </div>
          <div
            style={contextMenuItemStyle}
            onClick={() => { undoLastNode(); setContextMenu({ ...contextMenu, visible: false }); }}
          >
            undo
          </div>
          <div
            style={contextMenuItemStyle}
            onClick={() => { autoLayout(); setContextMenu({ ...contextMenu, visible: false }); }}
          >
            Autolayout
          </div>
          <div
            style={{ ...contextMenuItemStyle, borderBottom: "none" }}
            onClick={() => { startFlow(); setContextMenu({ ...contextMenu, visible: false }); }}
          >
            Start
          </div>
        </div>
      )}
    </div>
  );
}

export default Flowchart;
