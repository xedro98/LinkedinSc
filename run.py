import uvicorn
from fastapi import FastAPI
from api.routes import router

app = FastAPI()
app.include_router(router)

if __name__ == '__main__':
    uvicorn.run("run:app", host="127.0.0.1", port=8001, log_level="info", workers=4, reload=True)