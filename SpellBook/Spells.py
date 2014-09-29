import csv
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
      "Deadeyes Lore",
      "Disguise Self",
      "Know the Enemy",
      "Litany of Sloth",
      "Remove Fear",
      "True Strike",
      "Vocal Alteration",
   ],
   # Spell Level 2
   [         
      "Brow Gasher",
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
      "Locate Object",
      "Speak with Dead",
      "Terrible Remorse",
   ],
   # Spell Level 4
   [
      "Litany of Escape",
      "Sending",
   ]
]

def PrettyPrintSpell( inputEntry, detailLevel = 0 ):
   if( detailLevel == 0 ):
      outputStr = "%s: %s"
   if( detailLevel == 1 ):
      outputStr = "%12s: %s"
   if( detailLevel >= 2 ):
      outputStr = "%16s: %s"
   print outputStr%('Name',inputEntry['name'])
   if( detailLevel == 0 ):
      return
   print outputStr%('Components',inputEntry['components'])
   print outputStr%('Duration',inputEntry['duration'].capitalize( ) )
   print outputStr%('Casting Time',inputEntry['casting_time'].capitalize( ) )
   print outputStr%('Saving Throw', inputEntry['saving_throw'].capitalize( ) )
   if( detailLevel >= 2 ):
      print outputStr%('Spell Level',inputEntry['spell_level'] )
      print outputStr%('Spell Resistance', inputEntry['spell_resistence'].capitalize( ) )
      print outputStr%('School',inputEntry['school'].capitalize( ) ),
      if( inputEntry['subschool'] ):
         print "( %s )"%( inputEntry['subschool'] )
      else:
         print
   print outputStr%('Targets',inputEntry['targets'].capitalize( ) )
   if( detailLevel > 0 and detailLevel < 3 ):
      print outputStr%('Description',inputEntry['short_description'])
   elif( detailLevel >= 3 ):
      print outputStr%("Description",inputEntry['description'])
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

for index,Spell in enumerate( SpellList ):
   print "\n\n<<<<<              >>>>>"
   print "<<<<< Spell List %d >>>>>"% index
   print "<<<<<              >>>>>"
   for i in [ i for i in spellDBFiletered if i['name'] in Spell ]:
      print
      PrettyPrintSpell( i, Verbosity )