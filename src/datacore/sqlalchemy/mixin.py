import pandas as pd
from typing import List


class DataFrameMixin:
    @classmethod
    def to_df(cls, query_result):
        # Convert query result to a list of dictionaries
        data = [
            {column.name: getattr(instance, column.name)
             for column in cls.__table__.columns}
            for instance in query_result
        ]
        return pd.DataFrame(data)


class FutureIDMixin:
    @staticmethod
    def _construct_id_string(root_id_segment: str,
                             term: str,
                             ) -> str:
        """
        Helper method to construct an asset ID string.

        It parses the root_id_segment based on the divider_char and reconstructs
        a new ID string in the format: ROOT + TERM + DIVIDER_CHAR + SUFFIX.

        From CO.Comdty -> CO.1.Comdty

        Args:
            root_id_segment: The root part of the ID, potentially containing a suffix
                             separable by divider_char (e.g., "CO.Comdty").
            term: The term to insert into the ID (e.g., 'A','1','2','3',... '12').
            divider_char: The character used to split root_id_segment and to be
                          inserted in the new ID.

        Returns:
            The constructed asset ID string.
        """
        divider_char: str = "."
        parts = root_id_segment.split(divider_char)
        if len(parts) == 2:
            root = parts[0]
            suffix = parts[1]
        else:
            raise ValueError(f"{root_id_segment} not in correct format, example: CO.Comdty")

        return f"{root}{divider_char}{term}{divider_char}{suffix}"

    @classmethod
    def term_active(cls,
                    root_id: str,
                    ) -> str:
        return cls._construct_id_string(root_id, term='A')

    def to_asset_ids(self,
                     expand: bool = True,
                     include_active: bool = False,
                     ) -> List[str]:
        """
        Generates an asset ID or a list of asset IDs from a root id
        CO.Comdty -> [CO.1.Comdty] or
        CO.Comdty -> [CO.1.Comdty, CO.2.Comdty, CO.3.Comdty, ...]

        Args:
            root_id: A single root ID string (e.g., "CO.Comdty").
            expand: expand to all tenors or only one tenor.
            include_active: If to include CO.A.Comdty in the return list
            divider: The character used as a divider in the ID construction. Defaults to ".".

        Returns:
            A single asset ID string if root_id is a string, or a list of asset ID
            strings if root_id is a list.

        Raises:
            TypeError: If root_id is not a string or a list of strings.
        """
        if not hasattr(self, 'root_id') or self.root_id is None:
            raise ValueError('Instance must have a valid root_id attribute')

        if not hasattr(self, 'term') or self.term is None:
            raise ValueError('Instance must have a valid term attribute')

        if include_active:
            asset_ids = [self._construct_id_string(self.root_id, term='A')]
        else:
            asset_ids = []

        if expand:
            for term_i in range(1, self.term + 1):
                asset_ids.append(self._construct_id_string(self.root_id, str(term_i)))
        else:
            asset_ids.append(self._construct_id_string(self.root_id, str(self.term)))
        return asset_ids

    def to_series_ids(self, data_type: str, frequency: str, sub_frequency: str = None) -> List[str]:
        series_ids = []
        asset_ids = self.to_asset_ids()
        for asset_id in asset_ids:
            if sub_frequency is not None:
                series_id = f"fut.{asset_id}.{data_type}.{frequency}.{sub_frequency}"
            else:
                series_id = f"fut.{asset_id}.{data_type}.{frequency}"
            series_ids.append(series_id)
        return series_ids


class FXIDMixin:
    @property
    def asset_id(self):
        return self.root_id

    def to_series_id(self, data_type: str, frequency: str, sub_frequency: str = None):
        if sub_frequency is not None:
            return f"fx.{self.root_id}.{data_type}.{frequency}.{sub_frequency}"
        return f"fx.{self.root_id}.{data_type}.{frequency}"


class RollingFwdMixin:
    @property
    def asset_id(self):
        return self.root_id

    def to_series_id(self, data_type: str, frequency: str, sub_frequency: str = None):
        if sub_frequency is not None:
            return f"fwd.{self.root_id}.{data_type}.{frequency}.{sub_frequency}"
        return f"fwd.{self.root_id}.{data_type}.{frequency}"