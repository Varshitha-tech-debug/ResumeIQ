import { motion } from "framer-motion";
import type { InterviewReadinessBadgeProps } from "../types";

const LEVEL_CONFIG = {
  Beginner: {
    icon: "🔰",
    color: "#EF4444",
    bg: "rgba(239,68,68,0.07)",
    border: "rgba(239,68,68,0.2)",
    desc: "Resume needs significant improvement before applying to this role",
    tip: "Focus on adding missing keywords and building projects first",
  },
  Intermediate: {
    icon: "⚡",
    color: "#F59E0B",
    bg: "rgba(245,158,11,0.07)",
    border: "rgba(245,158,11,0.2)",
    desc: "Good foundation — key skills are missing, practice interview questions",
    tip: "Review the missing skills and prepare for common interview topics",
  },
  Ready: {
    icon: "✅",
    color: "#10B981",
    bg: "rgba(16,185,129,0.07)",
    border: "rgba(16,185,129,0.2)",
    desc: "Strong keyword match — you are ready to apply and interview",
    tip: "Polish your professional summary and prepare for system design questions",
  },
} as const;

const InterviewReadinessBadge = ({
  level,
  matchPercentage,
}: InterviewReadinessBadgeProps) => {
  const cfg = LEVEL_CONFIG[level] ?? LEVEL_CONFIG["Beginner"];

  return (
    <motion.div
      className="readiness-badge"
      style={{ background: cfg.bg, border: `1px solid ${cfg.border}` }}
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ duration: 0.35 }}
      aria-label={`Interview readiness: ${level}`}
    >
      <span className="readiness-icon" aria-hidden="true">
        {cfg.icon}
      </span>
      <div className="readiness-body">
        <div className="readiness-top">
          <span className="readiness-level" style={{ color: cfg.color }}>
            {level}
          </span>
          <span className="readiness-pct" style={{ color: cfg.color }}>
            {matchPercentage}% match
          </span>
        </div>
        <p className="readiness-desc">{cfg.desc}</p>
        <p className="readiness-tip">{cfg.tip}</p>
      </div>
    </motion.div>
  );
};

export default InterviewReadinessBadge;
