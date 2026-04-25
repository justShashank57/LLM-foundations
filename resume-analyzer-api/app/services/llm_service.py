import json
from openai import OpenAI
from pydantic import ValidationError

from app.config import settings
from app.prompts import RESUME_ANALYZER_SYSTEM_PROMPT, build_resume_analysis_prompt
from app.schemas import AnalyzeResponse


client = OpenAI(api_key=settings.OPENAI_API_KEY)


ANALYSIS_JSON_SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "resume": {
            "type": "object",
            "additionalProperties": False,
            "properties": {
                "candidate_name": {"type": ["string", "null"]},
                "skills": {"type": "array", "items": {"type": "string"}},
                "experience_years": {"type": ["number", "null"]},
                "projects": {"type": "array", "items": {"type": "string"}},
                "education": {"type": ["string", "null"]},
                "summary": {"type": "string"},
            },
            "required": [
                "candidate_name",
                "skills",
                "experience_years",
                "projects",
                "education",
                "summary",
            ],
        },
        "job_requirements": {
            "type": "object",
            "additionalProperties": False,
            "properties": {
                "required_skills": {"type": "array", "items": {"type": "string"}},
                "optional_skills": {"type": "array", "items": {"type": "string"}},
                "min_experience_years": {"type": ["number", "null"]},
                "role_title": {"type": ["string", "null"]},
                "domain_keywords": {"type": "array", "items": {"type": "string"}},
            },
            "required": [
                "required_skills",
                "optional_skills",
                "min_experience_years",
                "role_title",
                "domain_keywords",
            ],
        },
        "comparison": {
            "type": "object",
            "additionalProperties": False,
            "properties": {
                "matched_required_skills": {
                    "type": "array",
                    "items": {"type": "string"},
                },
                "missing_required_skills": {
                    "type": "array",
                    "items": {"type": "string"},
                },
                "matched_optional_skills": {
                    "type": "array",
                    "items": {"type": "string"},
                },
                "missing_optional_skills": {
                    "type": "array",
                    "items": {"type": "string"},
                },
                "domain_match_notes": {"type": "string"},
                "recommendation": {"type": "string"},
            },
            "required": [
                "matched_required_skills",
                "missing_required_skills",
                "matched_optional_skills",
                "missing_optional_skills",
                "domain_match_notes",
                "recommendation",
            ],
        },
    },
    "required": ["resume", "job_requirements", "comparison"],
}


class LLMService:
    def analyze_resume(self, resume_text: str, job_description: str) -> AnalyzeResponse:
        prompt = build_resume_analysis_prompt(resume_text, job_description)

        last_error = None

        for _ in range(2):
            try:
                response = client.responses.create(
                    model=settings.MODEL,
                    input=[
                        {
                            "role": "system",
                            "content": RESUME_ANALYZER_SYSTEM_PROMPT,
                        },
                        {
                            "role": "user",
                            "content": prompt,
                        },
                    ],
                    text={
                        "format": {
                            "type": "json_schema",
                            "name": "resume_analysis",
                            "schema": ANALYSIS_JSON_SCHEMA,
                            "strict": True,
                        }
                    },
                )

                raw_text = response.output_text
                parsed = json.loads(raw_text)

                # Score is added later by backend, so temporarily add empty score
                parsed["score"] = {
                    "required_skills_score": 0,
                    "optional_skills_score": 0,
                    "experience_score": 0,
                    "domain_score": 0,
                    "final_score": 0,
                }

                return AnalyzeResponse.model_validate(parsed)

            except (json.JSONDecodeError, ValidationError, Exception) as error:
                last_error = error

        raise RuntimeError(f"LLM analysis failed: {str(last_error)}")
