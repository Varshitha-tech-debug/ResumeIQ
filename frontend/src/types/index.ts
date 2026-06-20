// ============================================================
// ResumeIQ – Centralized Type Definitions v3.0
// ============================================================

// ── Evidence & Interview Types (v3 new) ──────────────────────────────────────

/** A single skill with its evidence sentence and signal strength */
export interface SkillEvidence {
  skill: string;
  evidence: string;
  strength: "strong" | "moderate" | "weak";
}

/** Interview questions for a missing skill */
export interface InterviewQuestionSet {
  skill: string;
  questions: string[];
}

// ── Core Response ─────────────────────────────────────────────────────────────

/** Full structured response from /upload-resume or /demo */
export interface AnalysisResult {
  filename: string;
  role: string;
  ats_score: number;
  keyword_score: number;
  project_score: number;
  experience_score: number;
  education_score: number;
  formatting_score: number;
  skills_found: string[];
  missing_skills: string[];
  strengths: string[];
  weaknesses: string[];
  recommendations: string[];
  /** Legacy feedback strings kept for backward compatibility */
  feedback: string[];
  recruiter_summary: string;
  skill_evidence: SkillEvidence[];
  weak_skills: string[];
  interview_readiness: "Beginner" | "Intermediate" | "Ready";
  match_percentage: number;
  recruiter_feedback: string[];
  interview_questions: InterviewQuestionSet[];
}

// ── Chat ──────────────────────────────────────────────────────────────────────

/** A single chat exchange between user and AI */
export interface ChatMessage {
  id: string;
  user: string;
  bot: string;
  timestamp: Date;
}

// ── Component Props ────────────────────────────────────────────────────────────

/** Props for the UploadCard component */
export interface UploadCardProps {
  roles: string[];
  role: string;
  setRole: (role: string) => void;
  file: File | null;
  setFile: (file: File | null) => void;
  loading: boolean;
  handleUpload: () => void;
  onDownloadReport: () => void;
  downloadLoading: boolean;
  /** Demo mode state */
  demoMode: boolean;
  onToggleDemo: () => void;
}

/** Props for the ATSDashboard component */
export interface ATSDashboardProps {
  result: AnalysisResult;
}

/** Props for SkillTags component */
export interface SkillTagsProps {
  skills: string[];
  variant: "matched" | "missing";
}

/** Props for ProgressBar component */
export interface ProgressBarProps {
  label: string;
  score: number;
  weight?: string;
  delay?: number;
}

/** Props for ScoreCircle component */
export interface ScoreCircleProps {
  score: number;
  size?: number;
  strokeWidth?: number;
}

/** Props for ErrorCard component */
export interface ErrorCardProps {
  message?: string;
  onRetry: () => void;
}

/** Props for AIChat component */
export interface AIChatProps {
  role: string;
  result: AnalysisResult | null;
}

/** Props for SkillEvidenceTable component */
export interface SkillEvidenceTableProps {
  evidence: SkillEvidence[];
}

/** Props for RecruiterFeedbackBox component */
export interface RecruiterFeedbackBoxProps {
  feedback: string[];
  role: string;
}

/** Props for InterviewReadinessBadge component */
export interface InterviewReadinessBadgeProps {
  level: "Beginner" | "Intermediate" | "Ready";
  matchPercentage: number;
}

/** Props for InterviewQuestions component */
export interface InterviewQuestionsProps {
  questions: InterviewQuestionSet[];
}

