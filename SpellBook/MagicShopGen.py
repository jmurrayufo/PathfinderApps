#!/usr/bin/env python

import csv 
import random
import sys

sourceFilterList = [ 'Ultimate Magic', 'Ultimate Combat', 'Advanced Race Guide',
   'APG', 'PFRPG Core', ]

classes = [ 
      'sor',
      'wiz',
      'cleric',
      'druid',
      'ranger',
      'bard',
      'paladin',
      'alchemist',
      'summoner',
      'witch',
      'inquisitor',
      'oracle',
      'antipaladin',
      'magus',
   ]

randClass = random.choice( classes ) 

with open( 'spell_full.csv' ) as fp:
   csvreader = csv.DictReader( fp )
   columns = csvreader.fieldnames
   spellDB = []
   for i in csvreader:
      # Append the converted row to the spell DB
      spellDB.append( i )

spellDBFiletered = [ i for i in spellDB if i[ 'source' ] in sourceFilterList ]

try:
   selection = random.sample( spellDBFiletered, int(sys.argv[1]) )
except (IndexError) :
   selection = random.sample( spellDBFiletered, 1 )

for i in selection :
   print "\n{name}".format(**i)
   print "   Spell Level: {spell_level}".format(**i)
   print "   Description: {short_description}".format(**i)
