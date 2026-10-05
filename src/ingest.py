from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine, text

from src.config import settings


ROOT_DIR = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT_DIR / "sql" / "schema.sql"
VIEWS_PATH = ROOT_DIR / "sql" / "views.sql"


def normalize_temperature_data(csv_path: str | Path) -> pd.DataFrame:
    """Normaliza o CSV do Kaggle para o modelo relacional do projeto."""
    df = pd.read_csv(csv_path)
    df.columns = [column.strip().lower() for column in df.columns]

    rename_map = {
        "id": "reading_id",
        "room_id/id": "room_id",
        "room_id": "room_id",
        "noted_date": "noted_at",
        "date": "noted_at",
        "temp": "temperature",
        "temperature": "temperature",
        "out/in": "location",
        "location": "location",
    }
    df = df.rename(columns={key: value for key, value in rename_map.items() if key in df.columns})

    required_columns = {"reading_id", "room_id", "noted_at", "temperature", "location"}
    missing_columns = required_columns.difference(df.columns)
    if missing_columns:
        missing = ", ".join(sorted(missing_columns))
        raise ValueError(f"Colunas obrigatorias ausentes no CSV: {missing}")

    normalized = df.loc[:, ["reading_id", "room_id", "noted_at", "temperature", "location"]].copy()
    normalized["reading_id"] = pd.to_numeric(normalized["reading_id"], errors="coerce")
    normalized["temperature"] = pd.to_numeric(normalized["temperature"], errors="coerce")
    normalized["noted_at"] = pd.to_datetime(
        normalized["noted_at"],
        errors="coerce",
        dayfirst=True,
        format="mixed",
    )
    normalized["location"] = normalized["location"].astype(str).str.strip().str.title()
    normalized["room_id"] = normalized["room_id"].astype(str).str.strip()
    normalized["device_id"] = (
        normalized["room_id"].str.lower().str.replace(r"[^a-z0-9]+", "_", regex=True).str.strip("_")
    )

    normalized = normalized.dropna(subset=["reading_id", "temperature", "noted_at"])
    normalized["reading_id"] = normalized["reading_id"].astype("int64")
    normalized = normalized.drop_duplicates(subset=["reading_id"]).sort_values("noted_at")

    return normalized[
        ["reading_id", "device_id", "room_id", "noted_at", "temperature", "location"]
    ]


def execute_sql_file(engine, path: Path) -> None:
    statements = [statement.strip() for statement in path.read_text(encoding="utf-8").split(";")]
    with engine.begin() as connection:
        for statement in statements:
            if statement:
                connection.execute(text(statement))


def load_data(csv_path: str | Path | None = None) -> int:
    source_path = Path(csv_path or settings.data_file)
    if not source_path.is_absolute():
        source_path = ROOT_DIR / source_path

    if not source_path.exists():
        raise FileNotFoundError(
            f"Arquivo CSV nao encontrado: {source_path}. "
            "Baixe o dataset do Kaggle ou ajuste DATA_FILE no arquivo .env."
        )

    engine = create_engine(settings.database_url)
    data = normalize_temperature_data(source_path)

    execute_sql_file(engine, SCHEMA_PATH)
    with engine.begin() as connection:
        connection.execute(text("TRUNCATE TABLE temperature_readings;"))

    data.to_sql(
        "temperature_readings",
        engine,
        if_exists="append",
        index=False,
        method="multi",
    )
    execute_sql_file(engine, VIEWS_PATH)
    return len(data)


if __name__ == "__main__":
    rows = load_data()
    print(f"{rows} leituras carregadas no PostgreSQL com sucesso.")
