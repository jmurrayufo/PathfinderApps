#!/usr/bin/env python

import csv 
import random
import numpy as np
import textwrap

sourceFilterList = [ 'Ultimate Magic', 'Ultimate Combat', 'Advanced Race Guide',
   'APG', 'PFRPG Core', ]

playerLevel = 5

townCrapFactor = 0.2


spellPerLevel =  5
spellPerLevel *= townCrapFactor 

johnsSpellRequests = []

expectedSpellsPerLevel = [
   min( 20, int( max( 0, ( playerLevel -  0 ) * spellPerLevel ) ) ), # Level 1 (max 112)
   min( 20, int( max( 0, ( playerLevel -  2 ) * spellPerLevel ) ) ), # Level 2 (max 135)
   min( 20, int( max( 0, ( playerLevel -  4 ) * spellPerLevel ) ) ), # Level 3 (max 117)
   min( 20, int( max( 0, ( playerLevel -  6 ) * spellPerLevel ) ) ), # Level 4 (max 100)
   min( 20, int( max( 0, ( playerLevel -  8 ) * spellPerLevel ) ) ), # Level 5 (max 89)
   min( 20, int( max( 0, ( playerLevel - 10 ) * spellPerLevel ) ) ), # Level 6 (max 74)
   min( 20, int( max( 0, ( playerLevel - 12 ) * spellPerLevel ) ) ), # Level 7 (max 66)
   min( 20, int( max( 0, ( playerLevel - 14 ) * spellPerLevel ) ) ), # Level 8 (max 47)
   min( 20, int( max( 0, ( playerLevel - 16 ) * spellPerLevel ) ) ), # Level 9 (max 43)
]

levelAmounts = [
   random.randint( 0, expectedSpellsPerLevel[0] ), # Level 1 (max 112)
   random.randint( 0, expectedSpellsPerLevel[1] ), # Level 2 (max 135)
   random.randint( 0, expectedSpellsPerLevel[2] ), # Level 3 (max 117)
   random.randint( 0, expectedSpellsPerLevel[3] ), # Level 4 (max 100)
   random.randint( 0, expectedSpellsPerLevel[4] ), # Level 5 (max 89)
   random.randint( 0, expectedSpellsPerLevel[5] ), # Level 6 (max 74)
   random.randint( 0, expectedSpellsPerLevel[6] ), # Level 7 (max 66)
   random.randint( 0, expectedSpellsPerLevel[7] ), # Level 8 (max 47)
   random.randint( 0, expectedSpellsPerLevel[8] ), # Level 8 (max 43)
]

# Force each level to have at LEAST the minimum number of spells
for idx,val in enumerate( levelAmounts ) :
   if val and val < spellPerLevel :
      levelAmounts[idx] = int( spellPerLevel )

spellCopyCosts = [
     7.5,
    15,
    60,
   135,
   240,
   375,
   540,
   735,
   960,
  1215,
]

with open( 'spell_full.csv' ) as fp:
   csvreader = csv.DictReader( fp )
   columns = csvreader.fieldnames
   spellDB = []
   for i in csvreader:
      
      if i['name'] in johnsSpellRequests :
         i['weight'] = 4
      elif i['source'] in [ 'PFRPG Core' ] :
         i['weight'] = 3
      elif i['source'] in [ 'APG' ] :
         i['weight'] = 2
      elif i['source'] in sourceFilterList :
         i['weight'] = 1
      else:
         i['weight'] = 0.15
      try:
         # Offset by one to get correct index!
         i['copy_cost'] = spellCopyCosts[ int( i['wiz'] ) - 1 ]
         
         if i['source'] not in sourceFilterList :
            i['copy_cost'] *= 3
      except (ValueError) :
         continue

      # Append the converted row to the spell DB
      spellDB.append( i )

# This check is now done in the open block above!
spellDBFiltered = [ i for i in spellDB if ( i[ 'wiz' ] != 'NULL' ) ]

try :
   rows, columns = os.popen('stty size', 'r').read().split()
   columns = int( columns ) - 5
except :
   columns = 80


for idx,numberOfSpells in enumerate( levelAmounts ) :
   if numberOfSpells == 0:
      continue
   idx += 1
   print "\n== Spells at Level {} => {} ==".format( idx, numberOfSpells  )
   subSpellDBFiltered = [ x for x in spellDBFiltered if x['wiz'] == str(idx)]

   p = np.array( [ x['weight'] for x in subSpellDBFiltered ] )
   # p /= sum( p ) doesn't work, even with a forced float value? Not sure why....
   p = p / float( sum( p ) )
   spells = sorted( 
      np.random.choice( 
         subSpellDBFiltered, 
         numberOfSpells, 
         False, 
         p=p 
         ), 
      key=lambda x: x['name'] 
      )
   for spell in spells :
      print "   Name: {name}".format( **spell )
      if len( spell['short_description'] ) :
         spellDes = textwrap.wrap( 
            text="      Details: {short_description}".format( **spell ),
            width=columns,
            subsequent_indent="                  "
            )
      else:
         spellDes = textwrap.wrap( 
            text="      Details: {description}".format( **spell ),
            width=columns,
            subsequent_indent="                  "
            )

      print "\n".join( spellDes )
      print "      Source: {source}".format( **spell )
      print "      Copy Cost: {copy_cost} gp".format( **spell )
      print

print "Total Spells: {}".format( int( sum( levelAmounts ) ) )

