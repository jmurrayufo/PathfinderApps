

class Bonus:

    def __init__(self, value, _type, conditions=None, description=None):
        self.value = value
        self._type = _type
        self.conditions = conditions
        self.description = description

    def __repr__(self):
        ret_val = ""
        ret_val += f"Bonus({self.value},{self._type}"
        if self.conditions:
            ret_val += f",\"{self.conditions}\""
        if self.description:
            ret_val += f",\"{self.description}\""
        ret_val += ")"


