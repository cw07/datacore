from pydantic import BaseModel


class BaseAsset(BaseModel):

    dflow_id: str

