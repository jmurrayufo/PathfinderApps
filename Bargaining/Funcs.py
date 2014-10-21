
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
   # def Interpolate( x0, x1, y0, y1, x ):
   #    return y0 + (y1-y0) * (x-x0) / (x1-x0)
   # print " Munshkined:",Interpolate( 1, 10, 8, 35, Level )
   # print "    Powered:",Interpolate( 1, 10, 6, 19, Level )
   # print "Points Only:",Interpolate( 1, 10, 4, 12, Level )
   # print "    Partial:",Interpolate( 1, 10, 4,  7, Level )
   # print "    Minimal:",Interpolate( 1, 10, 1,  4, Level )
   retVal = []
   retVal.append( int( round( np.interp( Level, [1,20],[ 8,35] ) ) ) )
   retVal.append( int( round( np.interp( Level, [1,20],[ 6,20] ) ) ) )
   retVal.append( int( round( np.interp( Level, [1,20],[ 4,12] ) ) ) )
   retVal.append( int( round( np.interp( Level, [1,20],[ 4, 7] ) ) ) )
   retVal.append( int( round( np.interp( Level, [1,20],[ 1, 4] ) ) ) )
   return retVal

if __name__ == '__main__' :

   print SkillChecks( 20 )

