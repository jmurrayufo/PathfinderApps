

class Character:
    def __init__(self,**kwargs):
        self.name = kwargs.get("name","NO NAME")

    def __repr__(self):
        ret_val = ""
        ret_val += "Character("
        ret_val += f"name={self.name},"
        ret_val += ")"
        return ret_val
