import { motion } from "framer-motion";

const LoadingScreen = () => (
  <motion.div
    className="loading-screen"
    initial={{ opacity: 0, y: 16 }}
    animate={{ opacity: 1, y: 0 }}
    exit={{ opacity: 0, y: -16 }}
    transition={{ duration: 0.3 }}
  >
    <div className="loading-orb">
      <motion.div
        className="loading-ring"
        animate={{ rotate: 360 }}
        transition={{ duration: 1.2, repeat: Infinity, ease: "linear" }}
      />
      <div className="loading-ring-inner" />
    </div>

    <h3>Analyzing your resume…</h3>
    <p>Matching keywords, extracting evidence, scoring structure</p>

    <div className="loading-dots">
      {[0, 1, 2].map((i) => (
        <motion.span
          key={i}
          className="loading-dot"
          animate={{ opacity: [0.3, 1, 0.3], scale: [0.8, 1.2, 0.8] }}
          transition={{ duration: 1.4, repeat: Infinity, delay: i * 0.25 }}
        />
      ))}
    </div>
  </motion.div>
);

export default LoadingScreen;
