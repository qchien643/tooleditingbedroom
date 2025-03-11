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
  // Kiểm soát "đang chờ bot trả lời" để disable input
  const [isAwaitingBot, setIsAwaitingBot] = useState(false);
  // Hiển thị trạng thái "bot đang gõ"
  const [isTyping, setIsTyping] = useState(false);
  

  async function handleSend(inputText) {
    // Nếu đang chờ phản hồi từ bot, không cho phép gửi thêm
    if (isAwaitingBot) return;

    // Loại bỏ các thẻ HTML khỏi text (nếu có)
    const text = inputText.replace(/<[^>]*>/g, "");

    // Tạo tin nhắn mới của user
    const newUserMessage = {
      id: messages.length + 1,
      sender: 'user',
      message: text,
    };

    // Cập nhật danh sách tin nhắn
    const updatedMessages = [...messages, newUserMessage];
    setMessages(updatedMessages);

    // Chuyển sang trạng thái chờ phản hồi
    setIsAwaitingBot(true);
    setIsTyping(true);

    // Gọi API/hàm gửi dữ liệu tới backend
    const botResponse = await sendDataBackend({
      data: updatedMessages,
      flag: 'message'
    });

    // Tạo tin nhắn phản hồi của bot
    const newBotMessage = {
      id: updatedMessages.length + 1,
      sender: 'bot',
      message: JSON.stringify(botResponse.data) // tuỳ cách hiển thị
    };

    // Thêm tin nhắn bot vào danh sách
    setMessages(prev => [...prev, newBotMessage]);

    // Kết thúc trạng thái chờ
    setIsAwaitingBot(false);
    setIsTyping(false);
  }

  return (
    <div className="chat-container" style={{ height: '100%', width: '100%' }}>
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
                  sender: msg.sender === 'bot' ? 'Bot' : 'You',
                  direction: msg.sender === 'bot' ? 'incoming' : 'outgoing',
                  position: 'normal',
                }}
              />
            ))}
          </MessageList>

          <MessageInput
            placeholder="Nhập tin nhắn..."
            onSend={handleSend}
            disabled={isAwaitingBot} // disable khi đang chờ phản hồi
          />
        </ChatContainer>
      </MainContainer>
    </div>
  );
};

export default ChatbotUI;
