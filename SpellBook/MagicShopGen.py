#!/usr/bin/env python

import csv 
import random
import sys
import argparse

parser = argparse.ArgumentParser()

parser.add_argument( 
   'numSpells', 
   type=int, 
   default=1,
   metavar='NUM',
   help='Test!\nAnd more!', 
   nargs='?',
   )

parser.add_argument( 
   '--level', '-l',
   type=int, 
   default=4, 
   metavar='NUM',
   help='Current Party level', 
   )

args = parser.parse_args()

#print args

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

with open( 'spell_full.csv' ) as fp:
   csvreader = csv.DictReader( fp )
   columns = csvreader.fieldnames
   spellDB = []
   for i in csvreader:
      # Append the converted row to the spell DB
      spellDB.append( i )


for i in spellDB:
   try:
      i['SLA_Level'] = int( i['SLA_Level'] )
   except (ValueError):
      i['SLA_Level'] = -1

spellDBFiletered = [ i for i in spellDB if 
   i[ 'source' ] in sourceFilterList and 
   i['SLA_Level'] <= args.level ]


selection = random.sample( spellDBFiletered, args.numSpells )

selection = sorted( selection, key = lambda x: (x['SLA_Level'],x['name']) )

for i in selection :
   print "\n{name}".format(**i)
   print "   Spell Level: {spell_level}".format(**i)
   print "   Description: {short_description}".format(**i)
