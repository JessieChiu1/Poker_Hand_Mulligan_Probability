class Card:
    def __init__(self, suit, value):
        if suit not in ["♠️", "♥️", "♣️", "♦️"]:
            raise ValueError("Invalid suit")
        if value not in range(2,15):
            raise ValueError("Invalid value")
        self.suit = suit
        self.value = value
        self.face = self.get_face_name()

    def get_face_name(self):
        face_names = {2: "2", 3: "3", 4: "4", 5: "5", 6: "6", 7: "7", 8: "8", 9: "9", 10: "10", 11: "Jack", 12: "Queen", 13: "King", 14: "Ace"}
        return face_names[self.value]

    def __str__(self):
        return f"{self.face}{self.suit}"