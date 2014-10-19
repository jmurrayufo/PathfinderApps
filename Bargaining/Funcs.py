
import numpy as np
from math import log10, floor

def Round_to_n(x,n=1):
   return round( x, -int( floor( log10( x ) ) - ( n - 1 ) ) )

def D20( ):
   sides = range(1,21)
   return np.random.choice( sides )

def GetLegalInt( prompt="> " ):
   while 1:
      try:
         return int( input( prompt ) )
      except (ValueError):
         continue

def GetLegalFloat( prompt="> " ):
   while 1:
      try:
         return float( input( prompt ) )
      except (ValueError):
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

if __name__ == '__main__' :
   print D20()