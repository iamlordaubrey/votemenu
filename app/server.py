from fastapi import FastAPI
from uvicorn import Server, Config

from app.api import health_check, home_page
from app.api.api_v1.api import api_router
from app.database import Base, engine
from app.settings import settings

Base.metadata.create_all(bind=engine)

app = FastAPI(title='Menu Votes', openapi_url='/openapi.json')

app.include_router(home_page.router)

app.include_router(health_check.router, tags=['health check'])
app.include_router(api_router, prefix=settings.API_V1_STR)


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
