from fastapi import FastAPI
from src.App.routes import router as rter
import uvicorn 

app = FastAPI()
app.include_router(rter)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)