import os
from configparser import ConfigParser
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    def __init__(self):
        # Load sensitive information from environment variables
        self.idealist_token = os.environ.get(
            'IDEALIST_TOKEN', '743e1f3940484d7680130c748ed22758')
        self.nats_url = os.environ.get('NATS_URL')
        self.database_url = os.environ.get('DATABASE_URL')

        # Load settings from the configuration file
        config = ConfigParser()
        config.read("config.ini")


# Initialize a global configuration object
config = Config()
