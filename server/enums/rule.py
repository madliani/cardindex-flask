from enum import StrEnum


class Rule(StrEnum):
    INDEX = "/"
    HEALTH = "/health"
    CARDS = "/cards"
    CARD_ADD = "/cards/add"
    CARD_DETAIL = "/cards/<int:id>"
    CARD_UPDATE = "/cards/<int:id>/update"
    CARD_DELETE = "/cards/<int:id>/delete"
