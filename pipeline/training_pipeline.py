if "__name__" == "__main__":
    from config.paths_config import *
    from src.data_ingestion import DataIngestion
    from src.data_processing import DataProcessing
        ### Data Ingestion
    data_ingestion = DataIngestion(config=read_yaml(CONFIG_PATH))
    data_ingestion.run()
    ### Data Processing
    data_processing = DataProcessing(data_path=INPUT_DIR)
    data_processing.run()
    ### Model Training  
    from src.model_training import ModelTraining
    model_trainer = ModelTraining(data_path=INPUT_DIR)
    model_trainer.train()