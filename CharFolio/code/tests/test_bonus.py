
import unittest

from ..Bonus.Bonus import Bonus

class Bonuses(unittest.TestCase):


    def test_bonus_addition1(self):
        x = Bonus(2,"shield","AC")
        y = Bonus(1,"armor","AC")
        z = y+x
        self.assertEqual(z.total(),3,f"Got {z.total()}")


    def test_bonus_addition2(self):
        x = Bonus(2,"shield","AC")
        y = Bonus(1,"shield","AC")
        z = y+x
        self.assertEqual(z.total(),2,f"Got {z.total()}")


    def test_bonus_addition3(self):
        with self.assertRaises(TypeError,msg="Adding ints to a Bonus() breaks checking"):
            x = Bonus(2,"shield","AC")
            z = x+1


    def test_bonus_type_assert(self):
        with self.assertRaises(TypeError,msg="Adding different bonus stats should fail"):
            x = Bonus(2,"shield","AC")
            y = Bonus(1,"MISC","ATK")
            x+y

