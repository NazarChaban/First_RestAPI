from fastapi_limiter import FastAPILimiter
import redis.asyncio as redis
from fastapi import FastAPI
import uvicorn

from src.routes import notes, tags, auth, users
from src.conf.config import settings

app = FastAPI()

app.include_router(tags.router, prefix='/api')
app.include_router(notes.router, prefix='/api')
app.include_router(auth.router, prefix='/api')
app.include_router(users.router, prefix='/api')


@app.on_event("startup")
async def startup():
    r = await redis.Redis(
        host=settings.redis_host, port=settings.redis_port, db=0,
        encoding="utf-8", decode_responses=True
    )
    await FastAPILimiter.init(r)


@app.get("/")
def read_root():
    return {"message": "Hello World"}


if __name__ == "__main__":
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=8000,
        reload=True
    )
