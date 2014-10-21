
import numpy as np
from math import log10, floor

def Round_to_n(x,n=1):
   frmtString = '{}'.format(n)
   frmtString = "{:."+frmtString+"g}"
   return float( frmtString.format(x) )
   # Old Code
   try:
      return round( x, -int( floor( log10( x ) ) - ( n - 1 ) ) )
   except (ValueError) :
      print "X:",x
      print "N:",n
      raise ValueError

def D20( ):
   sides = range(1,21)
   return np.random.choice( sides )

def GetLegalInt( prompt="> " ):
   while 1:
      try:
         return int( input( prompt ) )
      except (ValueError, NameError, SyntaxError):
         continue

def GetLegalFloat( prompt="> " ):
   while 1:
      try:
         return float( input( prompt ) )
      except (ValueError, NameError, SyntaxError):
         continue

def GetTruth( prompt="> " ):
   while 1:
      tmp = raw_input( prompt )
      if tmp in [ 'y','Y','yes','Yes' ] :
         return True
      elif tmp in [ 'n','N','no','No' ] :
         return False
      else:
         continue

def SkillChecks( Level ) :
   return [
      int( round( np.interp( Level, [1,20],[ 8,60] ) ) ),
      int( round( np.interp( Level, [1,20],[ 6,40] ) ) ),
      int( round( np.interp( Level, [1,20],[ 4,24] ) ) ),
      int( round( np.interp( Level, [1,20],[ 4,14] ) ) ),
      int( round( np.interp( Level, [1,20],[ 1, 8] ) ) ),
      ]

def Attribute( Level ) :
   return [
      int( np.interp( Level, [ 1,4,8,12,16,20 ], [  4, 6, 7, 8, 9,10 ] ) ),
      int( np.interp( Level, [ 1,4,8,12,16,20 ], [  2, 3, 4, 5, 7, 9 ] ) ),
      int( np.interp( Level, [ 1,4,8,12,16,20 ], [  1, 2, 2, 3, 4, 5 ] ) ),
      int( np.interp( Level, [ 1,4,8,12,16,20 ], [  0, 1, 1, 2, 2, 3 ] ) ),
      int( np.interp( Level, [ 1,4,8,12,16,20 ], [ -1,-1,-1, 0, 0, 1 ] ) ),
      ]

if __name__ == '__main__' :
   x = SkillChecks( 4 )
