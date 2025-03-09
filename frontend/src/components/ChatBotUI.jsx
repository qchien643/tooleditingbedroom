import React, { useState } from 'react';
import {
  MainContainer,
  ChatContainer,
  MessageList,
  Message,
  MessageInput,
  TypingIndicator
} from '@chatscope/chat-ui-kit-react';
import '@chatscope/chat-ui-kit-styles/dist/default/styles.min.css';

import sendDataBackend from '../ultis/sendtobackend';

const ChatbotUI = () => {
  // Danh sách tin nhắn
  const [messages, setMessages] = useState([]);
  // Biến kiểm soát: nếu đang chờ phản hồi của bot thì disable input
  const [isAwaitingBot, setIsAwaitingBot] = useState(false);
  // Biến hiển thị trạng thái "bot đang gõ"
  const [isTyping, setIsTyping] = useState(false);

  const handleSend = (text) => {
    // Nếu đang chờ phản hồi từ bot, không cho phép gửi thêm tin
    if (isAwaitingBot) return;

    // Tạo tin nhắn của người dùng
    const newUserMessage = {
      id: messages.length + 1,
      sender: 'user',
      message: text,
    };

    // Cập nhật danh sách tin nhắn và set trạng thái chờ phản hồi
    setMessages((prev) => [...prev, newUserMessage]);
    setIsAwaitingBot(true);
    setIsTyping(true);

    // Giả lập phản hồi của bot sau 2 giây
    setTimeout(() => {

      const botMessage = sendDataBackend({
        data : messages,
        flag : "100"
      });
      console.log(botMessage);

      const newBotMessage = {
        id: messages.length + 2,
        sender: 'bot',
        message: JSON.stringify(botMessage)
      };

      setMessages((prev) => [...prev, newBotMessage]);
      setIsAwaitingBot(false);
      setIsTyping(false);
    }, 2000);
  };

  return (
    <div className="chat-container" style={{height:"100%" , width:"100%" } }>
      <MainContainer>
      <ChatContainer>
        <MessageList 
          typingIndicator={isTyping ? <TypingIndicator content="Bot is typing..." /> : null}
        >
          {messages.map((msg) => (
            <Message
              key={msg.id}
              model={{
                message: msg.message,
                // Đặt tên hiển thị theo sender
                sender: msg.sender === 'bot' ? 'Bot' : 'You',
                // Chỉ định hướng của tin nhắn
                direction: msg.sender === 'bot' ? 'incoming' : 'outgoing',
                position: 'normal',
              }}
            />
          ))}
        </MessageList>
        <MessageInput 
          placeholder="Nhập tin nhắn..."
          onSend={handleSend}
          disabled={isAwaitingBot} // disable input nếu đang chờ phản hồi
        />
      </ChatContainer>
    </MainContainer>
    </div>
    
  );
};

export default ChatbotUI;
