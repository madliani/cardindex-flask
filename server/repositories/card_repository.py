from flask_sqlalchemy import SQLAlchemy

from server.models import CardModel


class CardRepository:
    def __init__(self, db: SQLAlchemy):
        self.db = db

    def get_all(self) -> list[CardModel]:
        return self.db.session.query(CardModel).all()

    def add(self, title: str, desc: str) -> CardModel:
        card = CardModel(title=title, desc=desc)

        self.db.session.add(card)
        self.db.session.commit()

        return card

    def get(self, id: int) -> CardModel | None:
        return self.db.session.query(CardModel).get(id)

    def update(self, id: int, title: str, desc: str) -> CardModel | None:
        card = self.db.session.query(CardModel).get(id)

        if card is None:
            return None

        card.title = title
        card.desc = desc

        self.db.session.commit()

        return card

    def delete(self, id: int) -> CardModel | None:
        card = self.db.session.query(CardModel).get(id)

        if card is None:
            return None

        self.db.session.delete(card)
        self.db.session.commit()

        return card
