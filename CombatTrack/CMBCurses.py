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

   # This set seems to be needed to get color working?
   # TODO: Isolate what is needed here. Remove uneeded and document it
   curses.start_color()   
   curses.use_default_colors()
   curses.init_pair(1,curses.COLOR_RED,-1)

   # Allow for off screen scrolling (Ugly, but saves from crash!)
   window.scrollok(1)
   window.idlok(1)

   while ( True ):
      maxX,maxY = window.getmaxyx()
      PlayerList = []

      # Try to parse the player data file
      try:
         with open(".playerdata.json",'r') as fp:

            # Attempt to treat the object like a valid json object
            try:
               tmp = json.load(fp)

            # Exception normall occurs when the user is writing to the file. 
            #  We can just wait for this to finish before trying again (0.1)
            except ValueError:
               window.clear()
               window.addstr( 0, 0, "JSON Object is currently corrupt..." )
               window.refresh()
               time.sleep( 0.1 )
               continue

            # Good JSON object found, parse the contents.    
            for i in tmp:
               PlayerList.append(Player())
               PlayerList[-1].Name = i['Name']
               PlayerList[-1].Active = i['Active']
               PlayerList[-1].Initiative = i['Initiative']
               PlayerList[-1].TimeTaken = timedelta( seconds = float( i['TimeTaken'] ) )
               PlayerList[-1].TurnStart = i['TurnStart']
               # If saves us a try, except pair. Not ver pythonic....
               if( i['TurnStart'] ):
                  PlayerList[-1].TurnStart = datetime.strptime( i['TurnStart'] , "%Y-%m-%dT%H:%M:%S.%f")
               PlayerList[-1].Turns = i['Turns']
               PlayerList[-1].Status = i['Status']

      # if we cannot parse that file, then we need to tell the user and wait!
      except IOError:
         window.clear()
         window.addstr( 1, 1, "The player data hidden file ('.playerdata.json') does not apear in this directory" )
         window.addstr( 2, 1,"Please wait...." )
         window.refresh()
         time.sleep( 1 )
         continue

      # Sort players by the floating pointer number Initiative
      PlayerList.sort( key = lambda x: x.Initiative, reverse = True )

      # Sum up the totalTime by ALL players for later display. 
      # This allow allows us to calculate a % for each player!
      totalTime = timedelta( 0 )
      for i in PlayerList:
         totalTime += i.SoftUpdate()

      # Avoid x/0
      if ( totalTime.total_seconds() < 1 ):
         totalTime = timedelta( seconds = 1 )

      # Print header
      window.addstr(0,0, "Index Active     Name     Init   Time    TimePer AvgTurn Turns Status" )

      # Track the row of the screen we are currently on. 
      screenRow = 1

      # Print out information for EACH character in combat
      for idx,val in enumerate( PlayerList ):

         # Get player dict to parse out!
         pDict = val.GetStrDict( totalTime )
         window.addstr( 
            screenRow, 
            0, 
            ' [{0:2.0f}] {Active:6} {Name:^12} ({Init:2.0f})  {TTime} ({PTime:6.2%}) {ATime} {Turns:^5} {1}'.format( 
               idx+1, 
               PrettyStatus( pDict['Status'] ), 
               **pDict 
               ) 
            )
         
         # Check to see if we are the active player, and highlight to bring attention if we are!
         if len( pDict['Active'] ) :
            window.chgat( screenRow, 0, maxY, curses.color_pair( 1 ) )
            # Parse through each character in buffer
            for x in range(13,25):
               # If this is NOT a space (Thus a valid char) bold it!
               if ( window.inch( screenRow, x ) & 0xFF ) != ( ord(' ') & 0xFF ) :
                  window.chgat( screenRow, x, 1, curses.A_BOLD | curses.color_pair( 1 ) )
         # Incriment the row each loop
         screenRow += 1

      # One last incriment for the total Time!
      screenRow += 1
      window.addstr( screenRow, 0, "Total Time: {}".format( DeltaTruncate( totalTime ) ) )
      
      # We have finished the update! Refresh all touched characters
      window.refresh( )

      # Mark EVERY character as touched for the next update. 
      window.clear( )


      # Should be fast enough to see like instant input from the output screen!
      time.sleep( UpdateRate )

def PrettyStatus( statusDict ):
   """
   Make the statusDict print out in a much more human readable format
   """

   # Return empty quick when we are empty
   if len( statusDict ) == 0 :
      return ""
   
   # Build up the retStr to have all of our data
   retStr = ""
   for i in statusDict :
      # After the first retStr loop, add a comma before adding data!
      if len( retStr ) :
         retStr += ", "

      # Add name of status
      retStr += i

      # Add Brackets and lengh of status
      retStr += " ["
      retStr += str( statusDict[i] )
      retStr += "]"

   # Return Results
   return retStr


wrapper(Main)

print curses.COLORS

print "Fin"
