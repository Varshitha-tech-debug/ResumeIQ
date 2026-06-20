import { useRef, useState } from "react";
import { motion } from "framer-motion";
import { FiUploadCloud, FiFileText, FiDownload, FiX } from "react-icons/fi";
import type { UploadCardProps } from "../types";

const UploadCard = ({
  roles,
  role,
  setRole,
  file,
  setFile,
  loading,
  handleUpload,
  onDownloadReport,
  downloadLoading,
  demoMode,
  onToggleDemo,
}: UploadCardProps) => {
  const [dragging, setDragging] = useState(false);
  const inputRef = useRef<HTMLInputElement>(null);

  const handleDrop = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setDragging(false);
    const dropped = e.dataTransfer.files[0];
    if (dropped?.type === "application/pdf") setFile(dropped);
  };

  const removeFile = (e: React.MouseEvent) => {
    e.stopPropagation();
    setFile(null);
    if (inputRef.current) inputRef.current.value = "";
  };

  const canAnalyze = demoMode || !!file;

  return (
    <motion.div
      className="upload-card"
      initial={{ opacity: 0, x: -20 }}
      animate={{ opacity: 1, x: 0 }}
      transition={{ duration: 0.5, delay: 0.1 }}
    >
      {/* Header */}
      <div className="upload-card-header">
        <h3>Resume Analyzer</h3>
        <p>Upload PDF · Select role · Analyze</p>
      </div>

      {/* Demo Mode Toggle */}
      <div className="demo-toggle-inline">
        <div className="demo-toggle-label">
          <span className="demo-toggle-icon">{demoMode ? "🎬" : "📄"}</span>
          <div>
            <strong>Demo Mode</strong>
            <p>{demoMode ? "Sample resume active · Presentation safe" : "Real resume analysis"}</p>
          </div>
        </div>
        <button
          className={`demo-switch${demoMode ? " demo-switch--on" : ""}`}
          onClick={onToggleDemo}
          type="button"
          aria-pressed={demoMode}
          aria-label={`Demo mode is ${demoMode ? "on" : "off"}`}
        >
          <motion.span
            className="demo-switch-thumb"
            animate={{ x: demoMode ? 18 : 2 }}
            transition={{ duration: 0.2 }}
          />
        </button>
      </div>

      {/* Role Selector */}
      <div className="form-group">
        <label className="form-label" htmlFor="role-select">
          Target Role
        </label>
        <select
          id="role-select"
          className="form-select"
          value={role}
          onChange={(e) => setRole(e.target.value)}
        >
          {roles.map((r) => (
            <option key={r} value={r}>{r}</option>
          ))}
        </select>
      </div>

      {/* Drop Zone — hidden when demo mode active */}
      {!demoMode && (
        <div
          className={`drop-zone${dragging ? " drop-zone--active" : ""}${
            file ? " drop-zone--filled" : ""
          }`}
          onDragOver={(e) => { e.preventDefault(); setDragging(true); }}
          onDragLeave={() => setDragging(false)}
          onDrop={handleDrop}
          onClick={() => inputRef.current?.click()}
          role="button"
          tabIndex={0}
          aria-label="Upload resume PDF. Click or drag and drop."
          onKeyDown={(e) => e.key === "Enter" && inputRef.current?.click()}
        >
          <input
            ref={inputRef}
            type="file"
            accept=".pdf"
            hidden
            aria-hidden="true"
            onChange={(e) => setFile(e.target.files?.[0] ?? null)}
          />

          {file ? (
            <div className="drop-zone-file">
              <FiFileText size={26} />
              <div className="drop-zone-file-info">
                <p className="file-name" title={file.name}>{file.name}</p>
                <p className="file-size">{(file.size / 1024).toFixed(1)} KB · PDF</p>
              </div>
              <button
                className="file-remove"
                onClick={removeFile}
                aria-label="Remove file"
                type="button"
              >
                <FiX size={15} />
              </button>
            </div>
          ) : (
            <div className="drop-zone-empty">
              <FiUploadCloud size={34} aria-hidden="true" />
              <p>
                Drop your PDF here or <span>browse</span>
              </p>
              <span className="drop-hint">Max 10 MB · PDF only</span>
            </div>
          )}
        </div>
      )}

      {/* Demo active notice */}
      {demoMode && (
        <div className="demo-active-notice">
          <span>🎬</span>
          <div>
            <strong>Sample Resume Loaded</strong>
            <p>Alex Chen · Software Engineer · Demo fixture</p>
          </div>
        </div>
      )}

      {/* Actions */}
      <div className="upload-actions">
        <motion.button
          className="btn-primary"
          onClick={handleUpload}
          disabled={loading || !canAnalyze}
          whileHover={!loading && canAnalyze ? { scale: 1.02 } : {}}
          whileTap={!loading && canAnalyze ? { scale: 0.98 } : {}}
          type="button"
          aria-busy={loading}
        >
          {loading ? (
            <>
              <span className="btn-spinner" aria-hidden="true" />
              Analyzing…
            </>
          ) : (
            <>
              <FiUploadCloud size={15} aria-hidden="true" />
              {demoMode ? "Run Demo Analysis" : "Analyze Resume"}
            </>
          )}
        </motion.button>

        {file && !demoMode && (
          <motion.button
            className="btn-secondary"
            onClick={onDownloadReport}
            disabled={downloadLoading || !file}
            whileHover={!downloadLoading ? { scale: 1.02 } : {}}
            whileTap={!downloadLoading ? { scale: 0.98 } : {}}
            type="button"
            aria-busy={downloadLoading}
            initial={{ opacity: 0, y: 6 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.25 }}
          >
            {downloadLoading ? (
              <>
                <span className="btn-spinner" aria-hidden="true" />
                Generating…
              </>
            ) : (
              <>
                <FiDownload size={15} aria-hidden="true" />
                Download PDF Report
              </>
            )}
          </motion.button>
        )}
      </div>
    </motion.div>
  );
};

export default UploadCard;
