import uvicorn
from api.routes import app

if __name__ == '__main__':
    uvicorn.run("api.routes:app", host="127.0.0.1", port=8001, log_level="info", workers=4)