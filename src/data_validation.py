import pandas as pd
from logger import logging 

def data_check(data:pd.DataFrame):
    try:
        logging.info("starting data validation")
        columns = ['skills', 'title']
        logging.info(f"criteria for columns are {columns}")
        assert (columns == data.columns).all()
        logging.info("data validation process has been done")

    except Exception as e:
        logging.error(f"error was occured on data validation.py file during data check as {e}")
        raise

if __name__ == "__main__":
    data_check(pd.read_csv("data\dataset.csv"))