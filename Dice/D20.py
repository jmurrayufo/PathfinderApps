import numpy as np
from numpy.random import random, choice, random_integers
import time

mapping = {}
mapping[1] =  [ 7,19,13]
mapping[2] =  [12,18,20]
mapping[3] =  [17,16,19]
mapping[4] =  [11,18,14]
mapping[5] =  [13,15,18]
mapping[6] =  [14, 9,16]
mapping[7] =  [ 1,15,17]
mapping[8] =  [10,16,20]
mapping[9] =  [ 6,11,19]
mapping[10] = [12, 8,17]
mapping[11] = [ 4, 9,13]
mapping[12] = [15, 2,10]
mapping[13] = [11, 5, 1]
mapping[14] = [20, 4, 6]
mapping[15] = [ 5, 7,12]
mapping[16] = [ 8, 3, 6]
mapping[17] = [10, 3, 7]
mapping[18] = [ 2, 4, 5]
mapping[19] = [ 1, 9, 3]
mapping[20] = [ 2,14, 8]

def GetRandomSide():
   global mapping
   side = choice( mapping.keys() )
   for i in range( random_integers(1,20) ):
      side = choice( mapping[side])
   return side

speed = 10
side = choice( mapping.keys() )
while speed > 0.4 :
   print "\n{:2}".format( side )
   time.sleep(1.0/speed)
   speed -= random()
   side = choice( mapping[side] )

# results = []
# for i in range( 1000 ):
#    results.append( GetRandomSide() )

# for i in range(1,21):
#    print "{:2}:{:6,}".format(i,results.count(i))

# print np.std( results )
# print np.mean( results )