from pathlib import Path
from sqlalchemy import create_engine, text

import os
from dotenv import load_dotenv


load_dotenv()

USERNAME = os.getenv('DB_USERNAME')
PASSWORD = os.getenv('DB_PASSWORD')
HOST = os.getenv('db_host')
PORT = os.getenv('DB_PORT')
DATABASE = os.getenv('DB_NAME')

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SQL_DIR = PROJECT_ROOT / "sql" / "db_init"


def create_database() -> None:
    """
    Создает БД, если она отсутствует.
    """

    engine = create_engine(f'postgresql+psycopg2://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/postgres',
                           isolation_level="AUTOCOMMIT")

    with engine.connect() as conn:
        result = conn.execute(
            text("SELECT 1 "
                 "FROM pg_database "
                 "WHERE datname = :database"),
            {"database": DATABASE}
        )

        if result.scalar():
            print(f"База данных '{DATABASE}' уже существует")
            return

        conn.execute(text(f'CREATE DATABASE "{DATABASE}"'))

        print(f"База данных '{DATABASE}' создана.")


def execute_sql_files() -> None:
    """
    Выполняет все SQL-файлы из каталога sql.
    """

    engine = create_engine(f'postgresql+psycopg2://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}')
    sql_files = sorted(SQL_DIR.glob("*.sql"))

    if not sql_files:
        raise FileNotFoundError(f"SQL файлы не обнаружены в директории: {SQL_DIR}")

    with engine.begin() as conn:
        for sql_file in sql_files:
            print(f"Исполнение файла: {sql_file.name}")

            sql_script = sql_file.read_text(encoding="utf-8")

            conn.execute(text(sql_script))

    print("Все SQL скрипты выполнены успешно.")


def main() -> None:
    create_database()
    execute_sql_files()


if __name__ == "__main__":
    main()