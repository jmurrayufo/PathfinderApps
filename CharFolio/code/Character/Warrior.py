
import logging

from . import Character

class Warrior(Character.Character):
    logger = logging.getLogger("charFolio").getChild(__module__)
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.class_ = 'warrior'