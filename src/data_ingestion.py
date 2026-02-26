import os
from pdb import run
import sys
import pandas as pd
from google.cloud import storage
from src.logger import get_logger
from src.custom_exception import CustomException
from config.paths_config import *
from utils.common_functions import read_yaml

logger = get_logger(__name__)

class DataIngestion:

    def __init__(self,config):
        self.config = config["data_ingestion"]
        self.bucket_name = self.config["bucket_name"]
        self.bucket_file_names = self.config["bucket_file_names"]
        os.makedirs(RAW_DIR,exist_ok=True)


    def download_data_from_gcs(self):
        
        try:
            storage_client = storage.Client()
            bucket = storage_client.bucket(self.bucket_name)
            for file_name in self.bucket_file_names:
                blob = bucket.blob(file_name)
                destination_file_name = os.path.join(RAW_DIR, file_name)
                blob.download_to_filename(destination_file_name)
                if file_name == "animelist.csv":
                    data = pd.read_csv(destination_file_name,nrows=5000000)
                    data.to_csv(destination_file_name,index=False)
                    logger.info("Large fiel downloaded and truncated to 5 million rows for faster processing.")
                logger.info(f"Downloaded {file_name} from bucket {self.bucket_name} to {destination_file_name}")
        except Exception as e:
            logger.error(f"Error downloading data from GCS: {e}")
            raise CustomException(CustomException.get_error_message(str(e), sys), sys)
        
    def run(self):
        try:
            logger.info("Starting data ingestion process.")
            self.download_data_from_gcs()
            logger.info("Data ingestion completed successfully.")
        except Exception as e:
            logger.error(f"Error in data ingestion run: {e}")
            raise CustomException(CustomException.get_error_message(str(e), sys), sys)

if __name__ == "__main__":
    DataIngestion = DataIngestion(config=read_yaml(CONFIG_PATH))
    DataIngestion.run()
    