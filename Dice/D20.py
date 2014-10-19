#!/usr/bin/env python
import numpy as np
from numpy.random import random, choice, random_integers
import time

mapping = {}
mapping[1] =  [ 7,13,19]
mapping[2] =  [12,18,20]
mapping[3] =  [16,17,19]
mapping[4] =  [11,14,18]
mapping[5] =  [13,15,18]
mapping[6] =  [ 9,14,16]
mapping[7] =  [ 1,15,17]
mapping[8] =  [10,16,20]
mapping[9] =  [ 6,11,19]
mapping[10] = [ 8,12,17]
mapping[11] = [ 4, 9,13]
mapping[12] = [ 2,10,15]
mapping[13] = [ 1, 5,11]
mapping[14] = [ 4, 6,20]
mapping[15] = [ 5, 7,12]
mapping[16] = [ 3, 6, 8]
mapping[17] = [ 3, 7,10]
mapping[18] = [ 2, 4, 5]
mapping[19] = [ 1, 9, 3]
mapping[20] = [ 2, 8,14]

def GetRandomSide():
   global mapping
   side = choice( mapping.keys() )
   last = side
   for i in range( random_integers(1,20) ):
      tmplist = [x for x in mapping[side] if x != last]
      last = side
      side = choice( tmplist )
   return side

print "Begin"
speed = 15
side = choice( mapping.keys() )
last = side
while speed > 0.5 :
   tmplist = [x for x in mapping[side] if x != last]
   last = side
   side = choice( tmplist )

   print "\n{:2}".format( side )
   time.sleep(1.0/speed)
   speed -= random() * 5



print "Almost got:",mapping[side]
"""
results = []
for i in range( 1000 ):
   results.append( GetRandomSide() )

for i in range(1,21):
   print "{:2}:{:6,}".format(i,results.count(i))

print np.std( results )
print np.mean( results )

"""
