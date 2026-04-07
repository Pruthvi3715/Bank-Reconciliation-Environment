from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from typing import Optional

from api.main import app as api_app


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


server_app = FastAPI(title="Bank Reconciliation Server", lifespan=lifespan)

server_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

server_app.mount("/api", api_app)


def main():
    import uvicorn

    uvicorn.run(server_app, host="0.0.0.0", port=7860)


if __name__ == "__main__":
    main()
