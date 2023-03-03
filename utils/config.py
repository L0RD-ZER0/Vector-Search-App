from dotenv import load_dotenv
from os import environ

__all__ = 'Config',

load_dotenv()


class Config:
    MYSQL_HOST = environ['MYSQL_HOST']
    MYSQL_PORT = environ['MYSQL_PORT']
    MYSQL_PASSWD = environ['MYSQL_PASSWD']
    MYSQL_USER = 'root'
    PINECONE_API_KEY = environ['PINECONE_API']
    MODEL_NAME = environ['MODEL_NAME']
