import { motion } from "framer-motion";
import { FiSearch } from "react-icons/fi";
import type { SkillEvidenceTableProps } from "../types";

const STRENGTH_CONFIG = {
  strong:   { label: "Strong",   className: "ev-strong",   icon: "✓" },
  moderate: { label: "Moderate", className: "ev-moderate", icon: "~" },
  weak:     { label: "Weak",     className: "ev-weak",     icon: "!" },
} as const;

const SkillEvidenceTable = ({ evidence }: SkillEvidenceTableProps) => {
  if (!evidence || evidence.length === 0) return null;

  return (
    <div className="evidence-wrapper">
      <div className="ats-section-header ats-section-header--primary">
        <FiSearch size={13} />
        <span>Skill Evidence — Extracted from Resume</span>
        <span className="evidence-note">No hallucination · Text quoted directly</span>
      </div>

      <div className="evidence-table">
        {/* Table header */}
        <div className="evidence-head">
          <span>Skill</span>
          <span>Evidence Found in Resume</span>
          <span>Signal</span>
        </div>

        {/* Rows */}
        {evidence.map((item, i) => {
          const cfg = STRENGTH_CONFIG[item.strength as keyof typeof STRENGTH_CONFIG]
            ?? STRENGTH_CONFIG.moderate;

          return (
            <motion.div
              key={item.skill}
              className="evidence-row"
              initial={{ opacity: 0, x: -8 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: i * 0.06, duration: 0.25 }}
            >
              <span className="ev-skill">{item.skill}</span>
              <span className="ev-text">"{item.evidence}"</span>
              <span className={`ev-strength ${cfg.className}`}>
                {cfg.icon} {cfg.label}
              </span>
            </motion.div>
          );
        })}
      </div>
    </div>
  );
};

export default SkillEvidenceTable;
