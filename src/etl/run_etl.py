from extract import download_dataset
from load import load_data


if __name__ == "__main__":
    print('ETL has been started...')

    download_dataset()
    load_data()

    print('ETL has been finished.')
