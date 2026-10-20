from enum import Enum
from pydantic import BaseModel, Field


class Severity(str, Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class ReviewFinding(BaseModel):
    file_path: str
    line_number: int
    severity: Severity
    category: str
    description: str
    suggested_fix: str
    confidence: float = Field(ge=0, le=1)


class PRReviewResult(BaseModel):
    pull_request_number: int
    summary: str
    findings: list[ReviewFinding]
