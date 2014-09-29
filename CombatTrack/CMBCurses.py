#!/usr/bin/env python

import curses
from curses.wrapper import wrapper
import time
import json
import os
from common import Player, DeltaTruncate
from datetime import timedelta
from datetime import datetime

UpdateRate = 0.25

def Main( window ):
   # This application will parse a given local file, and then display a combat 
   # status screen to the user as a refresh rate of at LEAST 1/Hz. This refresh 
   # rate can be adjusted as needed.
   curses.start_color()   
   curses.use_default_colors()
   curses.init_pair(1,curses.COLOR_RED,-1)

   while ( True ):
      maxX,maxY = window.getmaxyx()
      # os.system('clear')
      PlayerList = []
      try:
         with open(".playerdata.json",'r') as fp:
            try:
               tmp = json.load(fp)
            except ValueError:
               window.clear( )
               window.addstr( 0, 0, "JSON Object is currently corrupt..." )
               window.refresh( )
               time.sleep( 0.1 )
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
               PlayerList[-1].Status = i['Status']
      except IOError:
         window.clear()
         window.addstr(1,1, "The player data hidden file ('.playerdata.json') does not apear in this directory" )
         window.addstr(2,1,"Please wait...." )
         window.refresh()
         time.sleep(1)
         continue

      PlayerList.sort( key = lambda x: x.Initiative, reverse = True )

      totalTime = timedelta( 0 )
      for i in PlayerList:
         totalTime += i.SoftUpdate()

      if ( totalTime.total_seconds() < 1 ):
         totalTime = timedelta( seconds = 1 )

      window.addstr(0,0, "Index Active     Name     Init   Time    TimePer AvgTurn Turns Status" )
      y = 1
      for idx,val in enumerate( PlayerList ):
         # Get player dict to parse out!
         pDict = val.GetStrDict( totalTime )
         window.addstr( y, 0, ' [{0:2.0f}] {Active:6} {Name:^12} ({Init:2.0f})  {TTime} ({PTime:6.2%}) {ATime} {Turns:^5} {1}'.format( idx+1, PrettyStatus( pDict['Status'] ), **pDict ) )
         # Check to see if we are the active player, and highlight to bring attention if we are!
         if len( pDict['Active'] ) :
            window.chgat( y, 0, maxY, curses.color_pair( 1 ) )
            # window.chgat( y, 6, 3, curses.A_BOLD | curses.color_pair( 1 ) )
            for x in range(13,25):
               if ( window.inch( y, x ) & 0xFF ) != ( ord(' ') & 0xFF ) :
                  window.chgat( y, x, 1, curses.A_BOLD | curses.color_pair( 1 ) )

         y += 1
      y += 1
      window.addstr( y, 0, "Total Time: {}".format( DeltaTruncate( totalTime ) ) )
      window.refresh( )
      window.clear( )
      # Should be fast enough to see like instant input from the output screen!
      time.sleep( UpdateRate )

def PrettyStatus( statusDict ):
   if len( statusDict ) == 0 :
      return ""
   
   retStr = ""
   for i in statusDict :
      if len( retStr ) :
         retStr += ", "
      retStr += i
      retStr += " ["
      retStr += str( statusDict[i] )
      retStr += "]"
      pass
   return retStr


wrapper(Main)

print curses.COLORS

print "Fin"
