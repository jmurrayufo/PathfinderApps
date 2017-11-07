
import logging
import json

from . import Item

class Weapon(Item.Item):

    logger = logging.getLogger("charFolio").getChild(__module__)

    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.critical = kwargs.get("critical","x2")
        self.damage = kwargs.get("damage","???")
        self.damage_type = kwargs.get("damage_type","?")
        self.double_weapon = kwargs.get("double_weapon",False)
        self.hands = kwargs.get("hands",1)
        self.range = kwargs.get("range",None)
        self.size = kwargs.get("size","M")
        self.special = kwargs.get("special",None)
        self.use_str_mod = kwargs.get("use_str_mod",True)


    def save(self, file_):
        with open(file_,'w') as fp:
            json.dump(self.__dict__, fp, sort_keys=True, indent=2)





