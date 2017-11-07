
import logging

class Bonus:

    logger = logging.getLogger("charFolio").getChild(__module__)

    # This list will provide WARNINGS when a bonus is created that isn't listed. 
    #   This will not mean that we fail to create the bonus, only that we will
    #   warn the user in logs that we aren't sure this is valid.
    VALID_STATS = [
        "STR",
        "DEX",
        "CON",
        "INT",
        "WIS",
        "CHA",
        "AC",
        "ATK",
        "CMD",
        "CMB",]


    # This list will provide WARNINGS when a bonus is created that isn't listed. 
    #   This will not mean that we fail to create the bonus, only that we will
    #   warn the user in logs that we aren't sure this is valid.
    VALID_TYPES = [
        "armor",
        "shield",
    ]

    def __init__(self, value, type_, stat=None, conditions=None, description=None):
        self.conditions = conditions
        self.description = description
        self.stat = stat
        self.type_ = type_
        self.value = value


    def __repr__(self):
        ret_val = ""
        ret_val += f"Bonus({self.value},{self.type_}"
        if self.conditions:
            ret_val += f",\"{self.conditions}\""
        if self.description:
            ret_val += f",\"{self.description}\""
        ret_val += ")"
        return ret_val


    def __add__(self, other):
        if type(other) is BonusSet:
            ret_val = BonusSet(other.bonus_list)
        elif type(other) is Bonus:
            ret_val = BonusSet()
        else:
            raise TypeError(f"Cannot add {type(other)} to Bonus()")

        ret_val.append(self)
        ret_val.append(other)
        return ret_val


class BonusSet:

    logger = logging.getLogger("charFolio").getChild(__module__)

    def __init__(self, bonus_list=None):
        self.bonuses = list()
        if bonus_list is not None:
            for bonus in bonus_list:
                if type(bonus) is not Bonus:
                    raise TypeError(f"Cannot insert {type(bonus)} into BonusSet()!")
                self.append(bonus)


    def append(self, value):
        # Check to make sure we don't have duplicate types!
        self.logger.debug(f"Appending {value}")
        for index, bonus in enumerate(self.bonuses):
            # BonusSets can only hold one type of bonus, check that!
            if value.stat != bonus.stat:
                raise TypeError(f"Cannot insert Bonus() with stat {value.stat} when BonusSet() already has a bonus with a state of {bonus.stat}")
            # If we have two bonuses of the same type, only the highest is taken    
            if value.type_ == bonus.type_ and value.stat == bonus.stat:
                # Should this new bonus replace it?
                if value.value > bonus.value:
                    self.bonuses[index] = value
                return
        self.bonuses.append(value)


    def total(self):
        return sum([x.value for x in self.bonuses])


