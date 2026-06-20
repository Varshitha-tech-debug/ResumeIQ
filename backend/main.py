"""
ResumeIQ – FastAPI Backend v3.1
Production-ready entry point with modular architecture.
"""

import logging
import os
import tempfile
import uuid
from pathlib import Path

from fastapi import BackgroundTasks, FastAPI, File, Form, HTTPException, Request, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.exceptions import RequestValidationError

from resumeiq import __version__
from resumeiq.analyzer import analyze_ats
from resumeiq.coach import answer_coach_question
from resumeiq.constants import MAX_UPLOAD_BYTES, SUPPORTED_ROLES
from resumeiq.demo import DEMO_RESULT
from resumeiq.matcher import validate_role
from resumeiq.models import (
    AICoachRequest,
    AICoachResponse,
    ATSResponse,
    ErrorResponse,
    HealthResponse,
)
from resumeiq.pdf_extractor import extract_text_from_pdf
from resumeiq.pdf_report import generate_pdf

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("resumeiq")

app = FastAPI(
    title="ResumeIQ API",
    description="Deterministic resume intelligence — zero hallucination",
    version=__version__,
)

_cors_raw = os.getenv("CORS_ORIGINS", "*")
_cors_origins = [origin.strip() for origin in _cors_raw.split(",") if origin.strip()]
if not _cors_origins:
    _cors_origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=_cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(HTTPException)
async def http_exception_handler(_request: Request, exc: HTTPException) -> JSONResponse:
    detail = exc.detail if isinstance(exc.detail, str) else str(exc.detail)
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(detail=detail).model_dump(),
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    _request: Request, exc: RequestValidationError
) -> JSONResponse:
    errors = exc.errors()
    first = errors[0] if errors else {}
    loc = " → ".join(str(part) for part in first.get("loc", []))
    msg = first.get("msg", "Invalid request")
    detail = f"Validation error{f' at {loc}' if loc else ''}: {msg}"
    return JSONResponse(
        status_code=422,
        content=ErrorResponse(detail=detail, error_code="validation_error").model_dump(),
    )


@app.exception_handler(Exception)
async def unhandled_exception_handler(_request: Request, exc: Exception) -> JSONResponse:
    logger.exception("Unhandled error: %s", exc)
    return JSONResponse(
        status_code=500,
        content=ErrorResponse(
            detail="An unexpected error occurred. Please try again.",
            error_code="internal_error",
        ).model_dump(),
    )


def _validate_pdf_upload(file: UploadFile) -> str:
    if not file.filename or not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are accepted.")
    return file.filename


async def _read_upload_with_limit(file: UploadFile, dest_path: str) -> None:
    total = 0
    with open(dest_path, "wb") as buf:
        while chunk := await file.read(1024 * 64):
            total += len(chunk)
            if total > MAX_UPLOAD_BYTES:
                raise HTTPException(
                    status_code=400,
                    detail=f"File too large. Maximum size is {MAX_UPLOAD_BYTES // (1024 * 1024)} MB.",
                )
            buf.write(chunk)


def _validate_role_param(role: str) -> str:
    try:
        return validate_role(role)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


def _cleanup_file(path: str) -> None:
    try:
        if path and os.path.exists(path):
            os.remove(path)
    except OSError as exc:
        logger.warning("Failed to remove temp file %s: %s", path, exc)


@app.get("/health", response_model=HealthResponse)
async def health() -> dict:
    return {"status": "ok", "version": __version__}


@app.get("/roles")
async def list_roles() -> dict:
    return {"roles": sorted(SUPPORTED_ROLES)}


@app.get("/demo", response_model=ATSResponse)
async def get_demo() -> dict:
    logger.info("Demo mode requested")
    return DEMO_RESULT


@app.post("/upload-resume", response_model=ATSResponse)
async def upload_resume(
    file: UploadFile = File(...),
    role: str = Form(...),
) -> dict:
    filename = _validate_pdf_upload(file)
    validated_role = _validate_role_param(role)

    suffix = Path(filename).suffix or ".pdf"
    temp_path = os.path.join(tempfile.gettempdir(), f"resumeiq_{uuid.uuid4().hex}{suffix}")
    logger.info("Analyzing resume: %s for role: %s", filename, validated_role)

    try:
        await _read_upload_with_limit(file, temp_path)
        text = extract_text_from_pdf(temp_path)
        return analyze_ats(text, validated_role, filename)
    finally:
        _cleanup_file(temp_path)


@app.post("/download-report")
async def download_report(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    role: str = Form(...),
) -> FileResponse:
    filename = _validate_pdf_upload(file)
    validated_role = _validate_role_param(role)

    suffix = Path(filename).suffix or ".pdf"
    temp_path = os.path.join(tempfile.gettempdir(), f"resumeiq_{uuid.uuid4().hex}{suffix}")
    pdf_path = os.path.join(tempfile.gettempdir(), f"ResumeIQ_Report_{uuid.uuid4().hex}.pdf")
    logger.info("Generating PDF report for: %s role: %s", filename, validated_role)

    try:
        await _read_upload_with_limit(file, temp_path)
        text = extract_text_from_pdf(temp_path)
        data = analyze_ats(text, validated_role, filename)
        generate_pdf(data, pdf_path)
        background_tasks.add_task(_cleanup_file, pdf_path)
        return FileResponse(
            path=pdf_path,
            filename="ResumeIQ_Report.pdf",
            media_type="application/pdf",
        )
    finally:
        _cleanup_file(temp_path)


@app.post("/ai-coach", response_model=AICoachResponse)
async def ai_coach(request: AICoachRequest) -> dict:
    validated_role = request.role.strip()
    if validated_role and validated_role not in SUPPORTED_ROLES:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported role. Supported: {', '.join(sorted(SUPPORTED_ROLES))}",
        )
    answer = answer_coach_question(
        request.question,
        validated_role,
        request.context.model_dump() if request.context else None,
    )
    logger.info("Career coach answered for role: %s", validated_role or "unspecified")
    return {"answer": answer}
