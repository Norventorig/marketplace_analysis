from pathlib import Path

from kaggle.api.kaggle_api_extended import KaggleApi

RAW_DATA_DIR = Path(__file__).parent.parent.parent / "data" / "raw"

DATASET = "olistbr/brazilian-ecommerce"

EXPECTED_FILES = {'olist_customers_dataset.csv',
                  'olist_geolocation_dataset.csv',
                  'olist_orders_dataset.csv',
                  'olist_order_items_dataset.csv',
                  'olist_order_payments_dataset.csv',
                  'olist_order_reviews_dataset.csv',
                  'olist_products_dataset.csv',
                  'olist_sellers_dataset.csv',
                  'product_category_name_translation.csv'}


def dataset_exists() -> bool:
    """Проверяет, что все файлы датасета уже скачаны."""
    existing_files = {file.name for file in RAW_DATA_DIR.glob("*.csv")}
    return EXPECTED_FILES.issubset(existing_files)


def download_dataset() -> None:
    """
    Скачивает датаЯсет Olist в "data" / "raw".
    Если датасет уже существует — повторное скачивание не выполняется.
    """
    RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)

    if dataset_exists():
        print("Dataset already exists.")
        return

    try:
        api = KaggleApi()
        api.authenticate()

        api.dataset_download_files(
            dataset=DATASET,
            path=RAW_DATA_DIR,
            unzip=True,
        )

    except Exception as e:
        raise RuntimeError(f"Failed to download dataset: {e}") from e

    if not dataset_exists():
        raise RuntimeError("Dataset download finished, but some files are missing.")

    print(f"Dataset downloaded successfully to:\n{RAW_DATA_DIR.resolve()}")


if __name__ == "__main__":
    download_dataset()