import { motion } from "framer-motion";
import {
  FiAlertCircle,
  FiAward,
  FiCheckCircle,
  FiTrendingUp,
  FiUser,
} from "react-icons/fi";
import type { ATSDashboardProps } from "../types";
import InterviewQuestions from "./InterviewQuestions";
import InterviewReadinessBadge from "./InterviewReadinessBadge";
import ProgressBar from "./ProgressBar";
import RecruiterFeedbackBox from "./RecruiterFeedbackBox";
import ScoreCircle from "./ScoreCircle";
import SkillEvidenceTable from "./SkillEvidenceTable";
import SkillTags from "./SkillTags";

const ATSDashboard = ({ result }: ATSDashboardProps) => {
  const {
    ats_score,
    keyword_score,
    project_score,
    experience_score,
    education_score,
    formatting_score,
    skills_found,
    missing_skills,
    strengths,
    weaknesses,
    recommendations,
    role,
    filename,
    skill_evidence,
    weak_skills,
    interview_readiness,
    match_percentage,
    recruiter_feedback,
    interview_questions,
    recruiter_summary,
  } = result;

  const readinessLevel = interview_readiness;
  const matchPct = match_percentage;

  const recruiterLabel =
    ats_score >= 80
      ? "Highly Recommended"
      : ats_score >= 60
      ? "Consider with Revisions"
      : "Needs Improvement";

  const recruiterColor =
    ats_score >= 80 ? "#10B981" : ats_score >= 60 ? "#F59E0B" : "#EF4444";

  return (
    <motion.div
      className="ats-dashboard"
      initial={{ opacity: 0, x: 20 }}
      animate={{ opacity: 1, x: 0 }}
      exit={{ opacity: 0 }}
      transition={{ duration: 0.45, delay: 0.05 }}
      aria-label="ATS Analysis Dashboard"
    >
      {/* ── Header ───────────────────────────────────────────── */}
      <div className="ats-header">
        <h3>ATS Intelligence Dashboard</h3>
        <p>
          Deterministic analysis for <strong>{role}</strong>
        </p>
      </div>

      {/* ── Interview Readiness Badge ─────────────────────────── */}
      <InterviewReadinessBadge
        level={readinessLevel as "Beginner" | "Intermediate" | "Ready"}
        matchPercentage={matchPct}
      />

      {/* ── Score row ─────────────────────────────────────────── */}
      <div className="ats-score-row">
        <ScoreCircle score={ats_score} />
        <div className="ats-score-meta">
          <div
            className="recruiter-badge"
            style={{ color: recruiterColor, borderColor: recruiterColor }}
            aria-label={`Recruiter recommendation: ${recruiterLabel}`}
          >
            <FiUser size={13} />
            {recruiterLabel}
          </div>
          {recruiter_summary && (
            <p className="ats-recruiter-summary">{recruiter_summary}</p>
          )}
          <p className="ats-filename" title={filename}>
            📄 {filename}
          </p>
        </div>
      </div>

      {/* ── Score Breakdown ───────────────────────────────────── */}
      <div className="ats-breakdown">
        <h4>Score Breakdown</h4>
        <ProgressBar label="Keyword Match" score={keyword_score} weight="40%" delay={0.05} />
        <ProgressBar label="Projects"      score={project_score}    weight="20%" delay={0.15} />
        <ProgressBar label="Experience"    score={experience_score} weight="20%" delay={0.25} />
        <ProgressBar label="Education"     score={education_score}  weight="10%" delay={0.35} />
        <ProgressBar label="Formatting"    score={formatting_score} weight="10%" delay={0.45} />
      </div>

      {/* ── Matched / Missing Skills ──────────────────────────── */}
      <div className="ats-skills-grid">
        <div className="ats-skills-col">
          <div className="ats-section-header">
            <FiCheckCircle size={14} />
            <span>Matched Skills</span>
          </div>
          <SkillTags skills={skills_found} variant="matched" />
        </div>
        <div className="ats-skills-col">
          <div className="ats-section-header ats-section-header--warning">
            <FiAlertCircle size={14} />
            <span>Missing Skills</span>
          </div>
          <SkillTags skills={missing_skills} variant="missing" />
        </div>
      </div>

      {/* ── Weak Skills callout ───────────────────────────────── */}
      {weak_skills.length > 0 && (
        <div className="weak-skills-callout">
          <span className="weak-skills-label">⚡ Weak Signals:</span>
          {weak_skills.map((s) => (
            <span key={s} className="weak-skill-chip">{s}</span>
          ))}
          <span className="weak-skills-hint">
            — mentioned briefly, no project context
          </span>
        </div>
      )}

      {/* ── Skill Evidence Table ──────────────────────────────── */}
      {skill_evidence.length > 0 && (
        <SkillEvidenceTable evidence={skill_evidence} />
      )}

      {/* ── Recruiter Honest Feedback ─────────────────────────── */}
      {recruiter_feedback.length > 0 && (
        <RecruiterFeedbackBox feedback={recruiter_feedback} role={role} />
      )}

      {/* ── Strengths / Weaknesses ────────────────────────────── */}
      {(strengths.length > 0 || weaknesses.length > 0) && (
        <div className="ats-insights-grid">
          {strengths.length > 0 && (
            <div className="insights-col">
              <div className="ats-section-header">
                <FiTrendingUp size={14} />
                <span>Strengths</span>
              </div>
              <ul className="insights-list insights-list--strengths">
                {strengths.map((s, i) => <li key={i}>{s}</li>)}
              </ul>
            </div>
          )}
          {weaknesses.length > 0 && (
            <div className="insights-col">
              <div className="ats-section-header ats-section-header--warning">
                <FiAlertCircle size={14} />
                <span>Areas to Improve</span>
              </div>
              <ul className="insights-list insights-list--weaknesses">
                {weaknesses.map((w, i) => <li key={i}>{w}</li>)}
              </ul>
            </div>
          )}
        </div>
      )}

      {/* ── Recommendations ───────────────────────────────────── */}
      {recommendations.length > 0 && (
        <div className="ats-recommendations">
          <div className="ats-section-header ats-section-header--primary">
            <FiAward size={14} />
            <span>Recommendations</span>
          </div>
          <ul className="recommendations-list">
            {recommendations.map((r, i) => (
              <li key={i}>
                <span className="rec-number">{i + 1}</span>
                {r}
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* ── Interview Questions ────────────────────────────────── */}
      {interview_questions.length > 0 && (
        <InterviewQuestions questions={interview_questions} />
      )}
    </motion.div>
  );
};

export default ATSDashboard;
