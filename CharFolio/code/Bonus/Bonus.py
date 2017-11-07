

class Bonus:

    def __init__(self, value, type_, conditions=None, description=None):
        self.value = value
        self.type_ = type_
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


