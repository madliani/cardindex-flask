from enum import StrEnum

from flask import Flask, request
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Mapped, mapped_column
from werkzeug.exceptions import HTTPException, NotFound

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///cardindex.db"


db = SQLAlchemy(app=app)
migrate = Migrate(app=app, db=db)


# ty:ignore[unsupported-base]
class Card(db.Model):
    __tablename__ = "cards"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(unique=False, nullable=False)
    desc: Mapped[str] = mapped_column(unique=False, nullable=False)


class CardRepository:
    def __init__(self, db: SQLAlchemy):
        self.db = db

    def get_all(self) -> list[Card]:
        return self.db.session.query(Card).all()

    def add_card(self, title: str, desc: str) -> Card:
        card = Card(title=title, desc=desc)

        self.db.session.add(card)
        self.db.session.commit()

        return card

    def get(self, id: int) -> Card | None:
        return self.db.session.query(Card).get(id)

    def update(self, id: int, title: str, desc: str) -> Card | None:
        card = self.db.session.query(Card).get(id)

        if card is None:
            return None

        card.title = title
        card.desc = desc

        self.db.session.commit()

        return card

    def delete(self, id: int) -> Card | None:
        card = self.db.session.query(Card).get(id)

        if card is None:
            return None

        self.db.session.delete(card)
        self.db.session.commit()

        return card


class OneCardSerializer:
    def __init__(self, card: Card):
        self.card = card

    def serialize(self):
        return {
            "id": self.card.id,
            "title": self.card.title,
            "desc": self.card.desc,
        }


class ManyCardSerializer:
    def __init__(self, cards: list[Card]):
        self.cards = cards

    def serialize(self):
        return [OneCardSerializer(card).serialize() for card in self.cards]


class HTTPExceptionSerializer:
    def __init__(self, error: HTTPException):
        self.error = error

    def serialize(self):
        return {
            "code": self.error.code,
            "name": self.error.name,
            "description": self.error.description,
        }


class HTTPMethod(StrEnum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"


class RoutePath(StrEnum):
    INDEX = "/"
    HEALTH = "/health"
    CARDS = "/cards"
    CARD_ADD = "/cards/add"
    CARD_DETAIL = "/cards/<int:id>"
    CARD_UPDATE = "/cards/<int:id>/update"
    CARD_DELETE = "/cards/<int:id>/delete"


class Status(StrEnum):
    ERROR = "error"
    OK = "ok"


@app.route(RoutePath.INDEX)
def index():
    return {"status": Status.OK}, 200


@app.route(RoutePath.HEALTH)
def health():
    return {"status": Status.OK}, 200


@app.route(RoutePath.CARDS, methods=[HTTPMethod.GET])
def cards():
    if request.method == HTTPMethod.GET:
        card_repository = CardRepository(db)

        all_cards = card_repository.get_all()

        return {
            "status": Status.OK,
            "cards": ManyCardSerializer(all_cards).serialize(),
        }, 200


@app.route(RoutePath.CARD_ADD, methods=[HTTPMethod.POST])
def card_add():
    if request.method == HTTPMethod.POST:
        card_repository = CardRepository(db)

        card = card_repository.add_card(
            title=request.json["title"], desc=request.json["desc"]
        )

        return {
            "status": Status.OK,
            "card": OneCardSerializer(card).serialize(),
        }, 200


@app.route(RoutePath.CARD_DETAIL, methods=[HTTPMethod.GET])
def card_detail(id: int):
    if request.method == HTTPMethod.GET:
        card_repository = CardRepository(db)

        card = card_repository.get(id)

        if card is None:
            error = NotFound(f"Card with id = {id} not found")

            return {
                "status": Status.ERROR,
                "error": HTTPExceptionSerializer(error).serialize(),
            }, error.code

        return {
            "status": Status.OK,
            "card": OneCardSerializer(card).serialize(),
        }, 200


@app.route(RoutePath.CARD_UPDATE, methods=[HTTPMethod.PUT])
def card_update(id: int):
    if request.method == HTTPMethod.PUT:
        card_repository = CardRepository(db)

        card = card_repository.update(
            id=id, title=request.json["title"], desc=request.json["desc"]
        )

        if card is None:
            error = NotFound(f"Card with id = {id} not found")

            return {
                "status": Status.ERROR,
                "error": HTTPExceptionSerializer(error).serialize(),
            }, error.code

        return {
            "status": Status.OK,
            "card": OneCardSerializer(card).serialize(),
        }, 200


@app.route(RoutePath.CARD_DELETE, methods=[HTTPMethod.DELETE])
def card_delete(id: int):
    if request.method == HTTPMethod.DELETE:
        card_repository = CardRepository(db)

        card = card_repository.delete(id)

        if card is None:
            error = NotFound(f"Card with id = {id} not found")

            return {
                "status": Status.ERROR,
                "error": HTTPExceptionSerializer(error).serialize(),
            }, error.code

        return {
            "status": Status.OK,
            "card": OneCardSerializer(card).serialize(),
        }, 200
