
import logging
import json

from . import Item

class Armor(Item.Item):

    logger = logging.getLogger("charFolio").getChild(__module__)

    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.armor_bonus = kwargs.get("armor_bonus", 1)
        self.shield_bonus = kwargs.get("shield_bonus", None)
        self.max_dex_bonus = kwargs.get("max_dex_bonus", 8)
        self.ac_penalty = kwargs.get("ac_penalty", 0)
        self.arcane_spell_failure = kwargs.get("arcane_spell_failure", 0.05)


    def save(self, file_):
        with open(file_,'w') as fp:
            json.dump(self.__dict__, fp, sort_keys=True, indent=2)
