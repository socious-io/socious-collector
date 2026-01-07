import os
import sys
import argparse
from configparser import ConfigParser
from typing import Optional, List
from pydantic import field_validator
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

parser = argparse.ArgumentParser(
    description="Process some command line arguments.")

# Add the -c argument. This will expect one accompanying value (the path)
parser.add_argument('-c', '--config', type=str, required=False,
                    help="Path to the config.ini file")
args, _ = parser.parse_known_args()


class AppSettings(BaseSettings):
    """
    Application settings with validation.
    Required fields will raise an error if not provided.
    """
    # Required settings
    database_url: str
    nats_url: str

    # Optional service tokens
    idealist_token: Optional[str] = None
    adzuna_app_id: Optional[str] = None
    adzuna_app_key: Optional[str] = None
    serpapi_key: Optional[str] = None
    crunchbase_api_key: Optional[str] = None

    # AI detector settings
    ai_impact_job_detector_url: Optional[str] = None
    ai_impact_org_detector_url: Optional[str] = None
    ai_impact_detector_api_key: Optional[str] = None

    # Datadog settings
    dd_api_key: Optional[str] = None
    dd_app_key: Optional[str] = None
    dd_api_host: str = 'ap1.datadoghq.com'

    # Proxy settings
    http_proxy: Optional[str] = None

    # SQL directory
    sql_dir: str = os.path.join(os.getcwd(), 'src/core/sql')

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
        extra = 'ignore'


class Config:
    def __init__(self):
        # Validate and load settings using Pydantic
        try:
            settings = AppSettings()
        except Exception as e:
            print(f"Configuration error: {e}")
            print("\nRequired environment variables:")
            print("  - DATABASE_URL: PostgreSQL connection string")
            print("  - NATS_URL: NATS server URL")
            sys.exit(1)

        # Load sensitive information from validated settings
        self.idealist_token = settings.idealist_token
        self.nats_url = settings.nats_url
        self.database_url = settings.database_url
        self.sql_dir = settings.sql_dir

        self.http_proxy = dict(
            http=settings.http_proxy,
            https=settings.http_proxy
        )
        self.datadog = dict(
            api_key=settings.dd_api_key,
            app_key=settings.dd_app_key,
            api_host=settings.dd_api_host
        )

        self.adzuna = dict(
            app_id=settings.adzuna_app_id,
            app_key=settings.adzuna_app_key,
        )
        self.impact_job_detector = dict(
            url=settings.ai_impact_job_detector_url,
            api_key=settings.ai_impact_detector_api_key
        )
        self.impact_org_detector = dict(
            url=settings.ai_impact_org_detector_url,
            api_key=settings.ai_impact_detector_api_key
        )
        self.serpapi_key = settings.serpapi_key
        self.crunchbase_api_key = settings.crunchbase_api_key

        # Load settings from the configuration file
        config = ConfigParser()
        config.read(args.config or 'config.ini')
        self.services: List[str] = config['core']['services'].split(',')

        # Log loaded services
        print(f"Loaded services: {self.services}")


# Initialize a global configuration object

config = Config()
