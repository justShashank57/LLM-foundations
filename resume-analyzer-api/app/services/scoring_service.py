from app.schemas import (
    ResumeExtract,
    JobRequirementExtract,
    LLMComparison,
    ScoreBreakdown,
)


def calculate_match_score(
    resume: ResumeExtract,
    job: JobRequirementExtract,
    comparison: LLMComparison,
) -> ScoreBreakdown:
    required_score = _skill_score(
        matched=comparison.matched_required_skills,
        total=job.required_skills,
        weight=60,
    )

    optional_score = _skill_score(
        matched=comparison.matched_optional_skills,
        total=job.optional_skills,
        weight=20,
    )

    experience_score = _experience_score(
        resume_years=resume.experience_years,
        required_years=job.min_experience_years,
        weight=10,
    )

    domain_score = _domain_score(
        domain_keywords=job.domain_keywords,
        resume_text_items=resume.projects + resume.skills,
        weight=10,
    )

    final_score = required_score + optional_score + experience_score + domain_score

    return ScoreBreakdown(
        required_skills_score=round(required_score, 2),
        optional_skills_score=round(optional_score, 2),
        experience_score=round(experience_score, 2),
        domain_score=round(domain_score, 2),
        final_score=round(min(final_score, 100), 2),
    )


def _skill_score(matched: list[str], total: list[str], weight: float) -> float:
    if not total:
        return weight

    return (len(set(_normalize_list(matched))) / len(set(_normalize_list(total)))) * weight


def _experience_score(
    resume_years: float | None,
    required_years: float | None,
    weight: float,
) -> float:
    if required_years is None:
        return weight

    if resume_years is None:
        return 0

    if resume_years >= required_years:
        return weight

    return (resume_years / required_years) * weight


def _domain_score(
    domain_keywords: list[str],
    resume_text_items: list[str],
    weight: float,
) -> float:
    if not domain_keywords:
        return weight

    resume_blob = " ".join(resume_text_items).lower()
    matched = 0

    for keyword in domain_keywords:
        if keyword.lower() in resume_blob:
            matched += 1

    return (matched / len(domain_keywords)) * weight


def _normalize_list(items: list[str]) -> list[str]:
    return [item.strip().lower() for item in items if item.strip()]