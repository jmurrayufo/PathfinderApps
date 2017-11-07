
import logging

class Item:

    logger = logging.getLogger("charFolio").getChild(__module__)

    def __init__(self, name=None, description="", value=0, weight=0, amount=1, 
                json_str=None, file_=None, equiped=False, muled=False):
        if json_str:
            # TODO
            raise NotImplementedError
        elif file_:
            # TODO
            raise NotImplementedError
        else:
            self.name = name
            self.description = description
            self.value = value
            self.weight = weight
            self.amount = amount
            self.equiped = equiped
            self.muled = muled


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