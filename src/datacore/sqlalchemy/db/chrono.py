import time
import logging
import pandas as pd
from sqlalchemy import text
from typing import Union, Dict

from datacore.sqlalchemy.db.base_db import BaseDB
from datacore.config import CHRONO_STR_PROD, CHRONO_STR_UAT



_log = logging.getLogger(__name__)


class ChronoDB(BaseDB):
    conn_str_prod = CHRONO_STR_PROD
    conn_str_uat = CHRONO_STR_UAT

    def _get_table_schema(self, table: str, schema: str) -> dict:
        """Get column definitions from target table"""

        if self.dialect in ['mssql', 'sqlserver']:
            sql = """
                  SELECT COLUMN_NAME, \
                         DATA_TYPE, \
                         CHARACTER_MAXIMUM_LENGTH, \
                         NUMERIC_PRECISION, \
                         NUMERIC_SCALE, \
                         IS_NULLABLE
                  FROM INFORMATION_SCHEMA.COLUMNS
                  WHERE TABLE_SCHEMA = :schema
                    AND TABLE_NAME = :table
                  ORDER BY ORDINAL_POSITION \
                  """

        elif self.dialect == 'postgresql':
            sql = """
                  SELECT column_name, \
                         data_type, \
                         character_maximum_length, \
                         numeric_precision, \
                         numeric_scale, \
                         is_nullable
                  FROM information_schema.columns
                  WHERE table_schema = :schema
                    AND table_name = :table
                  ORDER BY ordinal_position \
                  """

        elif self.dialect == 'mysql':
            sql = """
                  SELECT COLUMN_NAME              as column_name, \
                         DATA_TYPE                as data_type, \
                         CHARACTER_MAXIMUM_LENGTH as character_maximum_length, \
                         NUMERIC_PRECISION        as numeric_precision, \
                         NUMERIC_SCALE            as numeric_scale, \
                         IS_NULLABLE              as is_nullable
                  FROM INFORMATION_SCHEMA.COLUMNS
                  WHERE TABLE_SCHEMA = :schema
                    AND TABLE_NAME = :table
                  ORDER BY ORDINAL_POSITION \
                  """

        else:
            raise NotImplementedError(f"Unsupported dialect: {self.dialect}")

        with self.engine.connect() as conn:
            result = conn.execute(text(sql), parameters={'schema': schema, 'table': table})
            columns = {}
            for row in result:
                col_name = row[0]
                data_type = row[1]
                max_length = row[2]
                precision = row[3]
                scale = row[4]
                nullable = row[5]

                columns[col_name] = {
                    'data_type': data_type,
                    'max_length': max_length,
                    'precision': precision,
                    'scale': scale,
                    'nullable': nullable
                }

        return columns

    def _get_sqlalchemy_types_for_table(self, table: str, schema: str) -> dict:
        """Get SQLAlchemy type objects for pandas to_sql dtype parameter"""
        from sqlalchemy import String, Integer, Float, Date, DateTime, Boolean

        table_schema = self._get_table_schema(table, schema)
        sqlalchemy_types = {}

        for col_name, col_info in table_schema.items():
            data_type = col_info['data_type'].lower()

            if data_type in ['varchar', 'nvarchar', 'char', 'nchar']:
                max_len = col_info['max_length'] or 255
                sqlalchemy_types[col_name] = String(max_len)
            elif data_type in ['int', 'integer', 'bigint', 'smallint']:
                sqlalchemy_types[col_name] = Integer()
            elif data_type in ['float', 'real', 'double']:
                sqlalchemy_types[col_name] = Float()
            elif data_type == 'date':
                sqlalchemy_types[col_name] = Date()
            elif data_type in ['datetime', 'timestamp']:
                sqlalchemy_types[col_name] = DateTime()
            elif data_type in ['bit', 'boolean']:
                sqlalchemy_types[col_name] = Boolean()
            else:
                raise ValueError(f"Unsupported data type: {data_type}")

        return sqlalchemy_types

    def _get_primary_key_columns(self, schema: str, table: str):
        db_type = self.dialect
        pk_columns = []

        if db_type in ['mssql', 'sqlserver']:
            sql = """
                  SELECT kcu.COLUMN_NAME
                  FROM INFORMATION_SCHEMA.TABLE_CONSTRAINTS tc
                           JOIN INFORMATION_SCHEMA.KEY_COLUMN_USAGE kcu
                                ON tc.CONSTRAINT_NAME = kcu.CONSTRAINT_NAME
                                    AND tc.TABLE_SCHEMA = kcu.TABLE_SCHEMA
                                    AND tc.TABLE_NAME = kcu.TABLE_NAME
                  WHERE tc.TABLE_SCHEMA = :schema
                    AND tc.TABLE_NAME = :table
                    AND tc.CONSTRAINT_TYPE = 'PRIMARY KEY'
                  ORDER BY kcu.ORDINAL_POSITION \
                  """

        elif db_type == 'postgresql':
            sql = """
                  SELECT kcu.column_name
                  FROM information_schema.table_constraints tc
                           JOIN information_schema.key_column_usage kcu
                                ON tc.constraint_name = kcu.constraint_name
                                    AND tc.table_schema = kcu.table_schema
                                    AND tc.table_name = kcu.table_name
                  WHERE tc.table_schema = :schema
                    AND tc.table_name = :table
                    AND tc.constraint_type = 'PRIMARY KEY'
                  ORDER BY kcu.ordinal_position \
                  """

        elif db_type == 'mysql':
            sql = """
                  SELECT COLUMN_NAME
                  FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE
                  WHERE TABLE_SCHEMA = :schema
                    AND TABLE_NAME = :table
                    AND CONSTRAINT_NAME = 'PRIMARY'
                  ORDER BY ORDINAL_POSITION \
                  """

        else:
            raise ValueError(f"Unsupported database type: {db_type}")

        try:
            with self.engine.connect() as conn:
                result = conn.execute(text(sql), parameters={'schema': schema, 'table': table})
                pk_columns = [row[0] for row in result.fetchall()]
        except Exception as e:
            raise RuntimeError(f"Error querying primary key for {schema}.{table}: {str(e)}")

        if not pk_columns:
            raise ValueError(f"No primary key found for table {schema}.{table}")

        return pk_columns


    def insert_new_only(self, schema: str, table: str, data: pd.DataFrame):
        if len(data) == 0:
            return

        try:
            pk_columns = self._get_primary_key_columns(schema, table)
        except Exception as e:
            raise RuntimeError(f"Failed to get primary key columns: {str(e)}")

        sqlalchemy_types = self._get_sqlalchemy_types_for_table(table, schema)

        temp_table_name = f"temp_{table}_{int(time.time())}"

        try:
            data.to_sql(temp_table_name,
                        schema=schema,
                        con=self.engine,
                        if_exists='replace',
                        index=False,
                        dtype=sqlalchemy_types
                        )
        except Exception as e:
            raise RuntimeError(f"Failed to create temp table: {str(e)}")

        try:
            join_conditions = []
            for col in pk_columns:
                quoted_col = self._quote_identifier(col)
                join_conditions.append(f"t.{quoted_col} = s.{quoted_col}")

            join_clause = " AND ".join(join_conditions)

            # Use first PK column for the WHERE IS NULL check
            first_pk_col = self._quote_identifier(pk_columns[0])

            # Get schema prefixes
            target_schema_prefix = self._get_schema_prefix(schema)
            temp_schema_prefix = f"{schema}."

            sql = f"""
               SELECT t.*
               FROM {temp_schema_prefix}{temp_table_name} t
               LEFT JOIN {target_schema_prefix}{table} s ON {join_clause}
               WHERE s.{first_pk_col} IS NULL
           """

            to_insert = pd.read_sql_query(sql, con=self.engine)  # Not insert into is there is some weird order issue
            if to_insert.empty:
                _log.info(f"Data already exists in {schema}.{table}; nothing to insert.")
            else:
                rows_inserted = to_insert.to_sql(table,
                                                 schema=schema,
                                                 con=self.engine,
                                                 if_exists='append',
                                                 index=False
                                                 )
                _log.debug(f"Inserted {rows_inserted} new records into {schema}.{table}")
        except Exception as e:
            raise RuntimeError(f"Failed to insert new records: {str(e)}")

        finally:
            try:
                drop_schema_prefix = f"{schema}."
                with self.engine.connect() as conn:
                    conn.execute(text(f"DROP TABLE {drop_schema_prefix}{temp_table_name}"))
                    conn.commit()
            except Exception as e:
                _log.debug(f"Warning: Failed to drop temp table {temp_table_name}: {str(e)}")


    def upsert(self, schema: str, table: str, data: Union[pd.DataFrame, Dict]):
        if isinstance(data, pd.DataFrame):
            pass
        elif isinstance(data, dict):
            pass
        else:
            raise NotImplementedError(f"Unsupported data type: {type(data)}")







