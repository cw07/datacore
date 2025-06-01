from typing import Dict, Optional
from pydantic import BaseSettings
from sqlalchemy.engine import URL
import yaml
from pathlib import Path
import os
from airflow.hooks.base import BaseHook
from airflow.exceptions import AirflowException

class DatabaseSettings(BaseSettings):
    """Base database settings that all databases will inherit."""
    host: str = "localhost"
    port: int = 5432
    user: str = "postgres"
    password: str = ""
    name: str = ""

class DatabaseConfig:
    """Database configuration manager."""
    
    def __init__(self):
        self._db_settings: Dict[str, DatabaseSettings] = {}
        self._schemas: Dict[str, Dict[str, str]] = {}
        self._is_airflow = self._check_airflow_environment()
        self._load_config()
    
    def _check_airflow_environment(self) -> bool:
        """Check if running in Airflow environment."""
        return 'AIRFLOW_HOME' in os.environ
    
    def _get_password_from_airflow(self, conn_id: str) -> str:
        """Get password from Airflow connection."""
        try:
            conn = BaseHook.get_connection(conn_id)
            return conn.password
        except AirflowException:
            raise ValueError(f"Airflow connection '{conn_id}' not found")
    
    def _get_password(self, password_value: str) -> str:
        """Get password from environment variable or Airflow connection."""
        if not password_value.startswith('${') or not password_value.endswith('}'):
            return password_value
            
        # Extract the variable name from ${VARIABLE_NAME}
        var_name = password_value[2:-1]
        
        if self._is_airflow:
            # In Airflow, use the connection ID as is
            return self._get_password_from_airflow(var_name)
        else:
            # In non-Airflow environment, use environment variable
            password = os.environ.get(var_name)
            if password is None:
                raise ValueError(f"Environment variable '{var_name}' not found")
            return password
    
    def _load_config(self):
        """Load database configurations from YAML file."""
        config_path = Path(__file__).parent / "databases.yaml"
        
        if not config_path.exists():
            # Create default config if it doesn't exist
            self._create_default_config(config_path)
        
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
            
        # Load database settings
        for db_name, settings in config.get('databases', {}).items():
            # Process password if it's a variable reference
            if isinstance(settings.get('password'), str):
                settings['password'] = self._get_password(settings['password'])
            self._db_settings[db_name] = DatabaseSettings(**settings)
        
        # Load schema mappings
        self._schemas = config.get('schemas', {})
    
    def _create_default_config(self, config_path: Path):
        """Create default configuration file."""
        default_config = {
            'databases': {
                'meta': {
                    'host': 'localhost',
                    'port': 5432,
                    'user': 'postgres',
                    'password': '${meta_db_conn}',  # Airflow connection ID
                    'name': 'meta'
                },
                'mktdata_01': {
                    'host': 'localhost',
                    'port': 5432,
                    'user': 'postgres',
                    'password': '${mktdata_01_conn}',  # Airflow connection ID
                    'name': 'mktdata_01'
                }
            },
            'schemas': {
                'meta': {
                    'radar': 'radar',
                    'refdata': 'refdata'
                },
                'mktdata': {
                    'public': 'public'
                }
            }
        }
        
        with open(config_path, 'w') as f:
            yaml.dump(default_config, f, default_flow_style=False)
    
    def get_db_url(self, db_name: str) -> URL:
        """Get database URL for a specific database."""
        if db_name not in self._db_settings:
            raise ValueError(f"Database '{db_name}' not found in configuration")
        
        settings = self._db_settings[db_name]
        return URL.create(
            drivername="postgresql",
            username=settings.user,
            password=settings.password,
            host=settings.host,
            port=settings.port,
            database=settings.name
        )
    
    def get_schema_name(self, db_name: str, schema_key: str) -> str:
        """Get the full schema name for a given database and schema key."""
        return self._schemas.get(db_name, {}).get(schema_key, "public")
    
    def add_database(self, db_name: str, settings: Dict[str, any], schemas: Optional[Dict[str, str]] = None):
        """Add a new database configuration dynamically."""
        if isinstance(settings.get('password'), str):
            settings['password'] = self._get_password(settings['password'])
        self._db_settings[db_name] = DatabaseSettings(**settings)
        if schemas:
            self._schemas[db_name] = schemas
    
    def remove_database(self, db_name: str):
        """Remove a database configuration."""
        self._db_settings.pop(db_name, None)
        self._schemas.pop(db_name, None)
    
    def save_config(self):
        """Save current configuration to YAML file."""
        config = {
            'databases': {
                name: settings.dict()
                for name, settings in self._db_settings.items()
            },
            'schemas': self._schemas
        }
        
        config_path = Path(__file__).parent / "databases.yaml"
        with open(config_path, 'w') as f:
            yaml.dump(config, f, default_flow_style=False)

# Create a singleton instance
db_config = DatabaseConfig() 