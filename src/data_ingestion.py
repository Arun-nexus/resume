import os
from src.data_access import Proj1Data
from notebook.configuration_file import load_parameters
from logger import logging
from src.data_access import save_data


def main():
    try:
        logging.info("Data ingestion started")
        params = load_parameters()
        output_path = "data/mongodb_dataset_path.csv"
        project_root = os.getcwd()
        full_path = os.path.join(project_root, output_path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        proj = Proj1Data()
        df = proj.export_collection_as_dataframe("resume_dataset")

        logging.info("Data successfully loaded from MongoDB")
        save_data(full_path,df)

        logging.info(f"Dataset saved successfully at {full_path}")

    except Exception as e:
        logging.error(f"Data ingestion failed: {e}")
        raise


if __name__ == "__main__":
    main()
