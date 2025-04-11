import os 
import sys 
import yaml
import numpy as np
from pandas import DataFrame
import dill
from src.logger import logging
from src.exception import MyException


def read_yaml_file(file_path:str)->dict:
  logging.info("Entered the read_yaml_file of utils")
  
  try:
    with open(file_path,"rb") as yaml_file:
      return yaml.safe_load(yaml_file)
    logging.info("Exited the read_yaml_file of utils")
    
  except Exception as e:
    raise MyException(e,sys)

def write_yaml_file(file_path:str,content: object,replace:bool = False):
  logging.info("Entered the write_yaml_file of utils")
  
  try:
    if replace:
      if os.path.exists(file_path):
        os.remove(file_path)
      os.makedirs(os.path.dirname(file_path),exist_ok=True)
      with open(file_path,"w") as file:
        yaml.dump(content,file)
    logging.info("Exited the write_yaml_file of utils")
      
  except Exception as e:
    raise MyException(e,sys)
        

def load_object(file_path:str)->object:
  logging.info("Entered the load_object method of utils")
  
  try:
    with open(file_path,"rb") as file_obj:
      obj = dill.load(file_obj)
      return obj
    logging.info("Exited the load_object method of utils")

  except Exception as e:
    raise MyException(e,sys)
  
def save_numpy_array_data(file_path:str,array:np.array):
  logging.info("Entered the save_numpy_array_data method of utils")
  
  try:
    dir = os.path.dirname(file_path)
    os.makedirs(dir,exist_ok=True)
    with open(file_path,"wb") as file_obj:
      np.save(file_obj,array)
    logging.info("Exited the save_numpy_array_data method of utils")
    
  except Exception as e:
    raise MyException(e,sys)
  
def load_numpy_array_data(file_path:str)->np.array:
  logging.info("Entered the load_numpy_array_data method of utils")
  
  try:
    with open(file_path,"rb") as file_obj:
      return np.load(file_obj)
    logging.info("Exited the load_numpy_array_data method of utils")
    
  except Exception as e:
    raise MyException(e,sys)


def save_object(file_path:str,obj:object)->None:
  logging.info("Entered the save object method of utils")
  try:
    dir = os.path.dirname(file_path)
    os.makedirs(dir,exist_ok=True)
    with open(file_path,"wb") as file_obj:
      dill.dump(obj,file_obj)
    logging.info("Exited the save object method of utils")
    
    
  except Exception as e:
    raise MyException(e,sys)


def drop_columns(df:DataFrame,cols:list)->DataFrame:
  logging.info("Entered drop_columns methon of utils")
  try:
    df = df.drop(columns=cols,exis=1)
    logging.info("Existed drop_columns methon of utils")
    return df
  except Exception as e:
    raise MyException(e,sys)
    


# # def drop_columns(df: DataFrame, cols: list)-> DataFrame:

# #     """
# #     drop the columns form a pandas DataFrame
# #     df: pandas DataFrame
# #     cols: list of columns to be dropped
# #     """
# #     logging.info("Entered drop_columns methon of utils")

# #     try:
# #         df = df.drop(columns=cols, axis=1)

# #         logging.info("Exited the drop_columns method of utils")
        
# #         return df
# #     except Exception as e:
# #         raise MyException(e, sys) from e