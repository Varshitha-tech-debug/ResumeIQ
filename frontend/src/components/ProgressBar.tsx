import { motion } from "framer-motion";
import type { ProgressBarProps } from "../types";

const ProgressBar = ({
  label,
  score,
  weight,
  delay = 0,
}: ProgressBarProps) => {
  const color =
    score >= 80 ? "#10B981" : score >= 60 ? "#6366F1" : "#F59E0B";

  return (
    <div className="progress-bar-wrapper">
      <div className="progress-bar-header">
        <span className="progress-label">{label}</span>
        <div className="progress-meta">
          {weight && <span className="progress-weight">{weight}</span>}
          <span className="progress-score" style={{ color }}>
            {score}%
          </span>
        </div>
      </div>
      <div className="progress-track" role="progressbar" aria-valuenow={score} aria-valuemin={0} aria-valuemax={100}>
        <motion.div
          className="progress-fill"
          style={{
            background: `linear-gradient(90deg, ${color}88, ${color})`,
          }}
          initial={{ width: 0 }}
          animate={{ width: `${score}%` }}
          transition={{ duration: 1, delay, ease: "easeOut" }}
        />
      </div>
    </div>
  );
};

export default ProgressBar;
