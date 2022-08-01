from fastapi import FastAPI
from uvicorn import Server, Config

from app.api import health_check, home_page
from app.api.api_v1.api import api_router as api_router_v1
from app.api.api_v2.api import api_router as api_router_v2
from app.database import Base, engine
from app.settings import settings

Base.metadata.create_all(bind=engine)

app = FastAPI(title='Menu Votes', openapi_url='/openapi.json')

app.include_router(home_page.router, tags=['Home page'])
app.include_router(health_check.router, tags=['Health check'])

app.include_router(api_router_v1, prefix=settings.api_v1_str)
app.include_router(api_router_v2, prefix=settings.api_v2_str)


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
