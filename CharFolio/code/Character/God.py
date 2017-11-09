
import logging

from . import Character, Fighter

class God:
    """Manage the creation of characters
    """
    logger = logging.getLogger("charFolio").getChild(__module__)
    def __init__(self):
        pass


    def load(self,file_):
        """Load a JSON file and return the correct type
        """
        pass