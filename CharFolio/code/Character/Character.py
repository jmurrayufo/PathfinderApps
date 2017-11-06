

class Character:
    def __init__(self, **kwargs):
        if "json" in kwargs:
            # Load from JSON
            pass
        elif "file" in kwargs:
            # Attempt to load from file (assumed to be JSON)
            pass
        else:
            self.name = kwargs.get("name","NO NAME")
            self.classes = {}
            self.equipment = []


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
        return ret_val


    def save(self, _file):
        """Save object to file. Will overwite if it exists.
        """
        pass


    def load(self, _file):
        """load object from file.
        """
        pass
