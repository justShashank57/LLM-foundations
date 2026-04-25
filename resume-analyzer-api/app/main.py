from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from app.routes.analyze import router as analyze_router


app = FastAPI(
    title="Resume Analyzer API",
    version="1.0.0",
    description="LLM-powered resume analyzer with structured output and backend scoring.",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def health_check():
    return {"status": "ok", "message": "Resume Analyzer API is running"}


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    for error in exc.errors():
        if error.get("type") == "json_invalid":
            return JSONResponse(
                status_code=400,
                content={
                    "detail": (
                        "Invalid JSON body. If resume_text or job_description contains "
                        "multiple lines, send the request through a JSON serializer or "
                        "escape line breaks as \\n inside the string."
                    )
                },
            )

    return JSONResponse(status_code=422, content={"detail": exc.errors()})


app.include_router(analyze_router)
