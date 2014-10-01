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
   print "Help!"
   print "x: Exit"
   print "h: This help statement"
   print "v#: Change verbosity"
   print "   v0: Absolute minimum"
   print "   v1: Basic Spell Info"
   print "   v2: Castable Spell Info"
   print "   v3: Full Spell Info"
   print "Current Verbosity: {}".format( Verbosity )
   

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



PrintHelpString()
Prev_User_Selection_Raw = ""
User_Selection_Raw = ""
while( True ):

   Prev_User_Selection_Raw = User_Selection_Raw

   User_Selection_Raw = raw_input( "> " )


   # Determine if this was a control statement, respond and loop
   if ( User_Selection_Raw in [ 'x', 'X', 'q', 'Q' ] ): 
      break

   tmp = re.match( "[vV](\d+)", User_Selection_Raw ) 
   if ( tmp ):
      print "Verbosity Changed to", int( tmp.groups()[0] )
      Verbosity = int( tmp.groups()[0] )
      continue

   if ( User_Selection_Raw in [ 'h', 'H', '?', '?' ] or len( User_Selection_Raw ) == 0 ): 
      PrintHelpString()
      continue

   try:
      re.compile( User_Selection_Raw )
   except sre_constants.error, e:
      print "Your regex had the following error:",e
      print "Dont do that!"
      continue

   # Take previous input if nothing is given
   if ( not len( User_Selection_Raw ) ):
      User_Selection_Raw = Prev_User_Selection_Raw
      # STILL no input? ok, %$#% this, NEXT!
      if ( not len( User_Selection_Raw ) ):
         continue



   # Determine if any spells match the regex of the input
   tmpSpellList = []
   for i in spellDBFiletered:
      if ( re.match( User_Selection_Raw, i['name'], flags=re.IGNORECASE ) ):
         tmpSpellList.append( i )

   tmpSpellList = sorted( tmpSpellList, key = lambda x: x['name'] )

   for i in tmpSpellList:
      if ( Verbosity > 0 ):
         print
      PrettyPrintSpell( i, Verbosity )

   # Nothing happened? Make fun of the user and loop

   if( not len( tmpSpellList ) ):
      print "You suck at this!"
      print "We could not find any spells with \"%s\" in them."%( User_Selection_Raw )



