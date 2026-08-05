from sqlalchemy.orm import Mapped, mapped_column

from server.db import db


# ty:ignore[unsupported-base]
class CardModel(db.Model):
    __tablename__ = "cards"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(unique=False, nullable=False, index=True)
    desc: Mapped[str] = mapped_column(unique=False, nullable=False, index=True)
