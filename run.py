import uvicorn
from fastapi import FastAPI
from starlette.requests import Request
import time

app = FastAPI()

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    print(f"Handled request in {process_time} seconds")
    return response

if __name__ == '__main__':
    uvicorn.run("run:app", host="127.0.0.1", port=8001, log_level="info", workers=4)