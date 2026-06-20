// ============================================================
// ResumeIQ – Centralized API Service v3.0
// ============================================================
import axios from "axios";
import type { AnalysisResult } from "../types";

const BASE_URL =
  (import.meta as ImportMeta & { env: Record<string, string> }).env
    .VITE_API_URL ?? "https://resumeiq-api-varsha.onrender.com";

const client = axios.create({ baseURL: BASE_URL });

/** Extract a user-facing message from axios/FastAPI errors. */
export function getApiErrorMessage(err: unknown, fallback: string): string {
  if (axios.isAxiosError(err)) {
    const detail = err.response?.data?.detail;
    if (typeof detail === "string" && detail.trim()) {
      return detail;
    }
    if (err.message === "Network Error") {
      return "Cannot reach the ResumeIQ server. Ensure the backend is running on port 8000.";
    }
    return err.message || fallback;
  }
  if (err instanceof Error) {
    return err.message;
  }
  return fallback;
}

/**
 * Upload a resume PDF and receive a full ATS analysis.
 */
export async function analyzeResume(
  file: File,
  role: string
): Promise<AnalysisResult> {
  const formData = new FormData();
  formData.append("file", file);
  formData.append("role", role);

  const res = await client.post<AnalysisResult>("/upload-resume", formData, {
    headers: { "Content-Type": "multipart/form-data" },
  });
  return res.data;
}

/** Fetch supported target roles from the backend. */
export async function fetchRoles(): Promise<string[]> {
  const res = await client.get<{ roles: string[] }>("/roles");
  return res.data.roles;
}

/**
 * Fetch the hardcoded demo result (safe for live presentations).
 * No file upload required. Always returns the same structured output.
 */
export async function fetchDemoResult(): Promise<AnalysisResult> {
  const res = await client.get<AnalysisResult>("/demo");
  return res.data;
}

/**
 * Download an executive PDF report for the uploaded resume.
 */
export async function downloadReport(file: File, role: string): Promise<Blob> {
  const formData = new FormData();
  formData.append("file", file);
  formData.append("role", role);

  const res = await client.post("/download-report", formData, {
    headers: { "Content-Type": "multipart/form-data" },
    responseType: "blob",
  });
  return res.data as Blob;
}

/**
 * Ask the Career Coach a question. Pass analysis result for context-aware answers.
 */
export async function askAICoach(
  question: string,
  role: string,
  result?: AnalysisResult | null
): Promise<string> {
  const payload: {
    question: string;
    role: string;
    context?: {
      role: string;
      ats_score: number;
      match_percentage: number;
      interview_readiness: string;
      skills_found: string[];
      missing_skills: string[];
      weak_skills: string[];
      recruiter_feedback: string[];
      recommendations: string[];
    };
  } = { question, role };

  if (result) {
    payload.context = {
      role: result.role,
      ats_score: result.ats_score,
      match_percentage: result.match_percentage,
      interview_readiness: result.interview_readiness,
      skills_found: result.skills_found,
      missing_skills: result.missing_skills,
      weak_skills: result.weak_skills,
      recruiter_feedback: result.recruiter_feedback,
      recommendations: result.recommendations,
    };
  }

  const res = await client.post<{ answer: string }>("/ai-coach", payload);
  return res.data.answer;
}
