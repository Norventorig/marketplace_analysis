from pathlib import Path
import pandas as pd
from unidecode import unidecode

MAIN_DIR = Path(__file__).parent.parent.parent
RAW_DATA_DIR = MAIN_DIR / "data" / "raw"


EXPECTED_FILES = {'olist_customers_dataset.csv',
                  'olist_geolocation_dataset.csv',
                  'olist_orders_dataset.csv',
                  'olist_order_items_dataset.csv',
                  'olist_order_payments_dataset.csv',
                  'olist_order_reviews_dataset.csv',
                  'olist_products_dataset.csv',
                  'olist_sellers_dataset.csv',
                  'product_category_name_translation.csv'}

if not RAW_DATA_DIR.exists():
    raise FileNotFoundError("olist_analysis/data/raw does not exist")

current_files = list(RAW_DATA_DIR.glob("*.csv"))
for file in EXPECTED_FILES:
    if file not in current_files:
        raise FileNotFoundError(f"{file} not found in {RAW_DATA_DIR}")


PROCESSED_DATA_DIR = MAIN_DIR / "data" / "processed"
PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)


def normalize_text(series: pd.Series) -> pd.Series:
    """
    Приводит текст к единому формату.
    """

    return (
        series
        .fillna("")
        .str.strip()
        .str.lower()
        .apply(unidecode)
    )


def save_processed(df: pd.DataFrame, filename: str) -> None:
    """
    Сохраняет обработанный файл.
    """

    df.to_csv(PROCESSED_DATA_DIR / filename, index=False)

    print(f"[OK] {filename}")


def transform_customers() -> pd.DataFrame:
    df = pd.read_csv(RAW_DATA_DIR / "olist_customers_dataset.csv", dtype=str)

    df = df.drop_duplicates(subset=["customer_id"])

    df["customer_city"] = normalize_text(df["customer_city"])

    save_processed(df, "olist_customers_dataset.csv")

    return df


def transform_geolocation() -> pd.DataFrame:
    df = pd.read_csv(RAW_DATA_DIR / "olist_geolocation_dataset.csv",
                     dtype={"geolocation_zip_code_prefix": str})

    df["geolocation_lat"] = pd.to_numeric(df["geolocation_lat"],
                                          errors="coerce")

    df["geolocation_lng"] = pd.to_numeric(df["geolocation_lng"],
                                          errors="coerce")

    df = df.dropna(subset=["geolocation_lat", "geolocation_lng"])

    mask = (df['geolocation_lat'].between(-90, 90) & df['geolocation_lng'].between(-180, 180))
    df = df.loc[mask]

    df["geolocation_city"] = normalize_text(df["geolocation_city"])

    save_processed(df, "olist_geolocation_dataset.csv")

    return df


def transform_orders() -> pd.DataFrame:
    date_columns = [
        "order_purchase_timestamp",
        "order_approved_at",
        "order_delivered_carrier_date",
        "order_delivered_customer_date",
        "order_estimated_delivery_date"
    ]

    null_target_columns = [
        'order_approved_at',
        'order_delivered_carrier_date',
        'order_delivered_customer_date'
    ]

    df = pd.read_csv(RAW_DATA_DIR / "olist_orders_dataset.csv", dtype=str)

    for col in date_columns:
        df[col] = pd.to_datetime(df[col], errors="coerce")

        if col in null_target_columns:
            df[col] = df[col].astype(object).where(df[col].notna(), None)

    df = df.drop_duplicates(subset=["order_id"])

    save_processed(df, "olist_orders_dataset.csv")

    return df


def transform_order_items() -> pd.DataFrame:
    df = pd.read_csv(
        RAW_DATA_DIR / "olist_order_items_dataset.csv",
        dtype='str'
    )

    df["order_item_id"] = df["order_item_id"].astype(int)
    df["price"] = pd.to_numeric(df["price"], errors="coerce")
    df["freight_value"] = pd.to_numeric(df["freight_value"], errors="coerce")

    df['shipping_limit_date'] = pd.to_datetime(df['shipping_limit_date'], errors="coerce")

    df = df.dropna(
        subset=[
            "order_item_id",
            "price",
            "freight_value"]
    )

    df = df[df["order_item_id"] > 0]
    df = df[df["price"] >= 0]
    df = df[df["freight_value"] >= 0]

    save_processed(df, "olist_order_items_dataset.csv")

    return df


def transform_order_payments() -> pd.DataFrame:
    integer_columns = [
        "payment_sequential",
        "payment_installments"
    ]

    df = pd.read_csv(
        RAW_DATA_DIR / "olist_order_payments_dataset.csv",
        dtype=str
    )

    for col in integer_columns:
        df[col] = df[col].astype(int)

    df["payment_value"] = pd.to_numeric(df["payment_value"], errors="coerce")

    df = df[df["payment_value"] >= 0]

    save_processed(df, "olist_order_payments_dataset.csv")

    return df


def transform_reviews() -> pd.DataFrame:
    date_columns = [
        "review_creation_date",
        "review_answer_timestamp"
    ]

    df = pd.read_csv(
        RAW_DATA_DIR / "olist_order_reviews_dataset.csv",
        dtype=str
    )

    df["review_score"] = df["review_score"].astype(int)

    df = df[df["review_score"].between(1, 5)]

    for col in date_columns:
        df[col] = pd.to_datetime(df[col], errors="coerce")

    save_processed(df, "olist_order_reviews_dataset.csv")

    return df


def transform_products() -> pd.DataFrame:

    df = pd.read_csv(
        RAW_DATA_DIR / "olist_products_dataset.csv",
        dtype=str
    )

    integer_columns = [
        "product_name_lenght",
        "product_description_lenght",
        "product_photos_qty",
        "product_weight_g",
        "product_length_cm",
        "product_height_cm",
        "product_width_cm"
    ]

    for col in integer_columns:
        df[col] = df[col].astype('Int64')

    save_processed(
        df,
        "olist_products_dataset.csv"
    )

    return df


def transform_sellers() -> pd.DataFrame:

    df = pd.read_csv(
        RAW_DATA_DIR / "olist_sellers_dataset.csv",
        dtype=str
    )

    df["seller_city"] = normalize_text(
        df["seller_city"]
    )

    save_processed(
        df,
        "olist_sellers_dataset.csv"
    )

    return df


def transform_category_translation() -> pd.DataFrame:

    df = pd.read_csv(
        RAW_DATA_DIR / "product_category_name_translation.csv",
        dtype=str
    )

    df = df.drop_duplicates()

    save_processed(
        df,
        "product_category_name_translation.csv"
    )

    return df


def transform() -> None:
    """
    Обрабатывает все CSV-файлы из data/raw.
    """

    transform_customers()
    transform_geolocation()
    transform_orders()
    transform_order_items()
    transform_order_payments()
    transform_reviews()
    transform_products()
    transform_sellers()
    transform_category_translation()

    print("\nВсе файлы успешно обработаны.")


if __name__ == "__main__":
    transform()
