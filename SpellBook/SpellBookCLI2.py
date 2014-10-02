#!/usr/bin/env python
import csv
import os
import re
import readline
import sre_constants
import textwrap
import time

# Options

# Source Filter List
sourceFilterList = [ 'Ultimate Magic', 'Ultimate Combat', 'Advanced Race Guide',
   'APG', 'PFRPG Core', ]

# Level of verbose output
# 0: Absolute minimum
# 1: Basic Spell Info
# 2: Castable Spell Info
# 3: Full Spell Info
Verbosity = 1

global completionList
completionList = []

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

def PrettyPrintSpell( inputEntry, detailLevel = 0 ):
   if( detailLevel == 0 ):
      outputStr = "%s: %s"
   if( detailLevel >= 1 ):
      outputStr = "%12s: %s"
   
   print outputStr%('Name',inputEntry['name'])
   if( detailLevel == 0 ):
      return
   
   print outputStr%('Components',inputEntry['components'])
   
   print outputStr%('Duration',inputEntry['duration'].capitalize( ) )
   
   print outputStr%('Casting Time',inputEntry['casting_time'].capitalize( ) )
   
   # Some spells don't have saving throw info, don't print a blank statment
   if( inputEntry['saving_throw'] ):
      print outputStr%('Saving Throw', inputEntry['saving_throw'].capitalize( ) )
   
   if( detailLevel >= 2 ):
      tmp = outputStr%('Spell Level',inputEntry['spell_level'] )
      print '\n'.join( textwrap.TextWrapper(subsequent_indent='                 ').wrap(tmp) )

      # Not all spells have resistance info. 
      if( inputEntry['spell_resistence'] ):
         print outputStr%('Resistance', inputEntry['spell_resistence'].capitalize( ) )
      
      print outputStr%('School',inputEntry['school'].capitalize( ) ),
      
      if( inputEntry['subschool'] ):
         print "( %s )"%( inputEntry['subschool'] )
      else:
         print
   
   # Not all spells have targets, dont print if we lack that data
   if( inputEntry['targets'] ):
      # apprently some of these are very long...
      tmp = outputStr%('Targets',inputEntry['targets'].capitalize( ) ) 
      print '\n'.join( textwrap.TextWrapper(subsequent_indent='                 ').wrap(tmp) )  

   # Not all spells have targets, dont print if we lack that data
   if( inputEntry['range'] ):
      print outputStr%('Range',inputEntry['range'].capitalize( ) )
   
   if( detailLevel > 0 and detailLevel < 3 ):
      tmp = outputStr%('Description',inputEntry['short_description'])
      tmp = SanatizeString( tmp )
      print '\n'.join( textwrap.TextWrapper(subsequent_indent='                 ').wrap(tmp) )

   
   elif( detailLevel >= 3 ):
      tmp = outputStr%("Description",inputEntry['description_formated'])
      tmp = AdvSanatizeString( tmp )
      tmp = tmp.splitlines()
      for idx, val in enumerate( tmp ):
         if ( idx == len( tmp ) - 1 and len( val ) == 0 ):
            break
         
         if ( idx == 0 ):
            print '\n'.join( textwrap.TextWrapper(subsequent_indent='                 ').wrap(val) )
         else:
            print '\n'.join( textwrap.TextWrapper(subsequent_indent='                 ', initial_indent='                 ').wrap(val) )
      
      print outputStr%("Source",inputEntry['source'])

def completer(text, state):
   global completionList
   options = [i for i in completionList if i.startswith(text)]
   if state < len(options):
      return options[state]
   else:
      return None 

def SanatizeString( Input_String ):
   for i in range( 128, 256 ):
      Input_String = Input_String.replace( chr(i) ,"")
   return Input_String

def AdvSanatizeString( Input_String ):
   Input_String = re.sub( '</?i>', '', Input_String )
   Input_String = re.sub( '</p>', "\n\n", Input_String )
   Input_String = re.sub( '<p>', '', Input_String )
   return Input_String

def PrintHelpString( ):
   print "\nAvliable Options"
   print "x: Exit"
   print "h: This help statement"
   print "v: Change Verbosity (Currently {})".format( Verbosity )
   print
   print "a: Add a Filter"
   print "r: Remove a Filter (NOT IMPLIMENTED)"
   print "e: Edit a Filter (NOT IMPLIMENTED)"
   print
   print "Enter: Search & Display"

def DisplayCurrentFilter( ):
   global Filter_Dict
   print "Current Filter(s):"

   if len( Filter_Dict ) < 1 :
      print "  Empty"
      return

   for i in Filter_Dict:
      print "  {}=> {}".format(i,Filter_Dict[i])

def ChangeVerbosity( ):
   global Verbosity

   print "\n\n<<< Chang Verbosity >>>"
   print "\nEnter new Verbosity Setting"
   print "Current Setting is {}".format( Verbosity )
   print "0 => Name Only"
   print "1 => Gameplay Details"
   print "2 => Casting Details"
   print "3 => Full Details"
   print "4 => OMFG (Not yet supported)"

   try :
      Verbosity = input( "> " )
   except ( ValueError, NameError ) :
      print "Invalid type, Verbosity unchanged"
      return
   except ( SyntaxError ) :
      print "Verbosity remains at {}".format( Verbosity )
      return

   try :
      Verbosity = int( Verbosity )
   except ValueError :
      print "Invalid Verbosity, setting unchanged"

   print "Verbosity set to {}".format( Verbosity )

   return


def AddFilter( ):
   # Be clear about globals
   global completionList
   global Filter_Dict

   # Select type of Filter to add
   allowedFilterTypes = [ 
      'name', 
      'school',
      'subschool',
      'descriptor',
      'spell_level',
      'casting_time',
      'components',
      'costly_components',
      'range',
      'area',
      'effect',
      'targets',
      'duration',
      'dismissible',
      'shapeable',
      'saving_throw',
      'spell_resistence',
      'description',
      'description_formated',
      'source',
      'full_text',
      'verbal',
      'somatic',
      'material',
      'focus',
      'divine_focus',
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
      'adept',
      'deity',
      'SLA_Level',
      'domain',
      'short_description',
      'acid',
      'air',
      'chaotic',
      'cold',
      'curse',
      'darkness',
      'death',
      'disease',
      'earth',
      'electricity',
      'emotion',
      'evil',
      'fear',
      'fire',
      'force',
      'good',
      'language_dependent',
      'lawful',
      'light',
      'mind_affecting',
      'pain',
      'poison',
      'shadow',
      'sonic',
      'water',
      'linktext',
      'id',
      'material_costs',
      'bloodline',
      'patron',
      'mythic_text',
      'augmented',
      'mythic',
   ]
   
   classFilters = [ 
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
      'adept',
   ]

   typeFilters = [
      'acid',
      'air',
      'chaotic',
      'cold',
      'curse',
      'darkness',
      'death',
      'disease',
      'earth',
      'electricity',
      'emotion',
      'evil',
      'fear',
      'fire',
      'force',
      'good',
      'language_dependent',
      'lawful',
      'light',
      'mind_affecting',
      'pain',
      'poison',
      'shadow',
      'sonic',
      'water',
   ]
   
   # Deep copy that thing, and apply to current completer
   completionList = list( allowedFilterTypes )
   readline.parse_and_bind( "tab: complete" )
   readline.set_completer( completer )
   
   # Get the filter type, and offer help to user. 
   # This loop is a bit clunky, but will help with new users a LOT
   filterType = ""
   while not len( filterType ) :
      print "\n\n<<< Add Filter >>>"
      print "\nSelect csv Field to filter by"
      print "!!! Enter 'help' for a help screen !!!"
      print "Hit tab to see completions. Hitting tab without anything entered"
      print "  will show all avliable fields!"
      filterType = raw_input( "> " )

      # Print very verbose help to the user. 
      if filterType == 'help' :

         # Reset this to prevent leaving the loop
         filterType = ""
         print "Filtering is done off of the raw CSV dump from the PFSRD. Note "
         print "  that prestige classes are not supported. After selecting a "
         print "  field you will be asked to give a valid regex. If ALL given "
         print "  filters match a spell, it will be returned in the search. "
         print "Example:"
         print "  Enter 'name' as your filter field"
         print "  Enter 'magic' as your valid regex"
         print "  Press enter on the main menu to find ALL spells with 'magic'"
         print "    in their name."
         print "NOTE:"
         print "  Searches are NOT case sensitive!"
         print "Examples:"
         print "  Search for 'wiz' with a regex of '1|2' to find all of your "
         print "  first and second level spells"
         print
         print "  Search for 'wiz' with a regex of '[0-9]' and 'fire' with "
         print "  a filter of '1' to find all wizard spells that deal fire "
         print "  damage. "
         print
         print "  If you arn't sure where to search, 'full_text' is a very"
         print "  verbose field, and is basicly a copy from the book text."
         print "  searching this is a workable catch all"

      # Allow blank lines to exit this mode still
      elif not len( filterType ) :
         return

   # Check to see if we got a valid filter type
   if filterType not in allowedFilterTypes :
      print "Sorry, we can't filted based on '{}'".format( filterType )
      completionList = []
      readline.set_completer( completer )
      return False
   
   # We now offer any help we can
   if filterType in classFilters :
      print "\nYou have selected to filter based on '{}'".format( filterType )
      print "  This is a CLASS filter. Items in the CSV will have one of two potential values."
      print "  If your class has that spell, the spell level will be given as a intiger"
      print "  If your class does not have the spell, 'null' will be listed in this field"
      print "  A good exampe for a regex that will find all spells from levels 0 to 2 would be [0-2]"

   if filterType in typeFilters :
      print "\nYou have selected to filter based on '{}'".format( filterType )
      print "  This is a TYPE filter. If a given spell has that type of damage/effect/descriptor"
      print "  it will have a '1' in this field. IF it does not have that type, it will have a 0"
      print "  in that field. "

   # Now lets get the regex from the user
   print "\nEnter value to filter by (valid regex)"
   filterValue = raw_input( "> " )

   # Empty filters make me Cry!
   if len( filterValue ) == 0 :
      print "Error: We need SOMETHING to filter by!"
      return

   # Run a test compile of the regex so we know we got something usable later
   try:
      re.compile( filterValue )
   # Tell the user that they don't know how to regex, then return to main menu
   except sre_constants.error, e:
      print "Sorry, but '{}' isn't a valid regex in python".format( filterValue )
      print "Error given: {}".format( e )
      completionList = []
      readline.set_completer( completer )
      return False

   # We have a valid regex, save it and return 
   Filter_Dict[ filterType ] = filterValue
   return True



def RemoveFilter( ):
   global Filter_Dict
   print "\n\n<<< Remove Filter >>>"
   print "Blank line to return"
   print "Enter index of item to delete"
   print "Current Filters:"
   
   if not len( Filter_Dict ) :
      print "  NONE! Sorry, we can't delete nothing!"
      return
   
   
   for idx,val in enumerate( Filter_Dict ) :
      print '\033[33m' + "  [{}] {}: {}".format( idx+1, val, Filter_Dict[ val ] ) + '\033[0m'


   try:
      user_selection = input( "> " )
   except ( ValueError, NameError ) :
      print "Invalid int, returning"
      return
   except ( SyntaxError ) :
      print "No changes"
      return

   # Shift to corrent indexing (We added one to display to users)
   user_selection -= 1 

   # Loop through to try to find the index to delete
   for idx,val in enumerate( Filter_Dict ) :
      if idx == user_selection :
         keyToDelete = val
         break
   # If we didn't break, we didn't find that index. Tell the user and return
   else:
      print "Index invalid, returning to Main Menu"
      return

   # If we didn't return in the else of the for loop, we found the key
   # Delete it
   print "Removed filter: {}: {}".format( 
      keyToDelete, 
      Filter_Dict[ keyToDelete ] 
   )
   del Filter_Dict[ keyToDelete ]


def EditFilter( ):
   pass

def RunSearch( ):
   global spellDBFiletered
   global Filter_Dict
   # Determine if any spells match the regex of the input
   tmpSpellList = []
   for i in spellDBFiletered :
      # Check EACH element of the current list.
      # If any check fails, break from the check
      for filterType in Filter_Dict :
         if not re.search( Filter_Dict[ filterType ], i[ filterType ], flags=re.IGNORECASE ) :
            break
      # If ALL checks pass, we execute the else and append the spell
      else:
         tmpSpellList.append( i )


   tmpSpellList = sorted( tmpSpellList, key = lambda x: x['name'] )

   for i in tmpSpellList:
      if ( Verbosity > 0 ):
         print
      PrettyPrintSpell( i, Verbosity )


   if( not len( tmpSpellList ) ):
      print "No Spells found that match"
   else:
      print "Found {} spells".format( len( tmpSpellList ) ) 
   raw_input( "Press enter to continue..." )

def ClearScreen( ):
   try:
      os.system('clear')
   except:
      os.system('cls')


def Main( ):
   global Filter_Dict
   global spellDBFiletered

   Filter_Dict = {}

   with open( 'spell_full.csv' ) as fp:
      csvreader = csv.DictReader( fp )
      columns = csvreader.fieldnames
      spellDB = []
      for i in csvreader:

         # Attempt to convert the elements in the row to ints
         # This caused regex to shit builder grade bricks, removed
         # for x in i:
         #    try:
         #       i[x] = int( i[x] )
         #       continue
         #    except ValueError:
         #       pass


         # Append the converted row to the spell DB
         spellDB.append( i )


   spellDBFiletered = [ i for i in spellDB if i['source'] in sourceFilterList ]

   from pprint import pprint

   for i in range(3):
      pprint( spellDBFiletered[i] )

   User_Selection_Raw = ""
   PrintHelpString()
   while( True ):
      ClearScreen()
      print "\n\n<<< Main Menu >>>"
      print "h: help"
      print
      DisplayCurrentFilter()
      print
      print "Enter Command, or press enter to search"
      User_Selection_Raw = raw_input( "> " )

      # Determine if this was a control statement, respond and loop
      if ( User_Selection_Raw in [ 'x', 'X', 'q', 'Q' ] ): 
         break

      if User_Selection_Raw == 'v' :
         ChangeVerbosity()
         continue

      if User_Selection_Raw == 'a' :
         AddFilter()
         continue

      if User_Selection_Raw == 'r' :
         RemoveFilter()
         continue

      if User_Selection_Raw == 'e' :
         EditFilter()
         continue

      if User_Selection_Raw in [ 'h', '?' ] : 
         PrintHelpString()
         continue

      if len( User_Selection_Raw ) == 0 :
         RunSearch()
         continue

      print "WTF was that? I don't know what to do with '{}'".format( User_Selection_Raw )
      print "You come back when you know what you're doing!"



Main()


"""

   name
   school
   subschool
   descriptor
   spell_level
   casting_time
   components
   costly_components
   range
   area
   effect
   targets
   duration
   dismissible
   shapeable
   saving_throw
   spell_resistence
   description
   description_formated
   source
   full_text
Components
   verbal
   somatic
   material
   focus
   divine_focus
Class   
   sor
   wiz
   cleric
   druid
   ranger
   bard
   paladin
   alchemist
   summoner
   witch
   inquisitor
   oracle
   antipaladin
   magus
   adept
   deity

   SLA_Level
   domain
   short_description
Type
   acid
   air
   chaotic
   cold
   curse
   darkness
   death
   disease
   earth
   electricity
   emotion
   evil
   fear
   fire
   force
   good
   language_dependent
   lawful
   light
   mind_affecting
   pain
   poison
   shadow
   sonic
   water

   linktext
   id
   material_costs
   bloodline
   patron
   mythic_text
   augmented
   mythic
"""
