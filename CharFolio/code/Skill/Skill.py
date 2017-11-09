import logging 

class Skill:

    logger = logging.getLogger("charFolio").getChild(__module__)
    LOOKUP = {
        # Skill: [Untrained, Ability, AC Penalty]
        "Acrobatics":[True,"DEX",True],
        "Appraise":[True,"INT",False],
        "Bluff":[True,"CHA",False],
        "Climb":[True,"STR",True],
        "Craft":[True,"INT",False],
        "Diplomacy":[True,"CHA",False],
        "Disable Device":[False,"DEX",True],
        "Disguise":[True,"CHA",False],
        "Escape Artist":[True,"DEX",True],
        "Fly":[True,"DEX",True],
        "Handle Animal":[False,"CHA",False],
        "Heal":[True,"WIS",False],
        "Intimidate":[True,"CHA",False],
        "Knowledge (arcana)":[False,"INT",False],
        "Knowledge (dungeoneering)":[False,"INT",False],
        "Knowledge (engineering)":[False,"INT",False],
        "Knowledge (geography)":[False,"INT",False],
        "Knowledge (history)":[False,"INT",False],
        "Knowledge (local)":[False,"INT",False],
        "Knowledge (nature)":[False,"INT",False],
        "Knowledge (nobility)":[False,"INT",False],
        "Knowledge (planes)":[False,"INT",False],
        "Knowledge (religion)":[False,"INT",False],
        "Linguistics":[False,"INT",False],
        "Perception":[True,"WIS",False],
        "Perform":[True,"CHA",False],
        "Profession":[False,"WIS",False],
        "Ride":[True,"DEX",True],
        "Sense Motive":[True,"WIS",False],
        "Sleight of Hand":[False,"DEX",True],
        "Spellcraft":[False,"INT",False],
        "Stealth":[True,"DEX",True],
        "Survival":[True,"WIS",False],
        "Swim":[True,"STR",True],
        "Use Magic Device":[False,"CHA",False],}

    def __init__(self,name,**kwargs):
        self.name = name
        if name not in Skill.LOOKUP: raise KeyError(f"{name} not in lookup table!")
        self.untrained = Skill.LOOKUP[name][0]
        self.ability = Skill.LOOKUP[name][1]
        self.ac_penalty = Skill.LOOKUP[name][2]

        self.description = kwargs.get("description","")
        self.ranks = kwargs.get("ranks",0)


    def __repr__(self):
        return f"Skill({self.name},ranks={self.ranks})"  

    def __str__(self):
        return f"{self.name} - {self.ability} (Ranks: {self.total()})"


    def total(self, parent=None):
        """Return total skill check
        """
        # TODO Handle racial bonus
        # TODO Handle feat bonus        
        # TODO Handle item bonus
        if parent:
            raise NotImplementedError

        return self.ranks


