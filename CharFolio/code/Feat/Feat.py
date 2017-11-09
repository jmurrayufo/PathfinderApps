
import os
from pathlib import Path
import json

class Feat:
    FEATS_DICT = {}
    library_dir = Path(os.path.dirname(__file__)+"/../library/feats/")

    for feat in library_dir.glob("*.json"):
        FEATS_DICT[feat.stem] = feat



    def __init__(self, name):
        """Given a feat name, lookup and populate from the library
        """
        if name not in Feat.FEATS_DICT:
            raise KeyError(f"{name} is not a valid feat. Check spelling?")