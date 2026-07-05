from pathlib import Path

from kaggle.api.kaggle_api_extended import KaggleApi


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


def dataset_exists(directory: Path) -> bool:
    """Проверяет, что все файлы датасета уже скачаны."""
    existing_files = {file.name for file in directory.glob("*.csv")}
    return EXPECTED_FILES.issubset(existing_files)


def download_dataset(download_dir: Path) -> None:
    """
    Скачивает датаЯсет Olist в указанную директорию.
    Если датасет уже существует — повторное скачивание не выполняется.
    """
    download_dir.mkdir(parents=True, exist_ok=True)

    if dataset_exists(download_dir):
        print("Dataset already exists.")
        return

    try:
        api = KaggleApi()
        api.authenticate()

        api.dataset_download_files(
            dataset=DATASET,
            path=download_dir,
            unzip=True,
        )

    except Exception as e:
        raise RuntimeError(f"Failed to download dataset: {e}") from e

    if not dataset_exists(download_dir):
        raise RuntimeError("Dataset download finished, but some files are missing.")

    print(f"Dataset downloaded successfully to:\n{download_dir.resolve()}")


if __name__ == "__main__":
    project_root = Path(__file__).resolve().parent.parent
    raw_data_dir = project_root / "data" / "raw"

    download_dataset(raw_data_dir)