import { ReactFlowProvider } from '@xyflow/react';

import { PanelGroup, Panel, PanelResizeHandle } from 'react-resizable-panels';

import "./App.css";

import ModelEditor from "./components/ModelEditor"
import Flowchart from "./components/FlowChart"
import ChatbotUI from './components/ChatBotUI';

  const models = [
    { id: 'modelA', path: './adjust_root_optimize/bed_1.glb', position: [0, 0, 0] },
    { id: 'modelB', path: './adjust_root_optimize/bed_simple.glb', position: [0, 0, 0] },
  ]

  const chatdata =  [
    {
      "id": 1,
      "sender": "user",
      "message": "Xin chào!",
      
    },
    {
      "id": 2,
      "sender": "bot",
      "message": "Chào bạn! Tôi có thể giúp gì cho bạn?",
      
    }
  ] 

// export default function App() {
//   return (
//     <ChatbotUI data={chatdata}/>
//   )
// }

export default function App(){
  return (
    <div className="container">
      {/* Thanh title */}
      <div className="container-title">
        <h1>DESIGN YOUR BEDROOM</h1>
      </div>

      {/* Thanh sidebar */}
      <div className="container-sidebar">
        <p>Sidebar</p>
      </div>

      {/*
        Vùng chính gồm hai phần:
          - Bên trái: gồm 2 vùng được sắp xếp theo chiều dọc (flowchart và chatbot)
          - Bên phải: model
        Sử dụng PanelGroup theo hướng ngang, bên trái là một PanelGroup theo hướng dọc.
      */}
      <div className="container-main">
        <PanelGroup direction="horizontal">
          {/* Left column: chứa flowchart (trên) và chatbot (dưới) */}
          <Panel defaultSize={40} minSize={20}>
            <PanelGroup direction="vertical">
              <Panel defaultSize={50} minSize={20}>
                <div className="container-user-flowchart">
                  <ReactFlowProvider>
                  <Flowchart />
                  </ReactFlowProvider>
                  
                </div>
              </Panel>
              <PanelResizeHandle className="custom-handle" />
              <Panel defaultSize={50} minSize={20}>
                <div className="container-user-chatbot">
                <ChatbotUI data={chatdata}/>
                </div>
              </Panel>
            </PanelGroup>
          </Panel>
          <PanelResizeHandle className="custom-handle" />
          {/* Right column: model */}
          <Panel defaultSize={60} minSize={20}>
            <div className="container-user-model">
              <ModelEditor models = {models}/>
            </div>
          </Panel>
        </PanelGroup>
      </div>

      {/* Footer */}
      <div className="container-footer">
        <p>AUTHOR : NGUYEN QUANG CHIEN</p>
        
        <p><a href="mailto:nguyenquanhchienpp2303@gmail.com">Contact : nguyenquanhchienpp2303@gmail.com</a></p>
      </div>
    </div>
  );
}