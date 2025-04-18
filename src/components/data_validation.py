import json
import sys
import os
import yaml
import pandas as pd

from pandas import DataFrame

from src.exception import MyException
from src.logger import logging
from src.utils.main_utils import read_yaml_file
from src.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
from src.entity.config_entity import DataValidationConfig
from src.constants import SCHEMA_FILE_PATH

class DataValidation:
  """Data Validation is used to validate the data which is get from Mongo Db"""
  def __init__(self,data_ingestion_artifact:DataIngestionArtifact,data_validation_config:DataValidationConfig):
    try:
      self.data_validation_config=data_validation_config
      self.data_ingestion_artifact=data_ingestion_artifact
      self._schema_config = read_yaml_file(SCHEMA_FILE_PATH)
    except Exception as e:
      raise MyException(e,sys)

  def validate_number_of_columns(self,dataframe:DataFrame)-> bool:
    status = len(dataframe.columns) == len(self._schema_config['columns'])
    logging.info(f"check columns issue dataframe columns ->{dataframe.columns} schema_config columns -> {self._schema_config['columns']}")
    logging.info(f"Is required columns present while data validation {status}")
    return status
  
  def is_column_exist(self,df: DataFrame)-> bool:
    try:
      dataframe_columns = df.columns
      missing_numerical_columns = []
      missing_categorical_columns = []
      for col in self._schema_config['numerical_columns']:
        if col not in dataframe_columns:
          missing_numerical_columns.append(col)
          
      if len(missing_numerical_columns)>0:
        logging.info(f"Missing numerical column in data validation : {missing_numerical_columns}")
        
      for col in self._schema_config['categorical_columns']:
        if col not in dataframe_columns:
          missing_categorical_columns.append(col)
          
      if len(missing_categorical_columns)>0:
        logging.info(f"Missing categorical column in data validation : {missing_categorical_columns}")
      return False if len(missing_numerical_columns)>0 or len(missing_categorical_columns)>0 else True 
    except Exception as e:
      raise MyException(e,sys)
  @staticmethod
  def read_data(file_path:str)->DataFrame:
    try:
      return pd.read_csv(file_path)
    except Exception as e:
      raise MyException(e,sys)
    
  def initiate_data_validation(self)->DataValidationArtifact:
    try:
      validation_error_msg = ""
      logging.info("Starting Data Validation")
      train_df,test_df = (DataValidation.read_data(file_path=self.data_ingestion_artifact.trained_file_path),DataValidation.read_data(file_path=self.data_ingestion_artifact.test_file_path))
      
      logging.info("Checking Columns length of Dataframe")
      status = self.validate_number_of_columns(dataframe=train_df)
      if not status:
        validation_error_msg += f"Columns are missing in training Dataframe"
      else:
        logging.info(f'All required columns present in training Dataframe : {status}')
      status = self.validate_number_of_columns(dataframe=test_df)
      if not status:
        validation_error_msg += f"Columns are missing in test Dataframe"
      else:
        logging.info(f'All required columns present in test Dataframe : {status}')
        
      logging.info('Checking Numerical and Categrical columns exist accurately')
      status = self.is_column_exist(df=train_df)
   
      if not status:
                validation_error_msg += f"Columns are missing in training dataframe. "
      else:
                logging.info(f"All categorical/int columns present in training dataframe: {status}")
      status = self.is_column_exist(df=test_df)
      if not status:
                validation_error_msg += f"Columns are missing in test dataframe. "
      else:
                logging.info(f"All categorical/int columns present in test dataframe: {status}")

      validation_status = len(validation_error_msg)==0
      data_validation_artifact = DataValidationArtifact(
        validation_status=validation_status,
        message=validation_error_msg,
        validation_report_file_path = self.data_validation_config.validation_report_file_path
      )
      report_file = os.path.dirname(self.data_validation_config.validation_report_file_path)
      os.makedirs(report_file,exist_ok=True)
      logging.info("writing data to report yaml file")
      validation_report = {
        "validation_status": validation_status,
        "message":validation_error_msg.strip()
      }
      with open(self.data_validation_config.validation_report_file_path,"w") as obj:
        json.dump(validation_report,obj,indent=4)
        
      logging.info("Data validation artifact created and saved to JSON file.")
      logging.info(f"Data validation artifact: {data_validation_artifact}")
      return data_validation_artifact
    except Exception as e:
      MyException(e,sys)
  