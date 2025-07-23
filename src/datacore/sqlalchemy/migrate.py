from datacore.sqlalchemy.base import Base
from datacore.sqlalchemy.db import chrono_db, time_lens_db


def migrate_models_to_db():
    Base.metadata.create_all(chrono_db.engine)
    Base.metadata.create_all(time_lens_db.engine)

if __name__ == '__main__':
    migrate_models_to_db()