from fastapi import FastAPI

app = FastAPI(title="Claude Playground")


@app.get("/")
def read_root():
    return {"message": "Hello from Claude Playground!"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/version")
def version():
    return {"version": "0.1.0"}
