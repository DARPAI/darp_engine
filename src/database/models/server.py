from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from .base import Base


class Server(Base):
    __tablename__ = "server"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    url: Mapped[str] = mapped_column(String(), nullable=False, unique=True)
    name: Mapped[str] = mapped_column(String(), nullable=False, unique=True)
    description: Mapped[str] = mapped_column(String(), nullable=False)
    logo: Mapped[str] = mapped_column(String())
    tools: Mapped[list["Tool"]] = relationship(back_populates="server")  # noqa
