from fastapi import HTTPException


def bad_request(message: str) -> HTTPException:
    return HTTPException(status_code=400, detail=message)


def internal_error(message: str) -> HTTPException:
    return HTTPException(status_code=500, detail=message)