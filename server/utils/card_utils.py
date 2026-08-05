from server.models import CardModel


class CardSerializer:
    def __init__(self, card: CardModel):
        self.card = card

    def serialize(self):
        return {
            "id": self.card.id,
            "title": self.card.title,
            "desc": self.card.desc,
        }


class CardListSerializer:
    def __init__(self, cards: list[CardModel]):
        self.cards = cards

    def serialize(self):
        return [CardSerializer(card).serialize() for card in self.cards]
