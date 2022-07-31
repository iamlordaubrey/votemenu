from fastapi import FastAPI
from uvicorn import Server, Config

from app.database import Base, engine
from app.routers import main, health_check
from app.settings import settings

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(main.router)
app.include_router(health_check.router)


if __name__ == '__main__':
    server = Server(
        Config(
            'server:app',
            host='0.0.0.0',
            port=int(settings.port),
            log_level=settings.log_level.lower(),
        )
    )
    server.run()
