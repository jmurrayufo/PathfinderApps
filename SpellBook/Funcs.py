import numpy as np
from scipy.interpolate import interp1d


"""
Player, NPC, Powerful NPC
"""
GoldList = [
   [    100,    260,    390 ],
   [   1000,    390,    780 ],
   [   3000,    780,   1650 ],
   [   6000,   1650,   2400 ],
   [  10500,   2400,   3450 ],
   [  16000,   3450,   4650 ],
   [  23500,   4650,   6000 ],
   [  33000,   6000,   7800 ],
   [  46000,   7800,  10050 ],
   [  62000,  10050,  12750 ],
   [  82000,  12750,  16350 ],
   [ 108000,  16350,  21000 ],
   [ 140000,  21000,  27000 ],
   [ 185000,  27000,  34800 ],
   [ 240000,  34800,  45000 ],
   [ 315000,  45000,  58500 ],
   [ 410000,  58500,  75000 ],
   [ 530000,  75000,  96000 ],
   [ 685000,  96000, 123000 ],
   [ 880000, 123000, 159000 ],
   ]
"""
Slow, Medium, Fast
"""
XPList = [
   [       0,       0,       0 ],
   [    3000,    2000,    1300 ],
   [    7500,    5000,    3300 ],
   [   14000,    9000,    6000 ],
   [   23000,   15000,   10000 ],
   [   35000,   23000,   15000 ],
   [   53000,   35000,   23000 ],
   [   77000,   51000,   34000 ],
   [  115000,   75000,   50000 ],
   [  160000,  105000,   71000 ],
   [  235000,  155000,  105000 ],
   [  330000,  220000,  145000 ],
   [  475000,  315000,  210000 ],
   [  665000,  445000,  295000 ],
   [  955000,  635000,  425000 ],
   [ 1350000,  890000,  600000 ],
   [ 1900000, 1300000,  850000 ],
   [ 2700000, 1800000, 1200000 ],
   [ 3850000, 2550000, 1700000 ],
   [ 5350000, 3600000, 2400000 ],
   ]

def XPAtLevel( level=1, scale=1 ) :
   return XPList[level][scale]

def XPMinAtLevel( level=1, scale=1) :
   assert( level >= 1 )
   assert( level <= 20 )
   return XPList[level-1][scale]

def PathCurrentWealth( level = 0, scale = 0 ):
   """
   Scale != Slow,Med,Fast! 
   Scale:
      0: PC
      1: NPC (Basic)
      2: NPC (Heroic)
   """
   return GoldList[ level-1 ][ scale ]

def Path_Current_Wealth_Interp( level = 0.0, scale = 0 ):
   """
   Scale != Slow,Med,Fast! 
   Scale:
      0: PC
      1: NPC (Basic)
      2: NPC (Heroic)
   """
   if( level <= 0 ):
      return 0
   
   if( level > 0 and level < 20 ):
      gold = []
      for x in range(20):
         gold.append(GoldList[x][scale])
      f = interp1d( range(1,21), gold, kind='cubic' )
      return float(f(level))

   if( level >= 20 ):
      return GoldList[ 19 ][ scale ]

def PathCurrentLevel( xp=0, scale=1 ):
   """
      xp: Amount of current xp
      Scale: 0, 1 or 2 for Slow, Medium, and Fast Progression
   """

   for idx,val in enumerate( XPList ):
      if( xp < val[ scale ] ):
         break

   else:
      idx = 20

   return idx

def Path_Float_Current_Level( xp=0, scale=1 ):
   if( xp <= 0 ):
      return 1.0

   for idx,val in enumerate( XPList ):
      if( xp < val[ scale ] ):
         break
   else:
      idx = 20

   return idx + 1 - float( XPList[idx][scale] - xp  ) / float( XPList[idx][scale] - XPList[idx-1][scale] )


def XPToLevelUp( xp, scale = 1 ):
   for idx,val in enumerate( XPList ):
      if( xp < val[ scale ] ):
         break
   else:
      return 0
   # Find Current XP amount
   return XPList[ idx ][scale] - xp

def CalcEncounterXP( CR, numCreatures = 1, partySize = 4,  ):
   """
   Calculate the expected XP from an encounter
   """
   assert( CR <= 25 )

   if( numCreatures == 1 ):
      pass
   elif( numCreatures == 2 ):
      CR += 2
   elif( numCreatures == 3 ):
      CR += 3
   elif( numCreatures == 4 ):
      CR += 4
   elif( numCreatures == 6 ):
      CR += 5
   elif( numCreatures == 8 ):
      CR += 6
   elif( numCreatures == 12 ):
      CR += 7
   elif( numCreatures == 16 ):
      CR += 8

   CROffsetTable = [
      0.125, 0.1666666667, 0.25, 0.3333333333, 0.5, 1, 2, 3, 4, 5, 6, 7, 8, 9, 
      10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25,
      ]
   rewardIndex = 0
   while( CR > CROffsetTable[rewardIndex] ):
      rewardIndex += 1

   XPRewardsTable = [
      50, 65, 100, 135, 200, 400, 600, 800, 1200, 1600, 2400, 3200, 4800, 6400, 
      9600, 12800, 19200, 25600, 38400, 51200, 76800, 102400, 153600, 204800, 
      307200, 409600, 614400, 819200, 1228800, 1638400,
      ]

   return XPRewardsTable[ rewardIndex ]

def CR( level, partySize = 4 ):
   if( level == 1/8. ):
      return 50 / partySize
   if( level == 1/6. ):
      return 65 / partySize
   if( level == 1/4. ):
      return 100 / partySize
   if( level == 1/3. ):
      return 135 / partySize
   if( level == 1/2. ):
      return 200 / partySize
   if( level > 25 ):
      return 1638400 / partySize

   tmp = [ 0, 400, 600, 800, 1200, 1600, 2400, 3200, 4800, 6400, 9600, 12800, 
      19200, 25600, 38400, 51200, 76800, 102400, 153600, 204800, 307200,
      409600, 614400, 819200, 1228800, 1638400 
   ]

   return tmp[ level ] / partySize

def Score_To_Mod( score ):
   return score/2-5

def Minimum_Caster_Level( level, class_name ):
   scale_dict = {
      "adept":[1,1,4,7,10,13,16],
      "alchemist":[1,1,4,7,10,13,16],
      "antipaladin":[1,4,7,10,13],
      "bard":[1,1,4,7,10,13,16],
      "cleric/oracle":[1,1,3,5,7,9,11,13,15,17],
      "cleric":[1,1,3,5,7,9,11,13,15,17],
      "druid":[1,1,3,5,7,9,11,13,15,17],
      "inquisitor":[1,1,4,7,10,13,16],
      "magus":[1,1,4,7,10,13,16],
      "oracle":[1,1,3,5,7,9,11,13,15,17],
      "paladin":[1,4,7,10,13],
      "ranger":[1,4,7,10,13],
      "sorcerer/wizard":[1,1,3,5,7,9,11,13,15,17],
      "summoner":[1,1,4,7,10,13,16],
      "witch":[1,1,3,5,7,9,11,13,15,17],
      "wizard":[1,1,3,5,7,9,11,13,15,17],
   }
   try:
      return scale_dict[class_name][level]
   except (IndexError):
      return None

def Re_Parse_Spell_Level( inputString ):
   import re

   retString = ""
   for sub_string in inputString.split(','):
      sub_string = sub_string.lstrip().rstrip()
      # print sub_string
      mtch = re.search('([\w/]+) (\d)',sub_string)
      if mtch:
         if len(retString):
            retString += ", "
         retString += mtch.group(1)
         retString += " "
         retString += mtch.group(2)
         retString += " (CL: {})".format(Minimum_Caster_Level( int(mtch.group(2)), mtch.group(1) ))
   return retString

if __name__ == '__main__' :
   test = "cleric/oracle 4, sorcerer/wizard 4"
   print test
   print Re_Parse_Spell_Level( test )
   print "{}".format(None)

   # for i in range(1,21):
   #    print i,Minimum_Caster_Level(i,'bard')