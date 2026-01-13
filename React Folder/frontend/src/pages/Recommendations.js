import React, { useState } from "react";
import ReactMarkdown from "react-markdown";
import { sendChatQuestion } from "../api";
import "./Recommendations.css";

const Recommendations = () => {
  const [question, setQuestion] = useState("");
  const [chat, setChat] = useState([]);
  const [loadingChat, setLoadingChat] = useState(false);

  const normalizeLLMResponse = (response) => {
    if (typeof response === "string") return response;

    if (
      typeof response === "object" &&
      response !== null
    ) {
      // common OpenRouter / LLM shapes
      if (typeof response.content === "string") {
        return response.content;
      }

      if (Array.isArray(response.children)) {
        return response.children.join("");
      }
    }

    return JSON.stringify(response);
  };

  const handleAsk = async () => {
    if (!question.trim()) return;

    const userMessage = { role: "user", content: question };

    setChat((prev) => [...prev, userMessage]);
    setQuestion("");
    setLoadingChat(true);

    try {
      const res = await sendChatQuestion(userMessage.content);

      const safeContent = normalizeLLMResponse(res.recommendation);

      setChat((prev) => [
        ...prev,
        { role: "assistant", content: safeContent }
      ]);
    } catch (err) {
      setChat((prev) => [
        ...prev,
        {
          role: "assistant",
          content:
            "⚠️ Unable to fetch recommendation. Backend may be unavailable."
        }
      ]);
    } finally {
      setLoadingChat(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === "Enter" && !e.shiftKey && !loadingChat) {
      e.preventDefault();
      handleAsk();
    }
  };

  const clearChat = () => setChat([]);

  const suggestedQuestions = [
    {
      icon: "👥",
      text: "How should I optimize staff scheduling based on footfall patterns?",
      category: "Staffing"
    },
    {
      icon: "📊",
      text: "What are the best times for promotional activities?",
      category: "Marketing"
    },
    {
      icon: "💡",
      text: "How can I improve customer engagement during off-peak hours?",
      category: "Strategy"
    },
    {
      icon: "⏰",
      text: "Should I adjust store hours based on current traffic data?",
      category: "Operations"
    }
  ];

  return (
    <div className="recommendations">
      <div className="recommendations-container">

        {/* HEADER */}
        <div className="rec-header">
          <div className="header-content">
            <div className="header-icon-large">🤖</div>
            <h1 className="rec-title">AI Business Assistant</h1>
            <p className="rec-subtitle">
              Intelligent recommendations based on your retail analytics
            </p>
          </div>
        </div>

        {/* CHAT CONTAINER */}
        <div className="chat-container">

          {/* CHAT MESSAGES */}
          <div className="chat-messages">

            {chat.length === 0 && (
              <div className="welcome-screen">
                <div className="welcome-icon">💬</div>
                <h2 className="welcome-title">How can I help you today?</h2>
                <p className="welcome-text">
                  Ask anything about staffing, marketing, operations, or growth.
                </p>

                <div className="suggestions">
                  <h3 className="suggestions-title">Suggested Questions</h3>
                  <div className="suggestions-grid">
                    {suggestedQuestions.map((s, i) => (
                      <button
                        key={i}
                        className="suggestion-card"
                        onClick={() => setQuestion(s.text)}
                      >
                        <div className="suggestion-header">
                          <span className="suggestion-icon">{s.icon}</span>
                          <span className="suggestion-category">
                            {s.category}
                          </span>
                        </div>
                        <p className="suggestion-text">{s.text}</p>
                      </button>
                    ))}
                  </div>
                </div>
              </div>
            )}

            {chat.map((msg, idx) => (
              <div key={idx} className={`message message-${msg.role}`}>
                <div className="message-avatar">
                  {msg.role === "user" ? "👤" : "🤖"}
                </div>

                <div className="message-content">
                  <div className="message-header">
                    <span className="message-sender">
                      {msg.role === "user" ? "You" : "AI Assistant"}
                    </span>
                    <span className="message-time">
                      {new Date().toLocaleTimeString([], {
                        hour: "2-digit",
                        minute: "2-digit"
                      })}
                    </span>
                  </div>

                  <div className="message-text">
                    {msg.role === "assistant" ? (
                      <ReactMarkdown>
                        {typeof msg.content === "string"
                          ? msg.content
                          : ""}
                      </ReactMarkdown>
                    ) : (
                      msg.content
                    )}
                  </div>
                </div>
              </div>
            ))}

            {loadingChat && (
              <div className="message message-assistant">
                <div className="message-avatar">🤖</div>
                <div className="message-content">
                  <div className="typing-indicator">
                    <span className="typing-dot"></span>
                    <span className="typing-dot"></span>
                    <span className="typing-dot"></span>
                  </div>
                </div>
              </div>
            )}
          </div>

          {/* INPUT */}
          <div className="chat-input-area">

            {chat.length > 0 && (
              <button className="clear-chat-btn" onClick={clearChat}>
                🗑️ Clear Chat
              </button>
            )}

            <div className="input-container">
              <textarea
                value={question}
                onChange={(e) => setQuestion(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder="Ask a business question…"
                className="chat-textarea"
                rows="1"
                disabled={loadingChat}
              />
              <button
                onClick={handleAsk}
                disabled={loadingChat || !question.trim()}
                className="send-btn"
              >
                {loadingChat ? "⏳" : "🚀"}
              </button>
            </div>

            <div className="input-footer">
              💡 Tip: Be specific for better recommendations
            </div>

          </div>
        </div>
      </div>
    </div>
  );
};

export default Recommendations;
