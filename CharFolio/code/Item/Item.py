
import logging

class Item:

    logger = logging.getLogger("charFolio").getChild(__module__)

    def __init__(self, json_str=None, file_=None, **kwargs):
        if json_str:
            # TODO
            raise NotImplementedError
        elif file_:
            # TODO
            raise NotImplementedError
        else:
            self.amount = kwargs.get("amount", 1)
            self.category = kwargs.get("category", None)
            self.description = kwargs.get("description", None)
            self.equipped = kwargs.get("equipped", False)
            self.muled = kwargs.get("muled", False)
            self.name = kwargs.get("name", None)
            self.value = kwargs.get("value", 0)
            self.weight = kwargs.get("weight", 0)
            self.masterwork = kwargs.get("masterwork", False)


    def __repr__(self):

        ret_val = ""
        ret_val += f"N: {self.name}"

        if self.amount > 1:
            ret_val += f" x{self.amount}"
        elif self.amount == 0:
            return ret_val

        ret_val += f", {self.weight:,.1f} lbs"
        if self.amount > 1:
            ret_val += f" ({self.weight*self.amount:,.1f} lbs)"

        ret_val += f", {self.value:,.0f}gp"
        if self.amount > 1:
            ret_val += f" ({self.value*self.amount:,.0f}gp)"
        return ret_val


    @property
    def weight_total(self):
        return self.weight*self.amount    


    @property
    def value_total(self):
        return self.value*self.amount