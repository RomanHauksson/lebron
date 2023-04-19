import { createChatBotMessage } from 'react-chatbot-kit';

const botName = 'LEBRON';

const config = {
  initialMessages: [
    createChatBotMessage(`Hi, my name's ${botName}! I'm here to help demystify the world of basketball statistics for you. What would you like to know?`),
  ],
  botName: botName,
  customStyles: { 
    botMessageBox: {
      backgroundColor: '#376B7E',
    },
    chatButton: {
      backgroundColor: '#5ccc9d',
    },
  },
};

export default config;