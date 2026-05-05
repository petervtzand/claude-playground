
from fastapi import FastAPI
from fastapi.responses import FileResponse, HTMLResponse

__version__ = "0.1.0"

app = FastAPI(
    title="Claude Playground",
    description="A FastAPI sandbox for hands-on learning of Claude Code features.",
    version=__version__,
)


@app.get("/")
async def read_root() -> dict[str, str]:
    return {"message": "Hello from Claude Playground!"}


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/version")
async def version() -> dict[str, str]:
    return {"version": __version__}


@app.get("/echo/{message}")
async def echo(message: str) -> dict[str, str]:
    return {"echo": message}


@app.get("/favicon.ico", include_in_schema=False)
async def favicon() -> FileResponse:
    return FileResponse("static/favicon.svg", media_type="image/svg+xml")


@app.get("/landing", response_class=HTMLResponse)
async def landing() -> str:
    return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Claude Playground</title>
    <link rel="icon" type="image/svg+xml" href="/favicon.ico">
    <style>
        *, *::before, *::after { box-sizing: border-box; }
        html, body { margin: 0; padding: 0; }
        body {
            min-height: 100vh;
            background: #0a0a0a;
            color: #e8e8e8;
            font-family: system-ui, -apple-system, sans-serif;
            font-size: 1.0625rem;
            line-height: 1.7;
            -webkit-font-smoothing: antialiased;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 2rem;
        }
        main {
            max-width: 36rem;
            width: 100%;
        }
        h1 {
            font-size: clamp(2.25rem, 5vw, 3.75rem);
            font-weight: 600;
            letter-spacing: -0.025em;
            line-height: 1.1;
            margin: 0 0 1.5rem;
            color: #fafafa;
        }
        p {
            color: #a3a3a3;
            margin: 0 0 2.5rem;
        }
        ul {
            list-style: none;
            padding: 0;
            margin: 0;
            display: flex;
            flex-direction: column;
            gap: 0.75rem;
        }
        a {
            color: #38bdf8;
            text-decoration: none;
            border-bottom: 1px solid transparent;
            transition: color 0.15s ease, border-color 0.15s ease;
            display: inline-block;
        }
        a:hover {
            color: #7dd3fc;
            border-bottom-color: #7dd3fc;
        }
    </style>
</head>
<body>
    <main>
        <h1>Welcome to Claude Playground</h1>
        <p>A FastAPI sandbox for exploring Claude Code features.</p>
        <ul>
            <li><a href="/docs">Interactive API docs</a></li>
            <li><a href="/health">Health check</a></li>
            <li><a href="/version">Version</a></li>
        </ul>
    </main>
</body>
</html>"""
