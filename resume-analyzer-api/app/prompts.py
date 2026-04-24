RESUME_ANALYZER_SYSTEM_PROMPT = """
You are a strict resume analyis engine.
Rules:
- Return only data matching the specified JSON schema.
- Do not invent skills that are not present or strongly implied.
- Normalize skill names. Example: JS -> JavaScript, React.js -> React.
- Be conservative with experience years.
- If information is unavailable, use null or empty arrays.
- Do not include markdown.
"""

def build_resume_analysis_prompt(resume_text: str, job_description: str) -> str:
    return f"""
Analyze the resume against the job description.
Resume:
{resume_text}

Job Description:
{job_description}

Tasks:
1. Extract structured resume details.
2. Extract structured job requirements.
3. Compare resume with job requirements.
4. Identify matched and missing skills.
5. Give a short recommendation.
"""
