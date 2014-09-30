#!/usr/bin/env python
from common import Player
from datetime import datetime,timedelta
from json import JSONEncoder
import atexit
import json
import os
import sys
import time


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
         print "Cannot encode!"
         print type(o)
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
   if ( os.name == 'nt' ):
      os.system('cls')
      
   elif (os.name == 'posix' ):
      os.system('clear')

   else:
      print os.name
      assert( False ), "This OS must be updated!"

def GetInput( prompt = "> ", inputType = None, forceReturn = True ):
   """
   Take input from user, prompted by the prompt string. 
   
   If inputType is given, we will ignore all input that cannot be cast into
   that type. 

   forceReturn will for the prompt to wait for valid input if a type is given 
   (default True)
   """
   if ( inputType == None ):
      return raw_input( prompt )
   else:
      while(1):
         try:
            return inputType( raw_input( prompt ) )
         except ValueError:
            if forceReturn :
               continue
            else:
               return None

def RunMenu( menuTuple, menuTitle, loop = True ):
   while( 1 ):
      ClearScreen()
      print "<<< %s >>>"%( menuTitle )
      for idx,val in enumerate( menuTuple ):
         print "[%d] %s"%( idx+1, val[0] )
      print 

      sel = GetInput( "> ", str )

      if( len( sel ) ):
         try:
            sel = int( sel ) - 1
            if sel < 0 :
               continue
         except ValueError:
            continue
      else:
         continue

      if ( sel >= len( menuTuple ) or sel < 0 ):
         continue

      if ( menuTuple[sel][1] == None ):
         return False

      menuTuple[sel][1]()
      
      if ( not loop ):
         return True

def Main( ):
   global GLOB_PLAYERS

   GLOB_PLAYERS = []
   atexit.register( Cleanup )
   
   if( os.path.exists('.playerdata.json') ):
      EmergencyReload()
   else:
      # BlastPlayers()
      DefaultGroup()

   menu = (
           ( "Run Encounter", RunEncounter ),
           ( "Default Group", DefaultGroup ),
           ( "Exit", Exit ), 
           )

   RunMenu( menu, "Main Menu", True )

def DefaultGroup( ):
   global GLOB_PLAYERS


   ClearScreen()
   print "\nInitiate Default Group!"
   
   for i in GLOB_PLAYERS:
      if i.Active :
         print "WARNING! Active Player Detected! Overwrite?"
         tmp = GetInput( "> ", str )
         if ( tmp not in ["y","Y" ] ):
            return
         else:
            break
   GLOB_PLAYERS = []

   # We don't need to ask anymore, we are crash safe!
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



   SaveGame()

   return 0

def ListPlayers( ):
   global GLOB_PLAYERS

   GLOB_PLAYERS.sort( key = lambda x: x.Initiative, reverse = True )

   totalTime = timedelta( 0 )
   for i in GLOB_PLAYERS:
      totalTime += i.SoftUpdate()

   if ( totalTime.total_seconds() < 1 ):
      totalTime = timedelta( seconds = 1 )
   print "\nIndex Name"
   for idx,val in enumerate( GLOB_PLAYERS ):
      # print " [%2d]"%(idx+1),val.GetStr( totalTime )
      print " [{:2}] {}".format( idx+1, val.Name )

def EditPlayers( ):
   menu = (
           ( "Add Player", AddPlayer ),
           ( "Blast Players", BlastPlayers ),
           ( "Blast Initiative", BlastInitiative ),
           ( "Delete Player", DelPlayer ),
           ( "Edit Player", EditPlayer ),
           ( "Return", None ),
           )
   while( 1 ):
      ClearScreen()
      ListPlayers()

      if ( not RunMenu( menu, "Edit Players", False ) ):
         break

def BlastPlayers( ):
   global GLOB_PLAYERS
   ClearScreen()
   print "\nBlast set of players into initiative. \nBlank line to finish!"
   while( 1 ):
      print "Next name to add..."
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
   ClearScreen()
   print "\nBlast group Initiatives!"
   print "Enter each players initiative. If blank, old number will be kept."
   for idx,val in enumerate( GLOB_PLAYERS ):
      print "Init for:",val.GetStr()
      tmp = GetInput( "> ", str )
      if ( len( tmp ) ):
         try:
            val.Initiative = float( tmp )
         except ValueError:
            continue


def AddPlayer( ):
   global GLOB_PLAYERS

   ClearScreen()
   print "\nAdding player to game!"
   mule = Player()

   print "Player Name:"
   mule.Name = GetInput( "> ", str )
   
   # Error check for empty names!
   if( not len( mule.Name ) ):
      return
 
   print "Initiative:"
   mule.Initiative = GetInput( "> ", float )

   GLOB_PLAYERS.append( mule )

   return 

def DelPlayer( ):
   ClearScreen()
   print "\nSelect Player to Delete."
   print "Blank line to return"

   while( 1 ):
      ListPlayers()

      tmp = GetInput( "> ", str )
      try:
         tmp = int( tmp )
      except ValueError:
         return
      if ( tmp > 0 and tmp <= len( GLOB_PLAYERS ) ):
         del GLOB_PLAYERS[ tmp - 1 ]
      else:
         print "Invalid Delete!\n"


def EditPlayer( ):
   global GLOB_PLAYERS

   while( 1 ):
      ClearScreen()
      print "\nSelect Player to Edit"
      print "Blank Line to Return"
      ListPlayers()

      sel = GetInput( "> ", str )

      try:
         sel = int( sel )
      except ValueError:
         break

      if ( sel > 0 and sel <= len( GLOB_PLAYERS ) ):
         # Correct selection for rest of menu
         sel -= 1

         print "You can press enter to skip new changes"
         print "\nSelected to edit:",GLOB_PLAYERS[ sel ].GetStr()
         
         print "New Name:"
         tmp = GetInput( "> ", str )
         if ( len( tmp ) ):
            GLOB_PLAYERS[ sel ].Name = tmp

         print "New Initiative:"
         tmp = GetInput( "> ", str )
         if ( len( tmp ) ):
            try:
               GLOB_PLAYERS[ sel ].Initiative = float( tmp )
            except ValueError:
               pass

         pass
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
      print "\n<< Options >>"
      print "#: Select Active Player"
      print "0: No Active Player, pause game"
      print "n: Next Player"
      print "s: Status Edit Menu"
      print 
      print "a: Add Player"
      print "b: Blast In Players"
      print "d: Delete Player"
      print "e: Edit Player"
      print "i: Blast In Initiatives"
      print 
      print "r: Reset Encounter"
      print "x: Return to Main Menu"


   global GLOB_PLAYERS

   while( 1 ):
      SaveGame( )
      ClearScreen()
      PrintHelp()
      GLOB_PLAYERS.sort( key = lambda x: x.Initiative, reverse = True )
      # sel = GetInput( "\n> ", str )
      sel = sys.stdin.read(1)
      
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
         if ( GetInput( "ARE YOU SURE???> ", str ) in [ "y", "Y" ] ):
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
   ClearScreen()
   print "\nSelect Player to exit the status of."
   print "Blank line to return"

   while( 1 ):
      ListPlayers()

      tmp = GetInput( "> ", int, False )
      if tmp == None or type(tmp) != int :
         return
      
      if ( tmp > 0 and tmp <= len( GLOB_PLAYERS ) ):
         StatusSubMenu( tmp - 1 )
         continue
      else:
         print "Invalid player slection!"
   pass

def StatusSubMenu( sel ):
   while True :
      ClearScreen()
      print "\nEditing the status of {}".format( GLOB_PLAYERS[sel].Name )
      
      print "Current Status:"
      for i in GLOB_PLAYERS[sel].Status : 
         print "{} [{}]".format( i, GLOB_PLAYERS[sel].Status[i] )
      
      print "\nSelection option"
      print "a: Add Status to player"
      print "r: Remove status from player"
      print "d: Remove status from player"
      print "x: Done"

      localSel = GetInput( "> ", str )
      if not len(localSel) or localSel == 'x' :
         break
      if localSel == 'a' :

         print "\nName of Status:"
         key = GetInput( "> ", str, False )
         if not len( key ) :
            continue
         
         print "Duration of Status (In turns):"
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
         
         print "Current status..."
         
         for idx,val in enumerate( GLOB_PLAYERS[sel].Status ) :
            print " [{}] {}:{}".format( idx + 1, val, GLOB_PLAYERS[sel].Status[val] )
         print "Select Status to delete:"

         localSel = GetInput( "> ", int, False )
         # Check for None input, or invlaid range and contiue if so
         if localSel == None or localSel < 1 or localSel > len( GLOB_PLAYERS[sel].Status ) :
            continue

         del GLOB_PLAYERS[sel].Status[ GLOB_PLAYERS[sel].Status.keys()[localSel-1] ] 
         SaveGame()



         


def Exit( ):
   #print "Quit?"

   #tmp = GetInput( "> ", str )
   #if ( tmp in ["y","Y" ] ):
   #   quit()
   #else:
   #   return

   # We don't need to ask anymore, we are crash safe!
   quit()

def Cleanup( ):
   try:
      #os.remove('.playerdata.json')
      pass
   except OSError:
      pass

Main( )
