import { motion } from "framer-motion";
import type { SkillTagsProps } from "../types";

const SkillTags = ({ skills, variant }: SkillTagsProps) => {
  if (skills.length === 0) {
    return (
      <p className="no-skills">
        {variant === "matched"
          ? "No skills matched"
          : "✓ All required skills found!"}
      </p>
    );
  }

  return (
    <div className="skill-tags">
      {skills.map((skill, i) => (
        <motion.span
          key={skill}
          className={`skill-tag skill-tag--${variant}`}
          initial={{ opacity: 0, scale: 0.8 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: i * 0.04, duration: 0.25 }}
        >
          {variant === "matched" ? "✓" : "+"} {skill}
        </motion.span>
      ))}
    </div>
  );
};

export default SkillTags;
