from flask import request
from werkzeug.exceptions import NotFound

from server.bp import bp
from server.database import db
from server.enums import HTTPMethod, Rule, Status
from server.repositories import CardRepository
from server.utils import (
    CardListSerializer,
    CardSerializer,
    HTTPExceptionSerializer,
)


@bp.route(Rule.CARDS, methods=[HTTPMethod.GET])
def cards():
    if request.method == HTTPMethod.GET:
        card_repository = CardRepository(db)

        all_cards = card_repository.get_all()

        return {
            "status": Status.OK,
            "cards": CardListSerializer(all_cards).serialize(),
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
