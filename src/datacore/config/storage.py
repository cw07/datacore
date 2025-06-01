from typing import Dict, Optional
from pydantic import BaseSettings
import os
from airflow.hooks.base import BaseHook
from airflow.exceptions import AirflowException

class StorageSettings(BaseSettings):
    """Base storage settings."""
    type: str  # s3, gcs, azure_blob, local, etc.
    bucket: Optional[str] = None
    path: Optional[str] = None
    credentials: Optional[Dict] = None

class StorageConfig:
    """Storage configuration manager."""
    
    def __init__(self):
        self._storage_settings: Dict[str, StorageSettings] = {}
        self._is_airflow = 'AIRFLOW_HOME' in os.environ
        self._load_config()
    
    def _get_credentials_from_airflow(self, conn_id: str) -> Dict:
        """Get credentials from Airflow connection."""
        try:
            conn = BaseHook.get_connection(conn_id)
            return {
                'access_key': conn.login,
                'secret_key': conn.password,
                'region': conn.extra_dejson.get('region'),
                'endpoint': conn.extra_dejson.get('endpoint')
            }
        except AirflowException:
            raise ValueError(f"Airflow connection '{conn_id}' not found")
    
    def _load_config(self):
        """Load storage configurations from YAML file."""
        config_path = os.path.join(os.path.dirname(__file__), 'storage.yaml')
        
        if not os.path.exists(config_path):
            self._create_default_config(config_path)
        
        import yaml
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
            
        for storage_name, settings in config.get('storages', {}).items():
            if self._is_airflow and settings.get('credentials_id'):
                settings['credentials'] = self._get_credentials_from_airflow(settings['credentials_id'])
            self._storage_settings[storage_name] = StorageSettings(**settings)
    
    def _create_default_config(self, config_path: str):
        """Create default configuration file."""
        default_config = {
            'storages': {
                'raw_data': {
                    'type': 's3',
                    'bucket': 'raw-data-bucket',
                    'path': 'raw/',
                    'credentials_id': 's3_raw_data_conn'
                },
                'processed_data': {
                    'type': 'gcs',
                    'bucket': 'processed-data-bucket',
                    'path': 'processed/',
                    'credentials_id': 'gcs_processed_data_conn'
                },
                'model_artifacts': {
                    'type': 'azure_blob',
                    'bucket': 'model-artifacts',
                    'path': 'models/',
                    'credentials_id': 'azure_model_artifacts_conn'
                }
            }
        }
        
        import yaml
        with open(config_path, 'w') as f:
            yaml.dump(default_config, f, default_flow_style=False)
    
    def get_storage_settings(self, storage_name: str) -> StorageSettings:
        """Get storage settings for a specific storage."""
        if storage_name not in self._storage_settings:
            raise ValueError(f"Storage '{storage_name}' not found in configuration")
        return self._storage_settings[storage_name]

# Create a singleton instance
storage_config = StorageConfig() 