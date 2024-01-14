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
        self.sql_dir = os.environ.get('SQL_DIR') or \
            os.path.join(os.getcwd(), 'src/core/sql')
        self.http_proxy = dict(
            http=os.environ.get('HTTP_PROXY'),
            https=os.environ.get('HTTP_PROXY')
        )
        self.datadog = dict(
            api_key=os.environ.get('DD_API_KEY'),
            app_key=os.environ.get('DD_APP_KEY'),
            api_host='ap1.datadoghq.com'
        )

        self.adzuna = dict(
            app_id=os.environ.get('ADZUNA_APP_ID'),
            app_key=os.environ.get('ADZUNA_APP_KEY'),
        )
        self.impact_job_detector = dict(
            url=os.environ.get('AI_IMPACT_JOB_DETECTOR_URL'),
            api_key=os.environ.get('AI_IMPACT_JOB_DETECTOR_API_KEY')
        )
        self.serpapi_key = os.environ.get('SERP_API_KEY')
        # Load settings from the configuration file
        config = ConfigParser()
        config.read(args.config or 'config.ini')
        self.services = config['core']['services'].split(',')


# Initialize a global configuration object

config = Config()
