import { BASE_URL } from '@/config/constants';
import React, { useState, useEffect, useRef } from 'react';
import { trackPromise } from 'react-promise-tracker';
import ReactMarkdown from 'react-markdown';
import BouncingDots from './BouncingDots';
import ErrorPopup from './ErrorPopup';
// import CodeBlock from './CodeBlock';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { vscDarkPlus } from 'react-syntax-highlighter/dist/cjs/styles/prism';
import MarkdownMessage from './MarkdownMessage';

export interface Message {
  persona: string;
  message: string;
}

const ChatWindow = () => {
  const [userMessages, setUserMessages] = useState<string[]>([]);
  const [systemMessages, setSystemMessages] = useState<string[]>([]);
  const [userInput, setUserInput] = useState<string>('');
  const [systemResponse, setSystemResponse] = useState<string>('');
  const [backendError, setBackendError] = useState<boolean>(false);
  const [conversationSummary, setConversationSummary] = useState<string>('');
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
      setUserInput('');
      // generate responses
      generateSystemResponse(userInput);
    }
  };

  const generateSystemResponse = (userInput: string) => {
    let conversation = interleaveHistory(userMessages, systemMessages).map((msg) => msg.message);

    const streamRequest = async (conversation: string[], userInput: string) => {
      const response = await fetch(BASE_URL + '/getKnowledge', {
        method: 'POST',
        mode: 'cors',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          conversation: conversation,
          q: userInput,
        }),
      });

      if (!response.ok) {
        handleErrorOccured();
        throw new Error('Request failed');
      }
      if (response.body == null) return;
      const reader = response.body.getReader();
      let receivedText = '';

      while (true) {
        const { done, value } = await reader.read();

        if (done) {
          break;
        }

        const textChunk = new TextDecoder('utf-8').decode(value);
        receivedText += textChunk;
        setSystemResponse(receivedText);
      }
    };

    trackPromise(streamRequest(conversation, userInput)).catch((error) => {
      console.error('Error:', error);
    });

    // fetch(BASE_URL + '/summarise', {
    //   method: 'POST',
    //   mode: 'cors',
    //   headers: {
    //     'Content-Type': 'application/json',
    //   },
    //   body: JSON.stringify({
    //     conversation: conversation,
    //   }),
    // })
    //   .then((resp) => {
    //     if (resp.status === 500) {
    //       handleErrorOccured();
    //     }
    //     return resp.json();
    //   })
    //   .then((data) => setConversationSummary(data['text']))
    //   .catch((error) => {
    //     console.error('Error:', error);
    //     // Handle other types of errors here if needed
    //   });
  };

  const handleErrorOccured = () => {
    setBackendError(true);
  };

  const handleErrorIgnore = () => {
    setBackendError(false);
  };
  const handleErrorReset = () => {
    setBackendError(false);
    reset();
  };
  useEffect(() => {
    if (!systemResponse) return;
    if (systemMessages.length < userMessages.length) {
      setSystemMessages([...systemMessages, systemResponse]);
    } else {
      const newSystemMessages = [...systemMessages];
      newSystemMessages[newSystemMessages.length - 1] = systemResponse;
      setSystemMessages(newSystemMessages);
    }
  }, [systemResponse]);

  function interleaveHistory(user: string[], system: string[]): Message[] {
    let interleavedArr: Message[] = [];
    for (let i = 0; i < user.length; i++) {
      interleavedArr.push({ persona: 'user', message: user[i] });
      interleavedArr.push({ persona: 'system', message: system[i] });
    }
    return interleavedArr;
  }

  function reset() {
    setUserMessages([]);
    setSystemMessages([]);
    setUserInput('');
    setSystemResponse('');
  }

  return (
    <div className="chat-window" ref={chatWindowRef}>
      <div className="chat-content">
        <div className="message-list">
          {userMessages.length ? (
            <button className="reset-button message system-message" onClick={reset}>
              Reset Conversation
            </button>
          ) : (
            ''
          )}
          {interleaveHistory(userMessages, systemMessages).map((message, index) => (
            <div key={index.toString()} className={`message ${message.persona}-message`}>
              {message.message != null ? <MarkdownMessage message={message} /> : <BouncingDots />}
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
          onKeyDown={(event) => {
            if (event.keyCode === 13 && !event.shiftKey) {
              // 13 is the keyCode for the enter key
              event.preventDefault(); // Prevent the default behavior of the enter key
              handleSendMessage();
            }
          }}
        />
        <button className="send-button" onClick={handleSendMessage}>
          Send
        </button>
      </div>
      <ErrorPopup error={backendError} onIgnore={handleErrorIgnore} onReset={handleErrorReset} />
    </div>
  );
};

export default ChatWindow;
