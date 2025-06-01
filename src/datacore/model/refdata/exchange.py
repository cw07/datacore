from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from data_model.models.base import Base
from data_model.config.database import db_config

class Exchange(Base):
    """Exchange model in the refdata schema."""
    
    __table_args__ = {
        'schema': db_config.get_schema_name('meta', 'refdata')
    }
    
    code: Mapped[str] = mapped_column(String(10), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    country: Mapped[str] = mapped_column(String(50), nullable=False)
    timezone: Mapped[str] = mapped_column(String(50), nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True)
    trading_hours: Mapped[str] = mapped_column(String(200), nullable=True) 