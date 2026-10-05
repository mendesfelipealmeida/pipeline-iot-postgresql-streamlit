from dataclasses import dataclass
import os

from dotenv import load_dotenv


load_dotenv()


@dataclass(frozen=True)
class Settings:
    postgres_user: str = os.getenv("POSTGRES_USER", "iot_user")
    postgres_password: str = os.getenv("POSTGRES_PASSWORD", "iot_password")
    postgres_db: str = os.getenv("POSTGRES_DB", "iot_db")
    postgres_host: str = os.getenv("POSTGRES_HOST", "localhost")
    postgres_port: str = os.getenv("POSTGRES_PORT", "5432")
    data_file: str = os.getenv("DATA_FILE", "data/sample_temperature_readings.csv")

    @property
    def database_url(self) -> str:
        return (
            "postgresql+psycopg2://"
            f"{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )


settings = Settings()
