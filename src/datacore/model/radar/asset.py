from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from data_model.models.base import Base
from data_model.config.database import db_config

class Asset(Base):
    """Asset model in the radar schema."""
    
    __table_args__ = {
        'schema': db_config.get_schema_name('meta', 'radar')
    }
    
    symbol: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    asset_type: Mapped[str] = mapped_column(String(50), nullable=False)
    description: Mapped[str] = mapped_column(String(500), nullable=True)
    is_active: Mapped[bool] = mapped_column(default=True) 