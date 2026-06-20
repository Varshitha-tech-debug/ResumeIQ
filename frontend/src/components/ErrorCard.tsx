import { motion } from "framer-motion";
import { FiAlertCircle, FiRefreshCw } from "react-icons/fi";
import type { ErrorCardProps } from "../types";

const ErrorCard = ({ message, onRetry }: ErrorCardProps) => (
  <motion.div
    className="error-card"
    initial={{ opacity: 0, scale: 0.95 }}
    animate={{ opacity: 1, scale: 1 }}
    exit={{ opacity: 0, scale: 0.95 }}
    transition={{ duration: 0.3 }}
    role="alert"
  >
    <div className="error-icon">
      <FiAlertCircle size={36} />
    </div>

    <h3>Unable to Analyze Resume</h3>

    <p>{message?.trim() || "Something went wrong. Please try again."}</p>

    <ul className="error-checklist">
      <li>Backend server is running on port 8000</li>
      <li>Uploaded file is a valid, text-based PDF</li>
      <li>Network connection is available</li>
    </ul>

    <motion.button
      className="retry-btn"
      onClick={onRetry}
      whileHover={{ scale: 1.04 }}
      whileTap={{ scale: 0.96 }}
    >
      <FiRefreshCw size={15} />
      Try Again
    </motion.button>
  </motion.div>
);

export default ErrorCard;
