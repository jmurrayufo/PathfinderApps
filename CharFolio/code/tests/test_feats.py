
import unittest

from .. import Feat

class Feats(unittest.TestCase):


    def test_feat_init(self):
        for feat_name in Feat.FEATS_DICT:
            x = Feat(feat_name)