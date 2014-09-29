#!/usr/bin/env python

import json
import time
import os
from common import Player, DeltaTruncate
from datetime import timedelta
from datetime import datetime

# This application will parse a given local file, and then display a combat 
# status screen to the user as a refresh rate of at LEAST 1/Hz. This refresh 
# rate can be adjusted as needed.

while ( True ):
   os.system('clear')
   PlayerList = []
   try:
      with open(".playerdata.json",'r') as fp:
         try:
            tmp = json.load(fp)
         except ValueError:
            print "JSON Object is currently corrupt..."
            time.sleep(1)
            continue
         for i in tmp:
            PlayerList.append(Player())
            PlayerList[-1].Name = i['Name']
            PlayerList[-1].Active = i['Active']
            PlayerList[-1].Initiative = i['Initiative']
            PlayerList[-1].TimeTaken = timedelta( seconds = float( i['TimeTaken'] ) )
            PlayerList[-1].TurnStart = i['TurnStart']
            if( i['TurnStart'] ):
               PlayerList[-1].TurnStart = datetime.strptime( i['TurnStart'] , "%Y-%m-%dT%H:%M:%S.%f")
            PlayerList[-1].Turns = i['Turns']
   except IOError:
      print "The player data hidden file ('.playerdata.json') does not apear in this directory"
      print "Please wait...."
      time.sleep(1)
      continue

   PlayerList.sort( key = lambda x: x.Initiative, reverse = True )

   totalTime = timedelta( 0 )
   for i in PlayerList:
      totalTime += i.SoftUpdate()

   if ( totalTime.total_seconds() < 1 ):
      totalTime = timedelta( seconds = 1 )
   print "Index Active         Name Init     Time  TimePer AvgTurn Turns"
   for idx,val in enumerate( PlayerList ):
      print " [%2d]"%(idx+1),val.GetStr( totalTime )
   print "Total Time:",DeltaTruncate( totalTime )


   time.sleep(1/5.)
