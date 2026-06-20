import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import { AnimatePresence, motion } from "framer-motion";
import { FiMessageSquare, FiSend, FiUser } from "react-icons/fi";
import type { AIChatProps, ChatMessage } from "../types";
import { askAICoach } from "../services/api";

const DEFAULT_SUGGESTIONS = [
  "How does ResumeIQ scoring work?",
  "What skills matter for my target role?",
  "How should I write project bullets?",
];

const CONTEXT_SUGGESTIONS = [
  "What are my biggest skill gaps?",
  "Explain my ATS score",
  "What should I fix first?",
  "What are my recruiter risks?",
];

const AIChat = ({ role, result }: AIChatProps) => {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [input, setInput] = useState("");
  const [isTyping, setIsTyping] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  const suggestions = useMemo(
    () => (result ? CONTEXT_SUGGESTIONS : DEFAULT_SUGGESTIONS),
    [result]
  );

  const scrollToBottom = useCallback(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, []);

  useEffect(() => {
    scrollToBottom();
  }, [messages, isTyping, scrollToBottom]);

  const sendMessage = useCallback(
    async (text?: string) => {
      const userText = (text ?? input).trim();
      if (!userText || isTyping) return;

      setInput("");

      const msgId = `${Date.now()}-${Math.random()}`;
      const newMsg: ChatMessage = {
        id: msgId,
        user: userText,
        bot: "",
        timestamp: new Date(),
      };

      setMessages((prev) => [...prev, newMsg]);
      setIsTyping(true);
      inputRef.current?.focus();

      try {
        const answer = await askAICoach(userText, role, result);
        setMessages((prev) =>
          prev.map((m) => (m.id === msgId ? { ...m, bot: answer } : m))
        );
      } catch {
        setMessages((prev) =>
          prev.map((m) =>
            m.id === msgId
              ? {
                  ...m,
                  bot: "Cannot reach Career Coach. Ensure the backend is running on port 8000.",
                }
              : m
          )
        );
      } finally {
        setIsTyping(false);
      }
    },
    [input, isTyping, role, result]
  );

  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  return (
    <section className="ai-chat" aria-label="Career Coach">
      <div className="ai-chat-header">
        <div className="ai-chat-avatar" aria-hidden="true">
          <FiMessageSquare size={18} />
        </div>
        <div className="ai-chat-title">
          <h2>Career Coach</h2>
          <p>
            {result
              ? "Rule-based guidance using your analysis results"
              : "Rule-based resume and interview guidance — analyze a resume for personalized answers"}
          </p>
        </div>
        <div className="ai-status ai-status--rule-based" aria-label="Rule-based coach">
          <span className="ai-dot" />
          Rule-based
        </div>
      </div>

      <div
        className="ai-chat-messages"
        role="log"
        aria-live="polite"
        aria-label="Chat messages"
      >
        {messages.length === 0 && (
          <div className="chat-empty">
            <FiMessageSquare size={38} aria-hidden="true" />
            <p>
              {result
                ? "Ask about your score, gaps, weak skills, or next steps"
                : "Ask about ATS strategy, skills, or interview prep"}
            </p>
            <div className="chat-suggestions">
              {suggestions.map((s) => (
                <button
                  key={s}
                  className="suggestion-chip"
                  onClick={() => sendMessage(s)}
                  type="button"
                >
                  {s}
                </button>
              ))}
            </div>
          </div>
        )}

        <AnimatePresence initial={false}>
          {messages.map((msg) => (
            <motion.div
              key={msg.id}
              className="chat-exchange"
              initial={{ opacity: 0, y: 18 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0 }}
              transition={{ duration: 0.3 }}
            >
              <div className="chat-bubble chat-bubble--user">
                <div
                  className="bubble-avatar bubble-avatar--user"
                  aria-hidden="true"
                >
                  <FiUser size={13} />
                </div>
                <div className="bubble-content">
                  <p>{msg.user}</p>
                </div>
              </div>

              {msg.bot && (
                <div className="chat-bubble chat-bubble--ai">
                  <div
                    className="bubble-avatar bubble-avatar--ai"
                    aria-hidden="true"
                  >
                    <FiMessageSquare size={13} />
                  </div>
                  <div className="bubble-content">
                    <p>{msg.bot}</p>
                  </div>
                </div>
              )}
            </motion.div>
          ))}
        </AnimatePresence>

        {isTyping && (
          <motion.div
            className="chat-bubble chat-bubble--ai"
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0 }}
            aria-label="Coach is responding"
          >
            <div className="bubble-avatar bubble-avatar--ai" aria-hidden="true">
              <FiMessageSquare size={13} />
            </div>
            <div className="bubble-content typing-indicator">
              <span />
              <span />
              <span />
            </div>
          </motion.div>
        )}

        <div ref={messagesEndRef} />
      </div>

      <div className="ai-chat-input-area">
        <input
          ref={inputRef}
          id="ai-chat-input"
          type="text"
          className="chat-input"
          placeholder={
            result
              ? "Ask about your analysis results…"
              : "Ask about resume strategy or interview prep…"
          }
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          aria-label="Chat message input"
          disabled={isTyping}
        />
        <motion.button
          className="chat-send-btn"
          onClick={() => sendMessage()}
          disabled={!input.trim() || isTyping}
          whileHover={{ scale: 1.06 }}
          whileTap={{ scale: 0.94 }}
          aria-label="Send message"
          type="button"
        >
          <FiSend size={17} />
        </motion.button>
      </div>
    </section>
  );
};

export default AIChat;
