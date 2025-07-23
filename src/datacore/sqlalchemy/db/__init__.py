from datacore.sqlalchemy.db.base_db import LazyDBInit
from datacore.sqlalchemy.db.chrono import ChronoDB
from datacore.sqlalchemy.db.time_lens import TimeLensDB


__all__ = ['chrono_db', 'time_lens_db']


chrono_db = LazyDBInit(ChronoDB)
time_lens_db = LazyDBInit(TimeLensDB)