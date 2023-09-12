import os
import argparse
from configparser import ConfigParser
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

parser = argparse.ArgumentParser(
    description="Process some command line arguments.")

# Add the -c argument. This will expect one accompanying value (the path)
parser.add_argument('-c', '--config', type=str, required=False,
                    help="Path to the config.ini file")
args = parser.parse_args()


class Config:
    def __init__(self):
        # Load sensitive information from environment variables
        self.idealist_token = os.environ.get('IDEALIST_TOKEN')
        self.nats_url = os.environ.get('NATS_URL')
        self.database_url = os.environ.get('DATABASE_URL')
        self.http_proxy = dict(
            http=os.environ.get('HTTP_PROXY'),
            https=os.environ.get('HTTP_PROXY')
        )
        self.datadog = dict(
            api_key=os.environ.get('DD_API_KEY'),
            app_key=os.environ.get('DD_APP_KEY'),
            api_host='ap1.datadoghq.com'
        )
        # Load settings from the configuration file
        config = ConfigParser()
        config.read(args.config or 'config.ini')
        self.services = config['core']['services'].split(',')
        self.sql_dir = config['core'].get('sql') or \
            os.path.join(os.getcwd(), 'src/core/sql')


# Initialize a global configuration object

config = Config()
