import os
from enum import StrEnum

from dotenv import load_dotenv
from flask import Blueprint, Flask, request
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Mapped, mapped_column
from werkzeug.exceptions import HTTPException, NotFound

FLASK_HOST = "localhost"
FLASK_PORT = 5_000

flask_host = str(os.environ.get("HOST") or FLASK_HOST)
flask_port = int(os.environ.get("PORT") or FLASK_PORT)
is_debug = bool(os.environ.get("DEBUG"))

POSTGRES_HOST = "localhost"
POSTGRES_PROVIDER = "postgresql+psycopg"

load_dotenv()

postgres_host = str(os.environ.get("POSTGRES_HOST") or POSTGRES_HOST)
postgres_db = os.environ["POSTGRES_DB"]
postgres_password = os.environ["POSTGRES_PASSWORD"]
postgres_port = os.environ["POSTGRES_PORT"]
postgres_user = os.environ["POSTGRES_USER"]
postgres_credentials = f"{postgres_user}:{postgres_password}"
postgres_url = f"{postgres_host}:{postgres_port}"
postgres_uri = (
    f"{POSTGRES_PROVIDER}://{postgres_credentials}@{postgres_url}/{postgres_db}"
)


def make_app(bp: Blueprint, db: SQLAlchemy, migrate: Migrate) -> Flask:
    """Flask application factory."""

    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = postgres_uri

    app.register_blueprint(bp)
    db.init_app(app)
    migrate.init_app(app=app, db=db)

    return app


bp = Blueprint("api", __name__)
db = SQLAlchemy()
migrate = Migrate()


# ty:ignore[unsupported-base]
class CardModel(db.Model):
    __tablename__ = "cards"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(unique=False, nullable=False, index=True)
    desc: Mapped[str] = mapped_column(unique=False, nullable=False, index=True)


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


class CardSerializer:
    def __init__(self, card: CardModel):
        self.card = card

    def serialize(self):
        return {
            "id": self.card.id,
            "title": self.card.title,
            "desc": self.card.desc,
        }


class ManyCardSerializer:
    def __init__(self, cards: list[CardModel]):
        self.cards = cards

    def serialize(self):
        return [CardSerializer(card).serialize() for card in self.cards]


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


class Rule(StrEnum):
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


@bp.route(Rule.INDEX)
def index():
    return {"status": Status.OK}


@bp.route(Rule.HEALTH)
def health():
    return {"status": Status.OK}


@bp.route(Rule.CARDS, methods=[HTTPMethod.GET])
def cards():
    if request.method == HTTPMethod.GET:
        card_repository = CardRepository(db)

        all_cards = card_repository.get_all()

        return {
            "status": Status.OK,
            "cards": ManyCardSerializer(all_cards).serialize(),
        }


@bp.route(Rule.CARD_ADD, methods=[HTTPMethod.POST])
def card_add():
    if request.method == HTTPMethod.POST:
        card_repository = CardRepository(db)

        card = card_repository.add(
            title=request.json["title"], desc=request.json["desc"]
        )

        return {
            "status": Status.OK,
            "card": CardSerializer(card).serialize(),
        }


@bp.route(Rule.CARD_DETAIL, methods=[HTTPMethod.GET])
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
            "card": CardSerializer(card).serialize(),
        }


@bp.route(Rule.CARD_UPDATE, methods=[HTTPMethod.PUT])
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
            "card": CardSerializer(card).serialize(),
        }


@bp.route(Rule.CARD_DELETE, methods=[HTTPMethod.DELETE])
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
            "card": CardSerializer(card).serialize(),
        }


app = make_app(bp=bp, db=db, migrate=migrate)

if __name__ == "__main__":
    app.run(host=flask_host, port=flask_port, debug=is_debug)
