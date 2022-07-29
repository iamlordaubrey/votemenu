from fastapi import FastAPI
from uvicorn import Server, Config

from app.settings import settings

app = FastAPI()


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
