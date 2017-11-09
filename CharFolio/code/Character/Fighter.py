
import logging

from . import Character

class Warrior(Character.Character):

    logger = logging.getLogger("charFolio").getChild(__module__)

    STATS_PREFERENCE = ['_STR','_DEX','_CON','_INT','_WIS','_CHA']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.class_ = 'warrior'

    def generate(self, method='3d6'):
        stats_line = self.get_stats_line(method)

        stats_line = sorted(stats_line, reverse=True)
        print(f"Got stats: {stats_line}")
        for index,stat in enumerate(Warrior.STATS_PREFERENCE):
            setattr(self,stat,stats_line[index])