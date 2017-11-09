
import logging

from . import Character

class Fighter(Character.Character):

    logger = logging.getLogger("charFolio").getChild(__module__)

    STATS_PREFERENCE = ['_STR','_DEX','_CON','_INT','_WIS','_CHA']

    BAB_LIST = [
        [ 1],
        [ 2],
        [ 3],
        [ 4],
        [ 5],
        [ 6, 1],
        [ 7, 2],
        [ 8, 3],
        [ 9, 4],
        [10, 5],
        [11, 6, 1],
        [12, 7, 2],
        [13, 8, 3],
        [14, 9, 4],
        [15,10, 5],
        [16,11, 6, 1],
        [17,12, 7, 2],
        [18,13, 8, 3],
        [19,14, 9, 4],
        [20,15,10, 5],
    ]

    FORT_SAVE_LIST = [2,3,3,4,4,5,5,6,6,7,7,8,8,9,9,10,10,11,11,12,]
    REF_SAVE_LIST = [0,0,1,1,1,2,2,2,3,3,3,4,4,4,5,5,5,6,6,6,]
    WILL_SAVE_LIST = [0,0,1,1,1,2,2,2,3,3,3,4,4,4,5,5,5,6,6,6,]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.class_ = 'warrior'

    def generate(self, method='3d6', level=1):
        stats_line = self.get_stats_line(method)

        stats_line = sorted(stats_line, reverse=True)
        print(f"Got stats: {stats_line}")
        for index,stat in enumerate(Fighter.STATS_PREFERENCE):
            setattr(self,stat,stats_line[index])