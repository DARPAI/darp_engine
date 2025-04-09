from fastapi import FastAPI

from registry.src.servers.router import router as servers_router

app = FastAPI()

app.include_router(servers_router)
