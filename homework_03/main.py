from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get("/")
def index():
    return {"message": "hello"}

@app.get("/ping/")
def view():
    return {"message": "pong"}

if __name__ == '__main__':
    uvicorn.run("main:app", reload=True)