from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, ForeignKey
from game.database.base import Base

class PlayerState(Base):
    __tablename__ = "player_state"

    save_id: Mapped[int] = mapped_column(ForeignKey("saves.id", ondelete="CASCADE"), primary_key=True)
    x: Mapped[int] = mapped_column(Integer, nullable=False, default=20)
    y: Mapped[int] = mapped_column(Integer, nullable=False, default=20)
    hp: Mapped[int] = mapped_column(Integer, nullable=False, default=100)
    max_hp: Mapped[int] = mapped_column(Integer, nullable=False, default=100)
    attack: Mapped[int] = mapped_column(Integer, nullable=False, default=20)
        