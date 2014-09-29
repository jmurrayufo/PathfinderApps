import csv
import time
import textwrap

# Options

# Source Filter List
sourceFilterList = [ 'Ultimate Magic', 'Ultimate Combat', 'Advanced Race Guide',
   'APG', 'PFRPG Core', ]

# Level of verbose output
# 0: Absolute minimum
# 1: Basic Spell Info
# 2: Castable Spell Info
# 3: Full Spell Info
Verbosity = 3


SpellList = [

   # Spell Level 0
   [
      "Acid Splash",
      "Brand",
      "Create Water",
      "Guidance",
      "Light",
      "Read Magic",
      "Resistance",
      "Sift",
      "Stabilize",
   ],

   # Spell Level 1
   [
      "Lend Judgment",
      "Disguise Self",
      "Know The Enemy",
      "Litany of Sloth",
      "Remove Fear",
      "True Strike",
      "Vocal Alteration",
   ],

   # Spell Level 2
   [         
      "Brow Gasher",
      "Castigate",
      "Confess",
      "Discovery Torch",
      "Hold Person",
      "Howling Agony",
      "Invisibility",
      "See Invisibility",
   ],

   # Spell Level 3
   [
      "Dispel Magic",
      "Litany Of Eloquence",
      "Locate Object",
      "Righteous Vigor",
      "Searing Light",
      "Speak with Dead",
      "Terrible Remorse",
   ],
   
   # Spell Level 4
   [
      "Find Quarry",
      "Judgment Light",
      "Litany of Escape",
      "Sending",
      "Freedom of Movement",
      "Restoration",
      "Sanctify Armor",
   ],

   # Spell Level 5
   [
      "Telepathic Bond",      
      "Flame Strike",
      "True Seeing",
      "Divine Pursuit",
   ],
]

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
      print '\n'.join( textwrap.TextWrapper(subsequent_indent='                 ').wrap(tmp) )
   
   elif( detailLevel >= 3 ):
      tmp = outputStr%("Description",inputEntry['description'])
      print '\n'.join( textwrap.TextWrapper(subsequent_indent='                 ').wrap(tmp) )
     
      print outputStr%("Source",inputEntry['source'])


with open( 'spell_full.csv' ) as fp:
   csvreader = csv.DictReader( fp )
   columns = csvreader.fieldnames
   spellDB = []
   for i in csvreader:

      # Attempt to convert the elements in the row to ints
      for x in i:
         try:
            i[x] = int( i[x] )
         except ValueError:
            pass

      # Append the converted row to the spell DB
      spellDB.append( i )

spellDBFiletered = [ i for i in spellDB if i['source'] in sourceFilterList ]

# import pprint
# pprint.pprint( spellDBFiletered[0] )

for index,Spell in enumerate( SpellList ):
   print "\n\n<<<<<              >>>>>"
   print "<<<<< Spell List %d >>>>>"% index
   print "<<<<<              >>>>>"
   SpellSet = [ i for i in spellDBFiletered if i['name'] in Spell ]
   for i in sorted( SpellSet, key = lambda i: i['name'] ):
      if( Verbosity > 0 ):
         print
      PrettyPrintSpell( i, Verbosity )

# Find Bad Spells
print "\nChecking for bad spell names..."
for index,val in enumerate( SpellList ):
   for spell in val:
      result = [ x for x in spellDBFiletered if x['name'] == spell]
      if not result:
         print "Spell Level:",index
         print spell