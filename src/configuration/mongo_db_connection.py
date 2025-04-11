import os 
import sys 
import pymongo
import certifi

from src.logger import logging
from src.exception import MyException
from src.constants import DATABASE_NAME,MONGODB_URL_KEY


# # Load the certificate authority file to avoid timeout errors when connecting to MongoDB
ca = certifi.where()

class MongoDBClient:
    """MongoDB Client is used for establishing a connection with a Mongo DB"""
  
    # A shared mongo db client instace which will remail common for all mongdb client instances 
    client = None 
    def __init__(self, database_name: str = DATABASE_NAME) -> None:
          """
          Initializes a connection to the MongoDB database. If no existing connection is found, it establishes a new one.

          Parameters:
          ----------
          database_name : str, optional
              Name of the MongoDB database to connect to. Default is set by DATABASE_NAME constant.

          Raises:
          ------
          MyException
              If there is an issue connecting to MongoDB or if the environment variable for the MongoDB URL is not set.
        """
          try:
            # Check if a MongoDB client connection has already been established; if not, create a new one
            if MongoDBClient.client is None:
              mongo_db_url = MONGODB_URL_KEY
            if mongo_db_url is None:
              raise MyException(f"Environment variable '{MONGODB_URL_KEY}' is not set.")
            
            # Establishing a new mongodb connection .
            MongoDBClient.client = pymongo.MongoClient(mongo_db_url, tlsCAFile=ca)
            
            # Use the shared MongoClient for this instance
            self.client = MongoDBClient.client 
            self.database = self.client[database_name]
            self.dastabase_name = self.database 
            logging.info("MongoDB Connection Successfull")
            
            
          except Exception as e:
            # Raise a custom exception with traceback details if connection fails
            raise MyException(e,sys)
        
  
