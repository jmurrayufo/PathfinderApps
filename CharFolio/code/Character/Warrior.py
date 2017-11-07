
from . import Character

class Warrior(Character.Character):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.class_ = 'warrior'