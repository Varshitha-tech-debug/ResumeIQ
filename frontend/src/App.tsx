import { AnimatePresence, motion } from "framer-motion";
import { useCallback, useEffect, useState } from "react";
import "./App.css";

import {
  analyzeResume,
  downloadReport,
  fetchDemoResult,
  fetchRoles,
  getApiErrorMessage,
} from "./services/api";
import type { AnalysisResult } from "./types";

import AIChat from "./components/AIChat";
import ATSDashboard from "./components/ATSDashboard";
import ErrorCard from "./components/ErrorCard";
import Header from "./components/Header";
import Hero from "./components/Hero";
import LoadingScreen from "./components/LoadingScreen";
import UploadCard from "./components/UploadCard";

function App() {
  const [file, setFile] = useState<File | null>(null);
  const [roles, setRoles] = useState<string[]>(["Software Engineer"]);
  const [role, setRole] = useState("Software Engineer");
  const [loading, setLoading] = useState(false);
  const [downloadLoading, setDownloadLoading] = useState(false);
  const [result, setResult] = useState<AnalysisResult | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [demoMode, setDemoMode] = useState(false);

  useEffect(() => {
    fetchRoles()
      .then((loaded) => {
        setRoles(loaded);
        setRole((current) => (loaded.includes(current) ? current : loaded[0]));
      })
      .catch(() => {
        // Keep defaults if backend is offline during initial load.
      });
  }, []);

  // ── Demo Mode toggle ──────────────────────────────────────────
  const toggleDemoMode = useCallback(() => {
    setDemoMode((prev) => !prev);
    // Clear previous results when switching modes
    setResult(null);
    setError(null);
  }, []);

  // ── Resume Upload / Demo Analyze ──────────────────────────────
  const handleUpload = useCallback(async () => {
    if (!demoMode && !file) return;

    setLoading(true);
    setError(null);
    setResult(null);

    try {
      let data: AnalysisResult;
      if (demoMode) {
        data = await fetchDemoResult();
      } else {
        data = await analyzeResume(file!, role);
      }
      setResult(data);
    } catch (err: unknown) {
      setError(getApiErrorMessage(err, "Unexpected error occurred."));
    } finally {
      setLoading(false);
    }
  }, [file, role, demoMode]);

  // ── PDF Download ──────────────────────────────────────────────
  const handleDownloadReport = useCallback(async () => {
    if (!file) return;
    setDownloadLoading(true);

    try {
      const blob = await downloadReport(file, role);
      const url = URL.createObjectURL(blob);
      const anchor = document.createElement("a");
      anchor.href = url;
      anchor.download = "ResumeIQ_Report.pdf";
      anchor.click();
      URL.revokeObjectURL(url);
    } catch (err: unknown) {
      setError(getApiErrorMessage(err, "PDF report download failed."));
    } finally {
      setDownloadLoading(false);
    }
  }, [file, role]);

  // ── Retry ─────────────────────────────────────────────────────
  const handleRetry = useCallback(() => {
    setError(null);
    handleUpload();
  }, [handleUpload]);

  return (
    <div className="app">
      <Header />

      <main className="main-content" id="main">
        <Hero />

        {/* Two-column workspace */}
        <section className="workspace" aria-label="Resume analysis workspace">
          {/* Left: upload + controls */}
          <UploadCard
            roles={roles}
            role={role}
            setRole={setRole}
            file={file}
            setFile={setFile}
            loading={loading}
            handleUpload={handleUpload}
            onDownloadReport={handleDownloadReport}
            downloadLoading={downloadLoading}
            demoMode={demoMode}
            onToggleDemo={toggleDemoMode}
          />

          {/* Right: dashboard state machine */}
          <div className="workspace-right">
            <AnimatePresence mode="wait">
              {loading && <LoadingScreen key="loading" />}

              {error && !loading && (
                <ErrorCard key="error" message={error} onRetry={handleRetry} />
              )}

              {result && !loading && !error && (
                <ATSDashboard key="dashboard" result={result} />
              )}

              {!loading && !error && !result && (
                <motion.div
                  key="empty"
                  className="workspace-empty"
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  exit={{ opacity: 0 }}
                >
                  <div className="workspace-empty-icon" aria-hidden="true">
                    📊
                  </div>
                  <h3>Your Analysis Dashboard</h3>
                  <p>
                    {demoMode
                      ? 'Click "Run Demo Analysis" to see a full sample output'
                      : "Upload your resume to see your ATS score, skill evidence and interview questions"}
                  </p>
                  {demoMode && (
                    <div className="demo-hint-badge">
                      🎬 Demo Mode Active · No file needed
                    </div>
                  )}
                </motion.div>
              )}
            </AnimatePresence>
          </div>
        </section>

        <AIChat role={role} result={result} />
      </main>
    </div>
  );
}

export default App;
