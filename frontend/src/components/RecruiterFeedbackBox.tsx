import { motion } from "framer-motion";
import { FiUserX } from "react-icons/fi";
import type { RecruiterFeedbackBoxProps } from "../types";

const RecruiterFeedbackBox = ({ feedback, role }: RecruiterFeedbackBoxProps) => {
  if (!feedback || feedback.length === 0) return null;

  return (
    <div className="rfb-wrapper" role="region" aria-label="Recruiter honest assessment">
      {/* Header */}
      <div className="rfb-header">
        <FiUserX size={15} />
        <span>Recruiter View · Honest Assessment</span>
        <span className="rfb-role-tag">{role}</span>
      </div>

      <p className="rfb-disclaimer">
        These are observable signals from your resume that may cause screening rejection.
        Based on detected text only.
      </p>

      {/* Rejection risk items */}
      <ul className="rfb-list">
        {feedback.map((item, i) => (
          <motion.li
            key={i}
            className="rfb-item"
            initial={{ opacity: 0, x: -10 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: i * 0.08, duration: 0.25 }}
          >
            <span className="rfb-bullet" aria-hidden="true">⚠</span>
            <span>{item}</span>
          </motion.li>
        ))}
      </ul>
    </div>
  );
};

export default RecruiterFeedbackBox;
