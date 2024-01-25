import uvicorn
from fastapi import FastAPI


app = FastAPI(
    title="Student Management API",
    description="This API is in charge of student management.",
    version="0.1.0",
)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)