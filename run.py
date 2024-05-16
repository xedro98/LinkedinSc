from api.routes import app
import uvicorn

if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8001, log_level="info", workers=4)