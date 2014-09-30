#!/usr/bin/env python
from datetime import datetime,timedelta
import os
import time
import json
from json import JSONEncoder
import atexit
from common import Player
from curses.wrapper import wrapper
import curses

# TODO: This program does a poor job of screen overrun protection. Find and fix
# 

class PlayerEncoder( JSONEncoder ) :
   def default(self, o):
      if type( o ) == Player  :
         d = {}
         d['Name'] = o.Name
         d['Active'] = o.Active
         d['Initiative'] = o.Initiative
         d['TimeTaken'] = o.TimeTaken
         d['TurnStart'] = o.TurnStart
         d['Turns'] = o.Turns
         d['Status'] = o.Status
      elif type( o ) == datetime :
         return o.isoformat()
      elif type( o ) == timedelta :
         return o.total_seconds()
      else:
         assert(0),"Cannot encode something! Debug Time!"
         # print "Cannot encode!"
         # print type(o)
         return o

      return d 

def EmergencyReload( ):
   global GLOB_PLAYERS
   with open(".playerdata.json",'r') as fp:
      for i in json.load(fp):
         GLOB_PLAYERS.append(Player())
         GLOB_PLAYERS[-1].Name = i['Name']
         GLOB_PLAYERS[-1].Active = i['Active']
         GLOB_PLAYERS[-1].Initiative = i['Initiative']
         GLOB_PLAYERS[-1].TimeTaken = timedelta( seconds = float( i['TimeTaken'] ) )
         GLOB_PLAYERS[-1].TurnStart = i['TurnStart']
         if( i['TurnStart'] ):
            GLOB_PLAYERS[-1].TurnStart = datetime.strptime( i['TurnStart'] , "%Y-%m-%dT%H:%M:%S.%f")
         GLOB_PLAYERS[-1].Turns = i['Turns']
         GLOB_PLAYERS[-1].Status = i['Status']

def ClearScreen( ):
   """
   Unused in curses!
   """
   pass
   # if ( os.name == 'nt' ):
   #    os.system('cls')
      
   # elif (os.name == 'posix' ):
   #    os.system('clear')

   # else:
   #    print os.name
   #    assert( False ), "This OS must be updated!"

def GetInput( prompt = "> ", inputType = None, forceReturn = True ):
   """
   Take input from user, prompted by the prompt string. 
   
   If inputType is given, we will ignore all input that cannot be cast into
   that type. 

   forceReturn will for the prompt to wait for valid input if a type is given 
   (default True)
   """
      
   curses.echo()
   while(1):
      stdscr.addstr( prompt )
      stdscr.refresh()
      tmp = stdscr.getstr()
      if inputType == None :
         curses.noecho()
         return tmp
      try:
         tmp = inputType( tmp )
         curses.noecho()
         return tmp
      except ValueError:
         if forceReturn :
            continue
         else:
            curses.noecho()
            return None

def RunMenu( menuTuple, menuTitle, loop = True ):
   # global stdscr

   while( 1 ):
      # ClearScreen()
      stdscr.clear()
      stdscr.addstr( "<<< %s >>>\n"%( menuTitle ) )
      for idx,val in enumerate( menuTuple ):
         stdscr.addstr( "[%d] %s\n"%( idx+1, val[0] ) )
      stdscr.addstr("> ")
      stdscr.refresh()


      sel = stdscr.getkey()

      try:
         sel = int( sel ) - 1
      except ValueError:
         continue

      if ( sel >= len( menuTuple ) or sel < 0 ):
         continue

      # If the menu location doesn't have a function call, we return. 
      # This allows for a handy sort of 'go back' menu funcion!
      if ( menuTuple[sel][1] == None ):
         return False

      menuTuple[sel][1]()
      
      if not loop :
         return True

def Main( window ):
   global GLOB_PLAYERS
   global stdscr
   stdscr = window

   GLOB_PLAYERS = []
   atexit.register( Cleanup )


   
   if( os.path.exists('.playerdata.json') ):
      EmergencyReload()
   else:
      DefaultGroup()

   menu = (
           ( "Run Encounter", RunEncounter ),
           ( "Default Group", DefaultGroup ),
           ( "Exit", Exit ), 
           )

   RunMenu( menu, "Main Menu", True )

def DefaultGroup( ):
   global GLOB_PLAYERS


   # ClearScreen()
   stdscr.clear()
   stdscr.addstr( "Initiate Default Group!\n" )
   
   for i in GLOB_PLAYERS:
      if i.Active :
         stdscr.addstr( "WARNING! Active Player Detected! Overwrite? (y/n)\n" )
         
         # Check to see if the user really wants to overwrite.
         stdscr.addstr( "> " )
         if stdscr.getkey() == 'y' :
            break
         else:
            # Anything other then a y will result in aborting the overwrite
            return

   # Clear global list if it exists
   GLOB_PLAYERS = []

   # Initiate default players list
   # TODO: This would be better as a pull from local user settings.
   mule = Player()   
   mule.Name = "Nate H"
   mule.Initiative = 0
   GLOB_PLAYERS.append( mule )
   
   mule = Player()   
   mule.Name = "John T"
   mule.Initiative = 0
   GLOB_PLAYERS.append( mule )
   
   mule = Player()   
   mule.Name = "Alexandria T"
   mule.Initiative = 0
   GLOB_PLAYERS.append( mule )
   
   mule = Player()   
   mule.Name = "Victor T"
   mule.Initiative = 0
   GLOB_PLAYERS.append( mule )
   
   mule = Player()   
   mule.Name = "NPC(s)"
   mule.Initiative = 0
   GLOB_PLAYERS.append( mule )

   # Write changes to disk
   SaveGame()

   return

def ListPlayers( ):
   """
   Insert current list of players into the buffer
   WARNING: Will not clear or refresh!
   """
   global GLOB_PLAYERS

   GLOB_PLAYERS.sort( key = lambda x: x.Initiative, reverse = True )

   totalTime = timedelta( 0 )
   for i in GLOB_PLAYERS:
      totalTime += i.SoftUpdate()

   if ( totalTime.total_seconds() < 1 ):
      totalTime = timedelta( seconds = 1 )

   # stdscr.clear()
   stdscr.addstr( "Index Name\n" )
   for idx,val in enumerate( GLOB_PLAYERS ):
      stdscr.addstr( " [{:2}] {}\n".format( idx+1, val.Name ) )
   # stdscr.refresh()

def BlastPlayers( ):
   global GLOB_PLAYERS

   while( 1 ):
      stdscr.clear()
      stdscr.addstr( "Blast set of players into initiative.\n" )
      stdscr.addstr( "Blank line to finish!\n" )
      stdscr.addstr( "Next name to add...\n" )

      tmp = GetInput( "> ", str )
      if ( len( tmp ) ):
         mule = Player()
         mule.Name = tmp
         GLOB_PLAYERS.append( mule )
      else:
         break
   BlastInitiative()
   return

def BlastInitiative( ):
   stdscr.clear()
   stdscr.addstr( "Blast group Initiatives!\n" )
   stdscr.addstr( "Enter each players initiative. " )
   stdscr.addstr( "If blank, old number will be kept.\n" )
   for idx,val in enumerate( GLOB_PLAYERS ):
      stdscr.addstr( "Init for: {Name} [{Init:.0f}] ".format( **val.GetStrDict() ) )
      tmp = GetInput( "> ", str )
      if ( len( tmp ) ):
         try:
            val.Initiative = float( tmp )
         except ValueError:
            continue


def AddPlayer( ):
   global GLOB_PLAYERS

   stdscr.clear()
   stdscr.addstr( "Adding player to game!\n" )
   mule = Player()

   stdscr.addstr( "Player Name: " )
   curses.echo()
   mule.Name = stdscr.getstr()
   curses.noecho()
   
   # Error check for empty names!
   if( not len( mule.Name ) ):
      return
 
   stdscr.addstr( "Initiative: " )
   mule.Initiative = GetInput( "", float )

   GLOB_PLAYERS.append( mule )

   return 

def DelPlayer( ):

   while( 1 ):
      stdscr.clear()
      stdscr.addstr( "Select Player to Delete.\n" )
      stdscr.addstr( "Blank line to return.\n" )

      ListPlayers()

      tmp = GetInput( "> ", str )
      try:
         tmp = int( tmp )
      except ValueError:
         return
      if ( tmp > 0 and tmp <= len( GLOB_PLAYERS ) ):
         del GLOB_PLAYERS[ tmp - 1 ]
         SaveGame( )
      else:
         continue


def EditPlayer( ):
   global GLOB_PLAYERS

   while( 1 ):
      stdscr.clear()
      stdscr.addstr( "Select Player to Edit\n" )
      stdscr.addstr( "Blank Line to Return\n" )
      ListPlayers()
      stdscr.addstr( ">> " )
      stdscr.refresh()
      sel = stdscr.getkey()

      if sel == '\n' :
         return

      try:
         sel = int( sel )
      except ValueError:
         break

      if ( sel > 0 and sel <= len( GLOB_PLAYERS ) ):
         # Correct selection for rest of menu
         sel -= 1

         stdscr.addstr( "You can press enter to skip new changes\n" )
         stdscr.addstr( "Selected to edit: {}\n".format( 
            GLOB_PLAYERS[ sel ].GetStr() 
            ) 
         )
         
         stdscr.addstr( "New Name: " )
         tmp = GetInput( "", str )
         if ( len( tmp ) ):
            GLOB_PLAYERS[ sel ].Name = tmp

         stdscr.addstr( "New Initiative: " )
         tmp = GetInput( "", str )
         if ( len( tmp ) ):
            try:
               GLOB_PLAYERS[ sel ].Initiative = float( tmp )
            except ValueError:
               pass
         SaveGame()
      else:
         continue

def SaveGame( ):
   # Save current encounter to a JSON file for human reading a parseing
   # with other applications!
   with open('.playerdata.json','w') as fp :
      json.dump( GLOB_PLAYERS, fp, cls=PlayerEncoder, indent=3 )

   return None

def RunEncounter( ):
   def PrintHelp( ):
      stdscr.addstr( "<< Options >>\n" )
      stdscr.addstr( "#: Select Active Player\n" )
      stdscr.addstr( "0: No Active Player, pause game\n" )
      stdscr.addstr( "n: Next Player\n" )
      stdscr.addstr( "s: Status Edit Menu\n" )
      stdscr.addstr( "\n" )
      stdscr.addstr( "a: Add Player\n" )
      stdscr.addstr( "b: Blast In Players\n" )
      stdscr.addstr( "d: Delete Player\n" )
      stdscr.addstr( "e: Edit Player\n" )
      stdscr.addstr( "i: Blast In Initiatives\n" )
      stdscr.addstr( "\n" )
      stdscr.addstr( "r: Reset Encounter\n" )
      stdscr.addstr( "x: Return to Main Menu\n" )


   global GLOB_PLAYERS

   while( 1 ):
      # Write to disk!
      SaveGame( )

      stdscr.clear()
      # ClearScreen( )
      PrintHelp( )
      GLOB_PLAYERS.sort( key = lambda x: x.Initiative, reverse = True )
      stdscr.addstr( ">> " )
      stdscr.refresh()
      # curses.echo()
      sel = stdscr.getkey()

      if ( sel in ["?","help","h","HELP","Help"]):
         PrintHelp()
         raw_input("Press Enter to continue...")
         continue

      # Exit from this menu
      if ( sel in ["x","X"] ):
         break

      if ( sel in ["i","I"] ):
         BlastInitiative()
         continue

      if ( sel in ["b","B"] ):
         BlastPlayers()
         continue

      if ( sel in ["a","A"] ):
         AddPlayer()
         continue

      if ( sel in ["r", "R"] ):
         if ( GetInput( "\nARE YOU SURE???> ", str ) in [ "y", "Y" ] ):
            for i in GLOB_PLAYERS:
               i.Clear()
         continue

      if ( sel in ["e","E"] ):
         EditPlayer()
         continue

      if ( sel in ["d","D"] ):
         DelPlayer()
         continue

      if sel in ["s","S"] :
         StatusMenu()
         continue

      # Next Player
      if ( sel in ["n","N"] ):
         # Find Active Player
         activeIdx = None
         for idx,val in enumerate( GLOB_PLAYERS ):
            if ( val.Active ):
               activeIdx = idx
               break

         # We didn't find a active player...
         if ( activeIdx == None ):
            continue

         # We DID find one! Make it the next one!
         for i in GLOB_PLAYERS:
            i.Update()

         GLOB_PLAYERS[ ( activeIdx + 1 ) % len ( GLOB_PLAYERS ) ].BeginTurn()
         continue

      try:
         sel = int( sel )
      except ValueError:
         continue

      if ( sel > 0 and sel <= len( GLOB_PLAYERS ) and not GLOB_PLAYERS[ sel - 1 ].Active ):
         for i in GLOB_PLAYERS:
            i.Update()
         # Adjust for index and display, begin that turn
         GLOB_PLAYERS[ sel - 1 ].BeginTurn()
      elif ( sel == 0 ):
         for i in GLOB_PLAYERS:
            i.Update()


def StatusMenu( ):

   while( 1 ):
      stdscr.clear()
      stdscr.addstr( "Select Player to exit the status of.\n" )
      stdscr.addstr( "Blank line to return\n" )
      ListPlayers()
      stdscr.addstr( ">> " )
      stdscr.refresh()
      tmp = stdscr.getkey()

      if tmp == '\n' :
         return

      try:
         tmp = int( tmp )
      except ValueError:
         continue
      
      if tmp > 0 and tmp <= len( GLOB_PLAYERS ) :
         StatusSubMenu( tmp - 1 )
         continue
      else:
         stdscr.addstr( "Invalid player slection!" )
         stdscr.refresh()
         curses.napms(1000)
   pass

def StatusSubMenu( sel ):
   while True :
      stdscr.clear()
      stdscr.addstr( "Editing the status of {}\n".format( GLOB_PLAYERS[sel].Name ) )
      
      stdscr.addstr( "Current Status:\n" )
      for i in GLOB_PLAYERS[sel].Status : 
         stdscr.addstr( "{} [{}]\n".format( i, GLOB_PLAYERS[sel].Status[i] ) )
      
      stdscr.addstr( "\nSelection option\n" )
      stdscr.addstr( "a: Add Status to player\n" )
      stdscr.addstr( "r: Remove status from player\n" )
      stdscr.addstr( "d: Remove status from player\n" )
      stdscr.addstr( "x: Done\n" )

      stdscr.addstr( ">> " )
      stdscr.refresh()
      localSel = stdscr.getkey()
      if localSel == '\n' or localSel == 'x' :
         break
      if localSel == 'a' :
         stdscr.clear()      
         stdscr.addstr( "Editing the status of {}\n".format( GLOB_PLAYERS[sel].Name ) )
         stdscr.addstr( "Name of Status:\n" )
         key = GetInput( "> ", str, False )
         if not len( key ) :
            continue
         
         stdscr.addstr( "Duration of Status (In turns):\n" )
         turns = GetInput( "> ", int, False )
         if not turns :
            continue
         
         GLOB_PLAYERS[sel].AddStatus( key, turns )
         SaveGame()
         continue
      
      if localSel in ['r','d'] :
         
         # Dont bother to try to delete if we dont have any status to delete
         if not len( GLOB_PLAYERS[sel].Status ) :
            continue
         stdscr.clear()
         stdscr.addstr( "Editing the status of {}\n".format( GLOB_PLAYERS[sel].Name ) )

         stdscr.addstr( "Current status...\n" )
         
         for idx,val in enumerate( GLOB_PLAYERS[sel].Status ) :
            stdscr.addstr( " [{}] {}:{}\n".format( 
               idx + 1, 
               val, 
               GLOB_PLAYERS[sel].Status[val] 
               ) 
            )
         stdscr.addstr( "Select Status to delete:\n" )

         localSel = GetInput( "> ", int, False )
         # Check for None input, or invlaid range and contiue if so
         if localSel == None or localSel < 1 or localSel > len( GLOB_PLAYERS[sel].Status ) :
            continue

         del GLOB_PLAYERS[sel].Status[ GLOB_PLAYERS[sel].Status.keys()[localSel-1] ] 
         SaveGame()

def Exit( ):
   quit()

def Cleanup( ):
   # Old versions of linux don't handle the wrapper function correctly, handle them here instead. 
   curses.nocbreak()
   curses.echo()
   curses.endwin()
   try:
      pass
   except OSError:
      pass

# Call the application within the curses wrapper!
wrapper( Main )


