import uvicorn
from fastapi import FastAPI, status, HTTPException
from fastapi.responses import JSONResponse

from controllers.templates import template_router

app = FastAPI(
    title="Student Management API",
    description="This API is in charge of student management.",
    version="0.1.0",
)

app.include_router(template_router)


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    return JSONResponse(
        status_code=status.HTTP_424_FAILED_DEPENDENCY, content={"message": exc.args}
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail},
    )


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
