import { BASE_URL } from '@/config/constants';
import React, { useState, useEffect, useRef } from 'react';
import { trackPromise } from 'react-promise-tracker'
import BouncingDots from './BouncingDots';

const ChatWindow = () => {
  const [userMessages, setUserMessages] = useState<string[]>([]);
  const [systemMessages, setSystemMessages] = useState<string[]>([]);
  const [userInput, setUserInput] = useState<string>('');
  const [systemResponse, setSystemResponse] = useState<string>('');
  const chatWindowRef = useRef<HTMLDivElement>(null);

  
  useEffect(() => {
    if (chatWindowRef == null || chatWindowRef.current == null) return;
    chatWindowRef.current.scrollTop = chatWindowRef.current.scrollHeight;
  }, [userMessages, systemMessages]);


  const handleUserInput = (event: React.ChangeEvent<HTMLTextAreaElement>) => {
    setUserInput(event.target.value);
  };

  const handleSendMessage = () => {
    // Check if user has typed a message
    if (userInput) {
      // Add user's message to state
      setUserMessages([...userMessages, userInput]);
      setUserInput("");
      // generate responses
      generateSystemResponse(userInput);

      // setUserInput("");
    }
  };

  const generateSystemResponse = (userInput: string) => {
    let conversation = interleaveHistory(userMessages, systemMessages).map((msg) => msg.persona + ': ' + msg.message)
    trackPromise(
      fetch(BASE_URL + "/getKnowledge", {
        method: "POST",
        mode: "cors",
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          q: userInput,
          conversation: conversation,
        })
      }))
    .then(resp => resp.json())
    .then(data => setSystemResponse(data['text']));
  };

  useEffect(() => {
    console.log("RESP", systemResponse)
    if (!systemResponse) return;
    setSystemMessages([...systemMessages, systemResponse]);
  }, [systemResponse])

  interface Message {
    persona: string;
    message: string;
  }
  
  function interleaveHistory(user: string[], system: string[]): Message[] {
    let interleavedArr: Message[] = [];
    for (let i = 0; i < user.length; i++) {
      interleavedArr.push({persona: 'user', message: user[i]});
      interleavedArr.push({persona: 'system', message: system[i]});
    }
    return interleavedArr;
  }

  return (
    <div className="chat-window" ref={chatWindowRef}>
      <div className="chat-content">
        <div className="message-list">

          {interleaveHistory(userMessages, systemMessages).map((message, index) => (
            <div 
              key={index.toString()} 
              className={`message ${message.persona}-message`}>
                {message.message ? message.message : <BouncingDots/>}
            </div>
          ))}
        </div>
        
      </div>
      <div className="input-container">
        <textarea
          className="message-input"
          placeholder="Type your message here..."
          value={userInput}
          onChange={handleUserInput}
          disabled={systemMessages.length < userMessages.length}
        />
        <button className="send-button" onClick={handleSendMessage}>Send</button>
      </div>
    </div>
  );
}

export default ChatWindow;