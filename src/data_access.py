import sys
import pandas as pd
import numpy as np
from typing import Optional
import os
from mongodb.mongodb_connection import mongodbclient
from logger import logging


class Proj1Data:

    def __init__(self) -> None:
        try:
            self.mongo_client = mongodbclient()
            self.default_db = "resume"

            if self.default_db is None:
                raise ValueError("database_name not set in environment")

        except Exception as e:
            logging.error(f"Error initializing Proj1Data: {e}")
            raise

    def export_collection_as_dataframe(
        self,
        collection_name: str,
        database_name: Optional[str] = None
    ) -> pd.DataFrame:

        try:
            db_name = database_name if database_name else self.default_db

            collection = self.mongo_client.client[db_name][collection_name]

            logging.info("Fetching data from MongoDB")

            df = pd.DataFrame(list(collection.find()))

            logging.info(f"Data fetched with length: {len(df)}")

            if "_id" in df.columns:
                df.drop(columns=["_id"], inplace=True)

            df.replace({"na": np.nan}, inplace=True)

            return df

        except Exception as e:
            logging.error(f"Error exporting collection: {e}")
            raise




