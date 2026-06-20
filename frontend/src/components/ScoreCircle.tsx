import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import type { ScoreCircleProps } from "../types";

const ScoreCircle = ({
  score,
  size = 150,
  strokeWidth = 10,
}: ScoreCircleProps) => {
  const [displayScore, setDisplayScore] = useState(0);

  const radius = (size - strokeWidth) / 2;
  const circumference = 2 * Math.PI * radius;
  const offset = circumference - (score / 100) * circumference;

  const color =
    score >= 80 ? "#10B981" : score >= 60 ? "#F59E0B" : "#EF4444";

  // Count-up animation
  useEffect(() => {
    let frame = 0;
    const totalFrames = 90;
    const step = score / totalFrames;

    const timer = setInterval(() => {
      frame++;
      if (frame >= totalFrames) {
        setDisplayScore(score);
        clearInterval(timer);
      } else {
        setDisplayScore(Math.round(frame * step));
      }
    }, 16);

    return () => clearInterval(timer);
  }, [score]);

  return (
    <div className="score-circle-wrapper">
      <svg
        width={size}
        height={size}
        viewBox={`0 0 ${size} ${size}`}
        aria-label={`ATS Score: ${score} out of 100`}
      >
        {/* Track ring */}
        <circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          fill="none"
          stroke="rgba(255,255,255,0.06)"
          strokeWidth={strokeWidth}
        />
        {/* Animated progress ring */}
        <g transform={`rotate(-90 ${size / 2} ${size / 2})`}>
          <motion.circle
            cx={size / 2}
            cy={size / 2}
            r={radius}
            fill="none"
            stroke={color}
            strokeWidth={strokeWidth}
            strokeLinecap="round"
            strokeDasharray={circumference}
            initial={{ strokeDashoffset: circumference }}
            animate={{ strokeDashoffset: offset }}
            transition={{ duration: 1.6, ease: "easeOut" }}
          />
        </g>
      </svg>

      {/* Centered label */}
      <div className="score-circle-label">
        <span className="score-value" style={{ color }}>
          {displayScore}
        </span>
        <span className="score-max">/100</span>
        <span className="score-text">ATS Score</span>
      </div>
    </div>
  );
};

export default ScoreCircle;
