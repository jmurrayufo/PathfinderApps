#!/usr/bin/env python

import numpy as np
import time

sided = 20

maxLoops = int( 10e6 )

def GetLoops( pFactor = 0.9 ) :
   assert( pFactor != 1 )
   loops = 0
   p = np.ones(sided,dtype=float)
   p /= sum( p )

   base  = np.zeros(sided,dtype=int)

   while xrange( maxLoops ) :
      loops += 1
      side = np.random.choice( range(0,sided), 1, p=p )[0]
      
      p[side] *= pFactor
      
      p /= sum( p ) 
      
      for i in p:
         if i > 0.999 :
            return loops
   

samples = []
tStart = time.time()
stdDev = 0
mean = 0
max_ = 0
min_ = 0
goodToExit = 10
good = 0

accFactor = 0.001

tgtpFactor = 2


while 1 :
   if len( samples ) :
      stdDev = np.std( samples )
      mean = np.mean( samples )
      max_ = np.max( samples )
      min_ = np.min( samples )

   samples.append( GetLoops( tgtpFactor ) )

   print samples[-1]

   if len( samples ) < 2 :
      print "Not Long Enough"
      good = 0
      continue

   if np.max( samples ) > max_ :
      print "New Max"
      good = 0
      continue

   if np.min( samples ) < min_ :
      print "New Min"
      good = 0
      continue

   if abs( np.mean( samples ) - mean ) > np.mean( samples ) * accFactor :
      print "Mean changed too much: {} > {}".format( abs( np.mean( samples ) - mean ), np.mean( samples ) * accFactor )
      good = 0
      continue

   if abs( np.std( samples ) - stdDev ) > np.mean( samples ) * accFactor :
      print "STD Changed too much: {} > {}".format( abs( np.std( samples ) - stdDev ), np.mean( samples ) * accFactor )
      good = 0
      continue
   good += 1
   print "Good {}".format( good )
   if good >= goodToExit :
      break

print np.mean( samples )
