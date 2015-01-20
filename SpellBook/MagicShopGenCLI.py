#!/usr/bin/env python

import csv 
import random
import sys
import argparse
import time
import numpy as np
from textwrap import wrap
import os

parser = argparse.ArgumentParser()

parser.add_argument( 
   'num', 
   type=int, 
   default=1,
   metavar='NUM',
   help='Number of Items to generate', 
   nargs='?',
   )

parser.add_argument( 
   'min',
   type=int, 
   default=0, 
   metavar='COST',
   help='Min Cost', 
   nargs='?'
   )

parser.add_argument( 
   'max',
   type=int, 
   default=float('inf'), 
   metavar='COST',
   help='Max Cost', 
   nargs='?'
   )

parser.add_argument( 
   '-d','--discount',
   type=float, 
   default=1.0, 
   metavar='FACTOR',
   help='Percent Discount. All costs are directly multiplied by this. (Default 1.0)'
   )

parser.add_argument(
   "--all",
   action='store_true',
   help='Ignore limit of list and attempt to display ALL items'
   )

parser.add_argument(
   "--short",
   action='store_true',
   help='Shot listings only'
   )

parser.add_argument(
   "--core",
   action='store_true',
   help='Only list items in the core set of books. (PFRPGCore, APG, UM, UC, UE, ARG)'
   )


args = parser.parse_args()


def price_parse( price_string ):
   price_string = price_string.replace('gp','').replace(',','')
   try:
      return int(price_string)
   except (ValueError):
      return None


sourceFilterList = [ 'Ultimate Magic', 'Ultimate Equipment', 'Ultimate Combat', 'Advanced Race Guide',
   'APG', 'PFRPG Core', ]


with open( 'magic_items_full.csv' ) as fp:
   csvreader = csv.DictReader( fp )
   columns = csvreader.fieldnames
   spellDB = []
   for i in csvreader:
      # Append the converted row to the spell DB
      i['Price'] = price_parse(i['Price'])
      if type(i['Price']) == int :
         i['Price'] = int( i['Price'] * args.discount )
      spellDB.append( i )


spellDBFiletered = [ i for i in spellDB if   
   type(i['Price']) == int 
   and i['Price'] <= args.max
   and i['Price'] >= args.min
   ]

if args.core:
   spellDBFiletered = [i for i in spellDBFiletered if i['Source'] in sourceFilterList]

if not args.all:
   if args.num > len(spellDBFiletered):
      args.num = len( spellDBFiletered )
         
   spellDBFiletered = np.random.choice( spellDBFiletered, args.num, False )

spellDBFiletered = sorted( spellDBFiletered, key = lambda x: x['Price'] )

rows, columns = os.popen('stty size', 'r').read().split()

#Name,Aura,CL,Slot,Price,Weight,Description,Requirements,Cost,Group,Source,AL,
#Int,Wis,Cha,Ego,Communication,Senses,Powers,MagicItems,FullText,Destruction,
#MinorArtifactFlag,MajorArtifactFlag,Abjuration,Conjuration,Divination,
#Enchantment,Evocation,Necromancy,Transmutation,AuraStrength,WeightValue,
#PriceValue,CostValue,Languages,BaseItem,LinkText,id,Mythic,LegendaryWeapon,
#Illusion,Universal
count = 0
for i in spellDBFiletered :
   print "\n{Name}".format(**i)
   print "   Aura: {Aura}".format(**i)
   print "   Price: {Price:,}".format(**i)
   print "   Weight: {Weight}".format(**i)
   print "   CL: {CL}".format(**i)
   print "   Slot: {Slot}".format(**i)
   print "   Source: {Source}".format(**i)
   for line in wrap( "   Description: " + i['Description'], width=int(columns)-16, subsequent_indent='                  ' ):
      print line

   if args.all:
      print "  Index: {}".format(count)
   count += 1

   #time.sleep(0.01)
