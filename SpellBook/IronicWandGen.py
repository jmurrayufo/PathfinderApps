#!/usr/bin/env python

import csv 
import random

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

spellDBFiletered = [ i for i in spellDB if ( i[ 'source' ] in sourceFilterList and i[ randClass ] in ['1','2','3','4'] ) ]

selection = random.sample( spellDBFiletered, 2)

print "Class: {}".format( randClass )
for i in selection :
   print i['name'],"[SL:{}]".format( i[randClass])
   print " ",i['short_description']
   print
