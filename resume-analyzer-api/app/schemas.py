from typing import List, Optional
from pydantic import BaseModel, Field


class AnalyzeRequest(BaseModel):
    resume_text: str = Field(..., min_length=50)
    job_description: str = Field(..., min_length=50)


class ResumeExtract(BaseModel):
    candidate_name: Optional[str]
    skills: List[str]
    experience_years: Optional[float]
    projects: List[str]
    education: Optional[str]
    summary: str


class JobRequirementExtract(BaseModel):
    required_skills: List[str]
    optional_skills: List[str]
    min_experience_years: Optional[float]
    role_title: Optional[str]
    domain_keywords: List[str]


class LLMComparison(BaseModel):
    matched_required_skills: List[str]
    missing_required_skills: List[str]
    matched_optional_skills: List[str]
    missing_optional_skills: List[str]
    domain_match_notes: str
    recommendation: str


class ScoreBreakdown(BaseModel):
    required_skills_score: float
    optional_skills_score: float
    experience_score: float
    domain_score: float
    final_score: float


class AnalyzeResponse(BaseModel):
    resume: ResumeExtract
    job_requirements: JobRequirementExtract
    comparison: LLMComparison
    score: ScoreBreakdown