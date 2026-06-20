import { motion } from "framer-motion";
import { FiBriefcase } from "react-icons/fi";

const Header = () => (
  <motion.header
    className="navbar"
    initial={{ opacity: 0, y: -20 }}
    animate={{ opacity: 1, y: 0 }}
    transition={{ duration: 0.5 }}
    role="banner"
  >
    <div className="navbar-inner">
      {/* Brand */}
      <div className="navbar-brand">
        <div className="brand-logo" aria-hidden="true">
          <FiBriefcase size={18} />
        </div>
        <span className="brand-name">
          Resume<span className="brand-accent">IQ</span>
        </span>
      </div>

      {/* Status badge */}
      <div className="navbar-badge" aria-label="Evidence-based analysis platform">
        <span className="live-pulse" aria-hidden="true" />
        Evidence-Based
      </div>
    </div>
  </motion.header>
);

export default Header;
