import { motion, type Variants } from "framer-motion";
import { FiZap, FiTarget, FiMessageSquare, FiShield, FiTrendingUp } from "react-icons/fi";

const STATS = [
  {
    icon: FiZap,
    value: "100%",
    label: "Deterministic",
    color: "#10B981",
    bg: "rgba(16,185,129,0.12)",
  },
  {
    icon: FiTarget,
    value: "50+",
    label: "Role Keywords",
    color: "#6366F1",
    bg: "rgba(99,102,241,0.12)",
  },
  {
    icon: FiMessageSquare,
    value: "0",
    label: "Hallucinations",
    color: "#8B5CF6",
    bg: "rgba(139,92,246,0.12)",
  },
];

const BADGES = [
  { icon: FiZap, text: "Evidence-Based Analysis" },
  { icon: FiShield, text: "ATS Optimized" },
  { icon: FiTrendingUp, text: "Recruiter Ready" },
];

// Framer Motion v12: ease must be Easing type, not a plain string in variants.
// Move transition to the motion component's transition prop instead.
const containerVariants: Variants = {
  hidden: {},
  visible: { transition: { staggerChildren: 0.12 } },
};

const itemVariants: Variants = {
  hidden:   { opacity: 0, y: 28 },
  visible:  { opacity: 1, y: 0 },
};

const Hero = () => (
  <section className="hero" aria-label="ResumeIQ hero section">
    <motion.div
      className="hero-inner"
      initial="hidden"
      animate="visible"
      variants={containerVariants}
    >
      {/* Eyebrow badge */}
      <motion.div
        className="hero-eyebrow"
        variants={itemVariants}
        transition={{ duration: 0.55 }}
      >
        <span className="hero-live-dot" />
        Resume Intelligence Platform
      </motion.div>

      {/* Brand title */}
      <motion.h1
        className="hero-title"
        variants={itemVariants}
        transition={{ duration: 0.55 }}
      >
        Resume<span className="hero-title-accent">IQ</span>
      </motion.h1>

      {/* Sub-heading */}
      <motion.h2
        className="hero-heading"
        variants={itemVariants}
        transition={{ duration: 0.55 }}
      >
        Land More Interviews with
        <br />
        <span className="hero-heading-gradient">Evidence-Based Resume Analysis</span>
      </motion.h2>

      {/* Subtitle */}
      <motion.p
        className="hero-subtitle"
        variants={itemVariants}
        transition={{ duration: 0.55 }}
      >
        Professional ATS scoring, recruiter insights, keyword matching
        with quoted evidence — deterministic and explainable.
      </motion.p>

      {/* Feature badges */}
      <motion.div
        className="hero-badges"
        variants={itemVariants}
        transition={{ duration: 0.55 }}
      >
        {BADGES.map(({ icon: Icon, text }) => (
          <div key={text} className="hero-badge">
            <Icon size={14} />
            {text}
          </div>
        ))}
      </motion.div>

      {/* Stats cards */}
      <motion.div className="hero-stats" variants={containerVariants}>
        {STATS.map(({ icon: Icon, value, label, color, bg }) => (
          <motion.div
            key={label}
            className="hero-stat-card"
            variants={itemVariants}
            transition={{ duration: 0.5 }}
            whileHover={{ y: -6, transition: { duration: 0.2 } }}
          >
            <div className="hero-stat-icon" style={{ color, background: bg }}>
              <Icon size={18} />
            </div>
            <div className="hero-stat-value" style={{ color }}>{value}</div>
            <div className="hero-stat-label">{label}</div>
          </motion.div>
        ))}
      </motion.div>
    </motion.div>
  </section>
);

export default Hero;
