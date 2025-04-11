import os 
import sys 
from pandas import DataFrame
from sklearn.model_selection import train_test_split
from src.entity.config_entity import DataIngestionConfig
from src.entity.artifact_entity import DataIngestionArtifact
from src.logger import logging
from src.exception import MyException
from src.data_access.proj1_data import Proj1Data


class DataIngestion:
  def __init__(self,data_ingestion_config: DataIngestionConfig=DataIngestionConfig()):
    """Params: data_ingestion_config : configurations for data ingestion"""
    try:
      self.data_ingestion_config = data_ingestion_config
    except Exception as e:
      raise MyException(e,sys)
    
  def export_data_into_feature_store(self)->DataFrame:
    logging.info("Exporting data into Feature store started in Data Ingesting phase")
    my_data = Proj1Data()
    dataframe = my_data.export_collection_as_dataframe(self.data_ingestion_config.collection_name)
    print(f"Shape of DataFrame {dataframe.shape}")
    feature_store_file_path = self.data_ingestion_config.feature_store_file_path
    dir_path = os.path.dirname(self.data_ingestion_config.feature_store_file_path)
    os.makedirs(dir_path,exist_ok=True)
    logging.info(f"Saving exported data in {feature_store_file_path}")
    dataframe.to_csv(feature_store_file_path,index=False,header=True)
    logging.info("Exporting Phase Data Ingesting Ends")
    
    return dataframe
  
  def split_data_as_train_test(self,dataframe: DataFrame)->None:
    """Spliting of DataFrame"""
    
    logging.info("Entered Dataframe Spliting Phase in Data Ingestion")
    train_set,test_set = train_test_split(dataframe,test_size=self.data_ingestion_config.train_test_split_ratio)
    
    logging.info("Performed spliting of data in data ingestion")
    dir_name = os.path.dirname(self.data_ingestion_config.training_file_path)
    os.makedirs(dir_name,exist_ok=True)
    logging.info("exporting train and test file path")
    train_set.to_csv(self.data_ingestion_config.training_file_path,index=False,header=True)
    test_set.to_csv(self.data_ingestion_config.testing_file_path,index=False,header=True)
    logging.info("exported train and test file path")
    
  def initiate_data_ingestion(self)->DataIngestionArtifact:
        """
        Method Name :   initiate_data_ingestion
        Description :   This method initiates the data ingestion components of training pipeline 
        
        Output      :   train set and test set are returned as the artifacts of data ingestion components
        On Failure  :   Write an exception log and then raise an exception
        """
        logging.info("Entered initiate data ingestion method of data ingestion class")
        
        try:
          dataframe = self.export_data_into_feature_store()
          logging.info("Got the dataframe from Mongodb")
          self.split_data_as_train_test(dataframe)
          logging.info("Performed train test split on the data")
          logging.info("Existed data Ingestion phase")
          
          data_ingestion_artifact = DataIngestionArtifact(trained_file_path=self.data_ingestion_config.training_file_path,
                                                          test_file_path=self.data_ingestion_config.testing_file_path)
          logging.info(f"Data Ingestion Artifact {data_ingestion_artifact}")
          return data_ingestion_artifact
          
          
        except Exception as e:
          raise MyException(e,sys)
      
  
  