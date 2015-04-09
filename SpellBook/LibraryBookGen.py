#!/usr/bin/env python

import csv 
import random
import numpy as np
import textwrap

sourceFilterList = [ 'Ultimate Magic', 'Ultimate Combat', 'Advanced Race Guide',
   'APG', 'PFRPG Core', ]

playerLevel = 10

townCrapFactor = 0.4

spellPerLevel =  5
spellPerLevel *= townCrapFactor 

johnsSpellRequests = []

"""
Adding Spells to a Wizard's Spellbook

Wizards can add new spells to their spellbooks through several methods. A wizard can only learn new spells that belong to the wizard spell lists.

Spells Gained at a New Level: Wizards perform a certain amount of spell research between adventures. Each time a character attains a new wizard level, he gains two spells of his choice to add to his spellbook. The two free spells must be of spell levels he can cast.

Spells Copied from Another's Spellbook or a Scroll: A wizard can also add a spell to his book whenever he encounters one on a magic scroll or in another wizard's spellbook. No matter what the spell's source, the wizard must first decipher the magical writing (see Arcane Magical Writings). Next, he must spend 1 hour studying the spell. At the end of the hour, he must make a Spellcraft check (DC 15 + spell's level). A wizard who has specialized in a school of spells gains a +2 bonus on the Spellcraft check if the new spell is from his specialty school. If the check succeeds, the wizard understands the spell and can copy it into his spellbook (see Writing a New Spell into a Spellbook). The process leaves a spellbook that was copied from unharmed, but a spell successfully copied from a magic scroll disappears from the parchment.

If the check fails, the wizard cannot understand or copy the spell. He cannot attempt to learn or copy that spell again until one week has passed. If the spell was from a scroll, a failed Spellcraft check does not cause the spell to vanish.

In most cases, wizards charge a fee for the privilege of copying spells from their spellbooks. This fee is usually equal to half the cost to write the spell into a spellbook (see Writing a New Spell into a Spellbook). Rare and unique spells might cost significantly more.

Independent Research: A wizard can also research a spell independently, duplicating an existing spell or creating an entirely new one. The cost to research a new spell, and the time required, are left up to GM discretion, but it should probably take at least 1 week and cost at least 1,000 gp per level of the spell to be researched. This should also require a number of Spellcraft and Knowledge (arcana) checks.
"""

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
   random.randint( 0, expectedSpellsPerLevel[8] ), # Level 9 (max 43)
]

# Force each level to have at LEAST the minimum number of spells
for idx,val in enumerate( levelAmounts ) :
   if (idx+1)*2-1 <= playerLevel and val < spellPerLevel :
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
