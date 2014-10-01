#!/usr/bin/env python
import csv
import time
import textwrap
import re
import sre_constants
import readline

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
   print "x: Exit"
   print "h: This help statement"
   print "v: Change verbosity"

   print "a: Add a Filter"
   print "r: Remove a Filter"
   print "e: Edit a Filter"
   
   print "Enter: Search & Display"
   print "Current Verbosity: {}".format( Verbosity )
   
def ChangeVerbosity( ):
   global Verbosity

   print "\nEnter new Verbosity Setting"
   print "0 => Name Only"
   print "1 => Gameplay Details"
   print "2 => Casting Details"
   print "3 => Full Details"
   print "4 => OMFG (Not yet supported)"

   try :
      Verbosity = input( "> " )
   except :
      return

   try :
      Verbosity = int( Verbosity )
   except ValueError :
      Verbosity = 1

   return


def AddFilter( ):
   global completionList
   global Filter_Dict
   # Select type of Filter to add
   allowedFilterTypes = [ 'name',
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
   # Deep copy that thing!
   completionList = list( allowedFilterTypes )
   readline.parse_and_bind( "tab: complete" )
   readline.set_completer( completer )
   
   print "\nSelect Filter Type:"
   filterType = raw_input( "> " )
   if filterType not in allowedFilterTypes :
      completionList = []
      readline.set_completer( completer )
      return False
   
   print "\nEnter value to filter by (valid regex)"
   filterValue = raw_input( "> " )
   try:
      re.compile( filterValue )
   except sre_constants.error, e:
      completionList = []
      readline.set_completer( completer )
      return False

   Filter_Dict[ filterType ] = filterValue
   return True



def RemoveFilter( ):
   pass

def EditFilter( ):
   pass

def RunSearch():
   global spellDBFiletered
   global Filter_Dict
   # Determine if any spells match the regex of the input
   tmpSpellList = []
   for i in spellDBFiletered :
      for filterType in Filter_Dict :
         if re.match( Filter_Dict[ filterType ], i[ filterType ], flags=re.IGNORECASE ) :
            tmpSpellList.append( i )

   tmpSpellList = sorted( tmpSpellList, key = lambda x: x['name'] )

   for i in tmpSpellList:
      if ( Verbosity > 0 ):
         print
      PrettyPrintSpell( i, Verbosity )

   if( not len( tmpSpellList ) ):
      print "No Spells found that match"

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
         for x in i:
            try:
               i[x] = int( i[x] )
               continue
            except ValueError:
               pass


         # Append the converted row to the spell DB
         spellDB.append( i )


   spellDBFiletered = [ i for i in spellDB if i['source'] in sourceFilterList ]

   User_Selection_Raw = ""
   while( True ):
      PrintHelpString()

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
Supported Filters:
   name
Unsupported Filters:

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
   verbal
   somatic
   material
   focus
   divine_focus
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
