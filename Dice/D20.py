#!/usr/bin/env python
import numpy as np
from numpy.random import random, choice, random_integers
import time
import scipy.stats

D6 = {}
D6[1] = [2,3,5,4]
D6[2] = [6,3,5,1]
D6[3] = [4,6,2,5]
D6[4] = [6,3,5,1]
D6[5] = [6,2,4,1]
D6[6] = [2,3,4,5]


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

def ProoveRandom(tTotal):
   tStart = time.time()
   Count = np.zeros(20,dtype=int)
   while time.time() - tStart < tTotal :
      speed = 15
      side = choice( mapping.keys() )
      last = side
      while speed > 0.5 :
         tmplist = [x for x in mapping[side] if x != last]
         last = side
         side = choice( tmplist )
         speed -= random() * 5
      Count[side-1]+=1
   
   print "Bins:",Count
   print "Total Rolls:",sum(Count)
   print "STD:",np.std(Count)
   total = 0
   for side,val in enumerate( Count ):
      total += (side+1)*val
   print "Average:",total/float( sum(Count) )
   cresults = scipy.stats.chisquare( Count )
   print "ChiSquared: {:.2%}".format(cresults[1])

if __name__ == '__main__' :
   print "We will first take a moment to proove that we are random!"
   ProoveRandom(5)
   print "Now to the roller\n"
   while 1:
      speed = 15
      side = choice( mapping.keys() )
      last = side
      while speed > 0.5 :
         tmplist = [x for x in mapping[side] if x != last]
         last = side
         side = choice( tmplist )

         print "\n{:5}".format( side )
         time.sleep(1.0/speed)
         speed -= random() * 5

      print "Almost got:",mapping[side]
      try:
         raw_input( "Press enter to roll again..." )
      except (EOFError):
         exit()
      print
