import logging

from datacore.sqlalchemy.db.base_db import BaseDB
from datacore.config import TIME_LENS_STR_UAT, TIME_LENS_STR_PROD


_log = logging.getLogger(__name__)


class TimeLensDB(BaseDB):
    conn_str_prod = TIME_LENS_STR_PROD
    conn_str_uat = TIME_LENS_STR_UAT