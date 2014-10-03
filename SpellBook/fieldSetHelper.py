#!/usr/bin/env python

import csv

targetColoumn = 'wiz'

with open( 'spell_full.csv' ) as fp:
   csvreader = csv.DictReader( fp )
   columns = csvreader.fieldnames
   spellDB = []
   for i in csvreader:
      # Append the converted row to the spell DB
      spellDB.append( i )

sourceFilterList = [ 'Ultimate Magic', 'Ultimate Combat', 'Advanced Race Guide',
   'APG', 'PFRPG Core', ]

spellDBFiletered = [ i for i in spellDB if i['source'] in sourceFilterList ]

print "Coloums:"
for field in columns:

   Results = set()

   for row in spellDBFiletered :
      # print row
      Results.add( row[field] )

   for i in Results:
      print " " + i

   print "FIELD TYPE:",field
   raw_input("next...")
