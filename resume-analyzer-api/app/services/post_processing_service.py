import re
from datetime import date

from app.schemas import AnalyzeResponse


MONTHS = {
    "jan": 1,
    "january": 1,
    "feb": 2,
    "february": 2,
    "mar": 3,
    "march": 3,
    "apr": 4,
    "april": 4,
    "may": 5,
    "jun": 6,
    "june": 6,
    "jul": 7,
    "july": 7,
    "aug": 8,
    "august": 8,
    "sep": 9,
    "sept": 9,
    "september": 9,
    "oct": 10,
    "october": 10,
    "nov": 11,
    "november": 11,
    "dec": 12,
    "december": 12,
}


DATE_RANGE_RE = re.compile(
    r"\b("
    r"jan(?:uary)?|feb(?:ruary)?|mar(?:ch)?|apr(?:il)?|may|jun(?:e)?|"
    r"jul(?:y)?|aug(?:ust)?|sep(?:t(?:ember)?|tember)?|oct(?:ober)?|"
    r"nov(?:ember)?|dec(?:ember)?"
    r")\s+(\d{4})\s*(?:-|to|–|—|\?)\s*("
    r"present|current|"
    r"jan(?:uary)?|feb(?:ruary)?|mar(?:ch)?|apr(?:il)?|may|jun(?:e)?|"
    r"jul(?:y)?|aug(?:ust)?|sep(?:t(?:ember)?|tember)?|oct(?:ober)?|"
    r"nov(?:ember)?|dec(?:ember)?"
    r")(?:\s+(\d{4}))?\b",
    re.IGNORECASE,
)


SKILL_ALIASES = {
    "API design": ["api design", "api-based", "apis", "rest api", "rest apis"],
    "ASP.NET": ["asp dotnet", "asp.net", "dotnet", ".net"],
    "C#": ["c#"],
    "C++": ["c++"],
    "Data modeling": ["data model", "data models", "data modeling"],
    "Django": ["django"],
    "Docker": ["docker"],
    "Express.js": ["express", "expressjs", "express.js"],
    "FastAPI": ["fastapi"],
    "Gin": ["gin"],
    "GraphQL": ["graphql"],
    "JavaScript": ["javascript", "js"],
    "Microsoft Azure": ["microsoft azure", "azure"],
    "MongoDB": ["mongodb", "mongo db"],
    "MySQL": ["mysql"],
    "Node.js": ["node", "nodejs", "node.js"],
    "PHP": ["php"],
    "PostgreSQL": ["postgresql", "postgres"],
    "Python": ["python", "python-based"],
    "Rails": ["rails", "ruby on rails"],
    "React": ["react", "reactjs", "react.js"],
    "React Native": ["react native", "expo"],
    "Redux": ["redux"],
    "REST APIs": ["rest api", "rest apis"],
    "Tailwind CSS": ["tailwind", "tailwind css"],
    "TypeScript": ["typescript", "ts"],
    "Vue": ["vue", "vue.js", "vuejs"],
}


FRONTEND_SKILLS = {"React", "Vue", "JavaScript", "TypeScript", "Redux", "Tailwind CSS"}
BACKEND_SKILLS = {
    "ASP.NET",
    "Django",
    "Express.js",
    "FastAPI",
    "Gin",
    "Node.js",
    "PHP",
    "Python",
    "Rails",
}
DATABASE_SKILLS = {"MongoDB", "MySQL", "PostgreSQL"}


def post_process_analysis(
    analysis: AnalyzeResponse,
    resume_text: str,
    job_description: str,
    as_of: date | None = None,
) -> AnalyzeResponse:
    resume_skills = _extract_skills(resume_text)
    job_skills = _extract_skills(job_description)

    analysis.resume.skills = _merge_unique(analysis.resume.skills, resume_skills)

    experience_years = calculate_experience_years(resume_text, as_of=as_of)
    if experience_years is not None:
        analysis.resume.experience_years = experience_years

    analysis.job_requirements.required_skills = _merge_unique(
        analysis.job_requirements.required_skills,
        job_skills,
    )

    _refresh_required_skill_matches(analysis, resume_text)

    return analysis


def calculate_experience_years(text: str, as_of: date | None = None) -> float | None:
    as_of = as_of or date.today()
    ranges = []

    for match in DATE_RANGE_RE.finditer(text):
        start_month = MONTHS[match.group(1).lower()]
        start_year = int(match.group(2))
        end_token = match.group(3).lower()
        end_year_token = match.group(4)

        if end_token in {"present", "current"}:
            end_month = as_of.month
            end_year = as_of.year
        else:
            if not end_year_token:
                continue
            end_month = MONTHS[end_token]
            end_year = int(end_year_token)

        start_index = start_year * 12 + start_month
        end_index = end_year * 12 + end_month

        if end_index >= start_index:
            ranges.append((start_index, end_index))

    if not ranges:
        return None

    merged_ranges = _merge_month_ranges(ranges)
    total_months = sum(end - start + 1 for start, end in merged_ranges)

    return round(total_months / 12, 2)


def _refresh_required_skill_matches(analysis: AnalyzeResponse, resume_text: str) -> None:
    matched = []
    missing = []

    for skill in analysis.job_requirements.required_skills:
        if _requirement_matches_resume(skill, analysis.resume.skills, resume_text):
            matched.append(skill)
        else:
            missing.append(skill)

    analysis.comparison.matched_required_skills = matched
    analysis.comparison.missing_required_skills = missing


def _requirement_matches_resume(
    requirement: str,
    resume_skills: list[str],
    resume_text: str,
) -> bool:
    normalized_requirement = _normalize(requirement)
    canonical_resume_skills = {_canonical_skill(skill) for skill in resume_skills}
    resume_blob = resume_text.lower()

    if "frontendframework" in normalized_requirement:
        return bool(canonical_resume_skills & FRONTEND_SKILLS)

    if "backendlanguage" in normalized_requirement or "backendframework" in normalized_requirement:
        return bool(canonical_resume_skills & BACKEND_SKILLS)

    if normalized_requirement == _normalize("API design"):
        return "api" in resume_blob or "REST APIs" in canonical_resume_skills

    if normalized_requirement == _normalize("Data modeling"):
        return (
            bool(canonical_resume_skills & DATABASE_SKILLS)
            or "dbms" in resume_blob
            or "database" in resume_blob
            or "data model" in resume_blob
        )

    canonical_requirement = _canonical_skill(requirement)
    return canonical_requirement in canonical_resume_skills


def _extract_skills(text: str) -> list[str]:
    found = []

    for skill, aliases in SKILL_ALIASES.items():
        if any(_contains_term(text, alias) for alias in aliases):
            found.append(skill)

    return found


def _contains_term(text: str, term: str) -> bool:
    escaped = re.escape(term)
    return re.search(rf"(?<![A-Za-z0-9+#.]){escaped}(?![A-Za-z0-9+#.])", text, re.IGNORECASE) is not None


def _canonical_skill(skill: str) -> str:
    normalized_skill = _normalize(skill)

    for canonical, aliases in SKILL_ALIASES.items():
        if normalized_skill == _normalize(canonical):
            return canonical

        for alias in aliases:
            if normalized_skill == _normalize(alias):
                return canonical

    return skill.strip()


def _merge_unique(primary: list[str], additions: list[str]) -> list[str]:
    merged = []
    seen = set()

    for item in primary + additions:
        canonical = _canonical_skill(item)
        key = _normalize(canonical)

        if key and key not in seen:
            merged.append(canonical)
            seen.add(key)

    return merged


def _merge_month_ranges(ranges: list[tuple[int, int]]) -> list[tuple[int, int]]:
    ranges = sorted(ranges)
    merged = [ranges[0]]

    for start, end in ranges[1:]:
        last_start, last_end = merged[-1]

        if start <= last_end + 1:
            merged[-1] = (last_start, max(last_end, end))
        else:
            merged.append((start, end))

    return merged


def _normalize(value: str) -> str:
    return re.sub(r"[^a-z0-9+#]+", "", value.lower())
