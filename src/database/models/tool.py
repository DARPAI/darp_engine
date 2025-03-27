from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy import UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from ...database import models
from .base import Base


class Tool(Base):
    __tablename__ = "tool"
    __table_args__ = (
        UniqueConstraint("name", "server_url", name="uq_tool_name_server_url"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(), nullable=False)
    description: Mapped[str] = mapped_column(String(), nullable=False)
    input_schema: Mapped[dict] = mapped_column(JSONB, nullable=False)
    server_url: Mapped[str] = mapped_column(
        ForeignKey("server.url", ondelete="CASCADE")
    )
    server: Mapped["models.server.Server"] = relationship(back_populates="tools")
