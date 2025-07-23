import asyncio
import logging
from abc import ABC
from typing import Type


from sqlalchemy.orm import sessionmaker
from sqlalchemy import Engine, create_engine

from tradetools.config_environment import ConfigEnvironment, get_config_environment


_log = logging.getLogger(__name__)


class BaseDB(ABC):
    conn_str_prod = ''
    conn_str_uat = ''

    def __init__(self, env: ConfigEnvironment, autocommit=False):
        self.env = env
        self.autocommit = autocommit
        self.engine: Engine = self._create_engine()
        self.session = self._create_session()
        self.dialect = self.engine.dialect.name.lower()

    def close(self):
        """Close all database connections and engines"""
        try:
            if hasattr(self, 'engine') and self.engine:
                self.engine.dispose()
        except Exception as e:
            _log.debug(f"Error disposing sync engine: {e}")

        try:
            if hasattr(self, 'async_engine') and self.async_engine:
                # For async engines, we need to run the disposal in an event loop
                try:
                    loop = asyncio.get_event_loop()
                    if loop.is_running():
                        # If loop is running, schedule the disposal
                        loop.create_task(self.async_engine.dispose())
                    else:
                        # If no loop is running, run it
                        asyncio.run(self.async_engine.dispose())
                except RuntimeError:
                    # If we can't get a loop (during shutdown), just dispose synchronously
                    pass
        except Exception as e:
            _log.error(f"Error disposing async engine: {e}")

    def _create_engine(self) -> Engine:
        if self.env == ConfigEnvironment.PROD:
            conn_str = self.conn_str_prod
        else:
            conn_str = self.conn_str_uat
        return create_engine(conn_str, echo=False, autocommit=self.autocommit)

    def _create_session(self):
        return sessionmaker(bind=self.engine, autocommit=self.autocommit)


class LazyDBInit:
    """
    To speed up the startup process
    """
    def __init__(self, db_class: Type[BaseDB]):
        self._db_class = db_class
        self._instance = None

    def _get_instance(self):
        if self._instance is None:
            if get_config_environment() == ConfigEnvironment.PROD:
                self._instance = self._db_class(env=ConfigEnvironment.PROD, autocommit=False)
                _log.info(f"Connected to PROD {self._db_class.__name__}")
            else:
                self._instance = self._db_class(env=ConfigEnvironment.UAT, autocommit=False)
                _log.info(f"Connected to UAT {self._db_class.__name__}")
        return self._instance

    def __getattr__(self, name):
        return getattr(self._get_instance(), name)

    def __repr__(self):
        return repr(self._get_instance())

    def __str__(self):
        return str(self._get_instance())

    def __call__(self, *args, **kwargs):
        return self._get_instance()(*args, **kwargs)

