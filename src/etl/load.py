from pathlib import Path
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy import text
from sqlalchemy.engine import URL
from sqlalchemy.exc import OperationalError

from src.etl.transform import transform_customers
from src.etl.transform import transform_geolocation
from src.etl.transform import transform_orders
from src.etl.transform import transform_order_items
from src.etl.transform import transform_order_payments
from src.etl.transform import transform_reviews
from src.etl.transform import transform_products
from src.etl.transform import transform_sellers
from src.etl.transform import transform_category_translation

import os
from dotenv import load_dotenv

load_dotenv()

USERNAME = os.getenv("DB_USERNAME")
PASSWORD = os.getenv("DB_PASSWORD")
HOST = os.getenv("DB_HOST")
PORT = os.getenv("DB_PORT")
DATABASE = os.getenv("DB_NAME")

url = URL.create(
    drivername="postgresql+psycopg2",
    username=USERNAME,
    password=PASSWORD,
    host=HOST,
    port=PORT,
    database=DATABASE,
)

ENGINE = create_engine(url=url)

DATASETS_PATH = Path(__file__).parent.parent.parent / "data" / "processed"

TABLE_CONFIG = {
    'olist_customers_dataset.csv': {
        'table_name': 'customers',
        'primary_key': ['customer_id'],
        'transform_function': transform_customers
    },
    'olist_sellers_dataset.csv': {
        'table_name': 'sellers',
        'primary_key': ['seller_id'],
        'transform_function': transform_sellers
    },
    'olist_products_dataset.csv': {
        'table_name': 'products',
        'primary_key': ['product_id'],
        'transform_function': transform_products
    },
    'product_category_name_translation.csv': {
        'table_name': 'product_category_name_translation',
        'primary_key': ['product_category_name'],
        'transform_function': transform_category_translation
    },
    'olist_geolocation_dataset.csv': {
        'table_name': 'geolocation',
        'primary_key': ['geolocation_id'],
        'transform_function': transform_geolocation
    },
    'olist_orders_dataset.csv': {
        'table_name': 'orders',
        'primary_key': ['order_id'],
        'transform_function': transform_orders
    },
    'olist_order_items_dataset.csv': {
        'table_name': 'order_items',
        'primary_key': ['order_id', 'order_item_id'],
        'transform_function': transform_order_items
    },
    'olist_order_payments_dataset.csv': {
        'table_name': 'order_payments',
        'primary_key': ['order_id', 'payment_sequential'],
        'transform_function': transform_order_payments
    },
    'olist_order_reviews_dataset.csv': {
        'table_name': 'order_reviews',
        'primary_key': ['review_id', 'order_id'],
        'transform_function': transform_reviews
    }
}


def check_connection() -> None:
    """
    Проверяет доступность базы данных.
    """

    try:
        with ENGINE.connect() as connection:
            connection.execute(text("SELECT 1"))

    except OperationalError as e:
        raise RuntimeError(
            f"Не удалось подключиться к базе данных '{DATABASE}'.\n\n"
            "Возможные причины:\n"
            "1) база данных не существует;\n"
            "2) PostgreSQL не запущен;\n"
            "3) неверные параметры подключения в .env."
        ) from e


def load_table(df: pd.DataFrame, table_name: str, primary_keys: list | None) -> None:
    """ Выполняет UPSERT данных в PostgreSQL. """

    columns = df.columns.to_list()

    if primary_keys is None:
        raise ValueError( f"Для таблицы '{table_name}' " f"не определен PRIMARY KEY." )

    update_sql = ", ".join(
        [f"{column}=EXCLUDED.{column}" for column in columns if column not in primary_keys]
    )

    columns_sql = ", ".join(columns)
    placeholders = ", ".join(
        [f":{column}" for column in columns]
    )

    conflict_columns = ", ".join(primary_keys)

    query = text(
        f"""
        INSERT INTO {table_name}
        ({columns_sql})
        
        VALUES
        ({placeholders})
        
        ON CONFLICT ({conflict_columns})
        DO UPDATE SET
        {update_sql}
        """
    )

    records = df.to_dict(orient="records")

    with ENGINE.begin() as connection:
        for start in range(0, len(records), 1000):
            batch = records[start:start + 1000]
            connection.execute(query, batch)


def process_file(filename: str) -> None:
    """
    Выполняет загрузку одного файла.
    """

    print(f"\nЗагрузка {filename}...")

    table_name = TABLE_CONFIG[filename]["table_name"]
    primary_keys = TABLE_CONFIG[filename]["primary_key"]
    df = TABLE_CONFIG[filename]["transform_function"]()

    load_table(df=df, table_name=table_name, primary_keys=primary_keys)

    print(
        f"Успешно загружено "
        f"{len(df)} строк в таблицу '{table_name}'."
    )


def load_data() -> None:
    """
    Загружает все обработанные датасеты в БД.
    """
    check_connection()

    for filename in TABLE_CONFIG:
        process_file(filename=filename)

    print("\nВсе данные успешно загружены.")


if __name__ == "__main__":
    load_data()
