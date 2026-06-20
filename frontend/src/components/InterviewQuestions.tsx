import { useState } from "react";
import { AnimatePresence, motion } from "framer-motion";
import { FiChevronDown, FiChevronUp } from "react-icons/fi";
import type { InterviewQuestionsProps } from "../types";

const InterviewQuestions = ({ questions }: InterviewQuestionsProps) => {
  const [openSkill, setOpenSkill] = useState<string | null>(null);

  if (!questions || questions.length === 0) return null;

  const toggle = (skill: string) => {
    setOpenSkill((prev) => (prev === skill ? null : skill));
  };

  return (
    <div className="iq-wrapper" role="region" aria-label="Interview questions for missing skills">
      <div className="iq-header">
        <span>🎯</span>
        <span>Interview Questions for Missing Skills</span>
      </div>
      <p className="iq-subtitle">
        Practice these before your interview · Derived from your skill gaps
      </p>

      <div className="iq-list">
        {questions.map((item) => {
          const isOpen = openSkill === item.skill;

          return (
            <div key={item.skill} className="iq-item">
              <button
                className={`iq-skill-btn${isOpen ? " iq-skill-btn--open" : ""}`}
                onClick={() => toggle(item.skill)}
                aria-expanded={isOpen}
                type="button"
              >
                <span className="iq-skill-name">{item.skill}</span>
                <span className="iq-count">{item.questions.length} questions</span>
                {isOpen ? <FiChevronUp size={14} /> : <FiChevronDown size={14} />}
              </button>

              <AnimatePresence initial={false}>
                {isOpen && (
                  <motion.ul
                    className="iq-questions"
                    initial={{ height: 0, opacity: 0 }}
                    animate={{ height: "auto", opacity: 1 }}
                    exit={{ height: 0, opacity: 0 }}
                    transition={{ duration: 0.25 }}
                  >
                    {item.questions.map((q, i) => (
                      <li key={i} className="iq-question">
                        <span className="iq-num" aria-label={`Question ${i + 1}`}>
                          Q{i + 1}
                        </span>
                        <span>{q}</span>
                      </li>
                    ))}
                  </motion.ul>
                )}
              </AnimatePresence>
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default InterviewQuestions;
