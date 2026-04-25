import json

from fastapi import APIRouter, HTTPException, Request
from pydantic import ValidationError

from app.schemas import AnalyzeRequest, AnalyzeResponse
from app.services.llm_service import LLMService
from app.services.post_processing_service import post_process_analysis
from app.services.scoring_service import calculate_match_score
from app.services.text_cleaner import clean_text, limit_text
from app.utils.errors import bad_request, internal_error


router = APIRouter(prefix="/api", tags=["Resume Analyzer"])

llm_service = LLMService()


@router.post("/analyze", response_model=AnalyzeResponse)
async def analyze_resume(request: Request):
    try:
        payload = await _parse_analyze_request(request)

        resume_text = limit_text(clean_text(payload.resume_text))
        job_description = limit_text(clean_text(payload.job_description))

        if len(resume_text) < 50:
            raise bad_request("Resume text is too short.")

        if len(job_description) < 50:
            raise bad_request("Job description is too short.")

        analysis = llm_service.analyze_resume(
            resume_text=resume_text,
            job_description=job_description,
        )
        analysis = post_process_analysis(
            analysis=analysis,
            resume_text=resume_text,
            job_description=job_description,
        )

        score = calculate_match_score(
            resume=analysis.resume,
            job=analysis.job_requirements,
            comparison=analysis.comparison,
        )

        analysis.score = score

        return analysis

    except HTTPException:
        raise
    except Exception as error:
        raise internal_error(str(error))


async def _parse_analyze_request(request: Request) -> AnalyzeRequest:
    try:
        raw_body = await request.body()
        data = json.loads(raw_body.decode("utf-8"), strict=False)
        return AnalyzeRequest.model_validate(data)
    except json.JSONDecodeError as error:
        raise bad_request(f"Invalid JSON body: {error.msg}.")
    except UnicodeDecodeError:
        raise bad_request("Request body must be valid UTF-8 JSON.")
    except ValidationError as error:
        raise HTTPException(status_code=422, detail=error.errors())
