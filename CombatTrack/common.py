from datetime import datetime,timedelta

class Player( object ):
   def __init__( self ):
      self.Name = "BLANK"
      self.Active = False
      self.Initiative = 0.0
      self.TimeTaken = timedelta(0)
      self.TurnStart = None
      self.Turns = 0
      self.Status = {}

   def GetStr( self, localTotalT = None ): 
      if ( localTotalT ):
         per = ( self.SoftUpdate().total_seconds() / localTotalT.total_seconds() * 100. )
      else:    
         per = 0.0

      timeOutput = DeltaTruncate( self.SoftUpdate() )
      if ( self.Turns ):
         avgTurn = DeltaTruncate( self.SoftUpdate() / self.Turns )
      else:
         avgTurn = timedelta( 0 )

      return "%6s %12s (%2d)  %s (%5.2f%%) %s %5d"%(
         ">>>" if self.Active else "   ",
         self.Name, 
         self.Initiative,
         timeOutput,
         per,
         avgTurn,
         self.Turns
         )

   def GetStrDict( self, localTotalT = None):
      if ( localTotalT ):
         per = ( self.SoftUpdate().total_seconds() / localTotalT.total_seconds() )
      else:    
         per = 0.0

      timeOutput = DeltaTruncate( self.SoftUpdate() )
      if ( self.Turns ):
         avgTurn = DeltaTruncate( self.SoftUpdate() / self.Turns )
      else:
         avgTurn = timedelta( 0 )

      localActive = ">>>" if self.Active else ""

      return { "Active":localActive,
         "Name":self.Name,
         "Init":self.Initiative,
         "TTime":timeOutput,
         "PTime":per,
         "ATime":avgTurn,
         "Turns":self.Turns,
         "Status":self.Status,
         }

   def Update( self ):
      """
      WARNING: This attempts to end the players turn if it can!

      Force update of Player. If a turn hasn't started for this character, 
         return without changes. 

      If a turn has begun, calculate the TimeTaken stat with any new time taken
         this turn. Set Active to False to complete the turn, and clear out
         the TurnStart variable to prevent more time buildup. 
      """
      if ( self.TurnStart == None ):
         return

      self.TimeTaken += datetime.now() - self.TurnStart
      self.Active = False
      self.TurnStart = None

   def SoftUpdate( self ):
      if ( self.TurnStart == None ):
         return self.TimeTaken

      return self.TimeTaken + ( datetime.now() - self.TurnStart )

   def GetTimeTaken( self ):
      if ( self.TurnStart != None ):
         return self.TimeTaken + ( datetime.now() - self.TurnStart )
      else:
         return self.TimeTaken

   def BeginTurn( self ):
      """
      Begins turn for player. 

      Will do the following:
         - Update any Status Effects, including deleting any with 0 turns left!
            This breaks Pathfinder rules by changing the Status on the players 
               turn. This might have wierd effects and should be paid attention
               to during gameplay. 
         - Set Player to Active
         - Incriment the number of turns
         - Save a new Turn Start date. 
      """

      assert( self.Active == False ),"A player tried to begin a turn \
      even through they were already active..."

      keysToDelete = []
      for key in self.Status :
         # If this key is already zero, we are done. Delete it!
         if self.Status[key] == 0 :
            keysToDelete.append( key )
            continue
         # We dont want to deal with -1 keys, as they are indeffinate. 
         if self.Status[key] > 0 :
            self.Status[key] -= 1
      
      for i in keysToDelete :
         del self.Status[i]


      self.Active = True
      self.Turns += 1
      self.TurnStart = datetime.now()

   def AddStatus( self, key, turns ) :
      """
      Append the given status (given as a string key) to the STatus dict. 
      
      Status will be saved for 'turns' turns. 

      A negative value for turns will make the status perminent. 
      """
      assert( type( key ) == str )
      assert( type( turns ) == int )

      self.Status[key] = turns

   def Clear( self ):
      self.Active = False
      self.TurnStart = None
      self.Turns = 0
      self.TimeTaken = timedelta( 0 )


def DeltaTruncate( TD ):
   assert( type(TD) == timedelta )
   return timedelta( seconds = int( TD.total_seconds() ) )
