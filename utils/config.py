from dotenv import load_dotenv
from os import environ

__all__ = 'Config',

load_dotenv()


class Config:
    DATASET = environ['DATASET_CSV']
    MYSQL_HOST = environ['MYSQL_HOST']
    MYSQL_PORT = environ['MYSQL_PORT']
    MYSQL_USER = environ['MYSQL_USER']
    MYSQL_PASSWD = environ['MYSQL_PASSWD']
    PINECONE_API_KEY = environ['PINECONE_API']
    PINECONE_INDEX = environ['PINECONE_INDEX']
    PINECONE_ENVIRONMENT = environ['PINECONE_ENVIRONMENT']
    MODEL_NAME = environ['MODEL_NAME']
    MODEL_DIMENTIONS = int(environ['MODEL_DIMENTIONS'])
