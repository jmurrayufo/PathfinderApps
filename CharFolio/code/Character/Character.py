
from ..Helpers.Maths import ab_mod
from ..Skill.Skill import Skill

import numpy as np

class Character:
    def __init__(self, **kwargs):
        if "json_str" in kwargs:
            # Load from JSON
            pass
        elif "file" in kwargs:
            # Attempt to load from file (assumed to be JSON)
            pass
        else:
            self.name = kwargs.get("name","NO NAME")
            self.classes = {}
            self.equipment = []
            self.feats = []
            self.skills = {}
            for skill in Skill.LOOKUP:
                self.skills[skill] = Skill(skill)
            self._STR = kwargs.get("STR",10)
            self._DEX = kwargs.get("DEX",10)
            self._CON = kwargs.get("CON",10)
            self._INT = kwargs.get("INT",10)
            self._WIS = kwargs.get("WIS",10)
            self._CHA = kwargs.get("CHA",10)


    def __repr__(self):
        ret_val = ""
        ret_val += "Character("
        ret_val += f"name={self.name},"
        ret_val += ")"
        return ret_val


    def card(self, level=1):
        """Return a string to display the character pretty like.
        level controls the amount of detail
            1: Minimal imformation (combat card)
            2: Some detail
            3: Full detail
        """
        ret_val = ""
        ret_val += f"Name: {self.name}"
        if hasattr(self,"level"):
            ret_val += f" Level {self.level}"
        if level >= 2:
            ret_val += "\n  Ability Scores"
            ret_val += f"\n    STR: {self.STR:2} [{str(self.STR_mod):+>2}]"
            ret_val += f"\n    DEX: {self.DEX:2} [{str(self.DEX_mod):+>2}]"
            ret_val += f"\n    CON: {self.CON:2} [{str(self.CON_mod):+>2}]"
            ret_val += f"\n    INT: {self.INT:2} [{str(self.INT_mod):+>2}]"
            ret_val += f"\n    WIS: {self.WIS:2} [{str(self.WIS_mod):+>2}]"
            ret_val += f"\n    CHA: {self.CHA:2} [{str(self.CHA_mod):+>2}]"
        if True:
            ret_val += "\n  Combat"
            ret_val += "\n    AC: 10"
        return ret_val


    def save(self, _file):
        """Save object to file. Will overwite if it exists.
        """
        pass


    def load(self, _file):
        """load object from file.
        """
        pass


    @property
    def STR(self):
        return self._STR
        # TODO: Calculate effects of equipment
    @property
    def STR_mod(self):
        return ab_mod(self.STR)

    @property
    def DEX(self):
        return self._DEX
        # TODO: Calculate effects of equipment
    @property
    def DEX_mod(self):
        return ab_mod(self.DEX)

    @property
    def CON(self):
        return self._CON
        # TODO: Calculate effects of equipment
    @property
    def CON_mod(self):
        return ab_mod(self.CON)

    @property
    def INT(self):
        return self._INT
        # TODO: Calculate effects of equipment
    @property
    def INT_mod(self):
        return ab_mod(self.INT)

    @property
    def WIS(self):
        return self._WIS
        # TODO: Calculate effects of equipment
    @property
    def WIS_mod(self):
        return ab_mod(self.WIS)

    @property
    def CHA(self):
        return self._CHA
        # TODO: Calculate effects of equipment
    @property
    def CHA_mod(self):
        return ab_mod(self.CHA)


    # Random Generation Functions
    def roll_stats(self, method='3d6'):
        """Roll random stats for character
        method picks the means of stats chosen
            '3d6': Roll 3d6 and use them for stats
            '4d6d1': Roll 4d6 and drop the lowest
            '4d6b3': Alias to 3d6d1
        """
        for stat in ['_STR','_DEX','_CON','_INT','_WIS','_CHA']:
            randint = np.random.randint
            if method == '3d6':
                value = randint(1,7)+randint(1,7)+randint(1,7)
            elif method in ['4d6d1','4d6b3']:
                results = []
                for i in range(4):
                    results.append(randint(1,7))
                value = sum(sorted(results,reverse=True)[:3])

            setattr(self,stat,value)



    def generate(self):
        raise NotImplementedError("This must be subclassed")
