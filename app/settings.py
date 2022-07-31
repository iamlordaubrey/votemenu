import os

from pydantic import BaseSettings
from sqlalchemy.engine import URL

DIR_PATH = os.path.dirname(os.path.abspath(__file__))


class Settings(BaseSettings):
    port: str
    root_dir: str = DIR_PATH

    log_level: str = 'INFO'

    ci_commit_id: str
    ci_branch: str

    db_host: str
    db_port: str
    db_name: str
    db_password: str
    db_user: str
    db_driver: str = 'postgresql+psycopg2'

    test_db_name: str

    db_dsn: URL

    class Config:
        env_file = DIR_PATH + '/../.env'

    @property
    def db_dsn(self):
        return URL.create(
            drivername=self.db_driver,
            username=self.db_user,
            password=self.db_password,
            host=self.db_host,
            port=self.db_port,
            database=self.db_name,
        )

    @property
    def test_db_dsn(self):
        return URL.create(
            drivername=self.db_driver,
            username=self.db_user,
            password=self.db_password,
            host=self.db_host,
            port=self.db_port,
            database=self.test_db_name,
        )


settings = Settings()
