#!/usr/bin/env python

import csv 
import random
import numpy as np

sourceFilterList = [ 'Ultimate Magic', 'Ultimate Combat', 'Advanced Race Guide',
   'APG', 'PFRPG Core', ]

playerLevel = 10

townCrapFactor = 1.0

spellPerLevel =  5 * townCrapFactor 

levelAmounts = [
   random.randint(0, int( max(0, (playerLevel -  0) * spellPerLevel ) ) ), # Level 1 (max 112)
   random.randint(0, int( max(0, (playerLevel -  2) * spellPerLevel ) ) ), # Level 2 (max 135)
   random.randint(0, int( max(0, (playerLevel -  4) * spellPerLevel ) ) ), # Level 3 (max 117)
   random.randint(0, int( max(0, (playerLevel -  6) * spellPerLevel ) ) ), # Level 4 (max 100)
   random.randint(0, int( max(0, (playerLevel -  8) * spellPerLevel ) ) ), # Level 5 (max 89)
   random.randint(0, int( max(0, (playerLevel - 10) * spellPerLevel ) ) ), # Level 6 (max 74)
   random.randint(0, int( max(0, (playerLevel - 12) * spellPerLevel ) ) ), # Level 7 (max 66)
   random.randint(0, int( max(0, (playerLevel - 14) * spellPerLevel ) ) ), # Level 8 (max 47)
   random.randint(0, int( max(0, (playerLevel - 16) * spellPerLevel ) ) ), # Level 9 (max 43)
]

with open( 'spell_full.csv' ) as fp:
   csvreader = csv.DictReader( fp )
   columns = csvreader.fieldnames
   spellDB = []
   for i in csvreader:
      # Append the converted row to the spell DB
      if i['source'] in [ 'PFRPG Core', 'APG' ] :
         i['weight'] = 2
      elif i['source'] in sourceFilterList :
         i['weight'] = 1
      else:
         i['weight'] = 0.05
      spellDB.append( i )

spellDBFiltered = [ i for i in spellDB if ( i[ 'wiz' ] != 'NULL' ) ]

for idx,numberOfSpells in enumerate( levelAmounts ) :
   if numberOfSpells == 0:
      continue
   idx += 1
   print "Spells at Level {} => {}".format( idx, numberOfSpells  )
   subSpellDBFiltered = [ x for x in spellDBFiltered if x['wiz'] == str(idx)]
   # spells = sorted( random.sample( subSpellDBFiltered, numberOfSpells ), key = lambda x: x['name'] )
   p = np.array( [ x['weight'] for x in subSpellDBFiltered ] )
   p /= sum( p )
   spells = sorted( np.random.choice( subSpellDBFiltered, numberOfSpells, False, p=p ), key=lambda x: x['name'] )
   for spell in spells :
      print "   Name: {name}".format( **spell )
      print "      Short Description: {short_description}".format( **spell )
      print "      Level: {wiz}".format( **spell )
      print "      Source: {source}".format( **spell )
      print

print "Total Spells: {}".format( sum( levelAmounts ) )

