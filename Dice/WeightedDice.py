#!/usr/bin/env python

import numpy as np
import time

p = np.ones(20,dtype=float)
p /= sum( p )

count = np.zeros(20,dtype=int)

totalLoops = 100000
expected = 0

for i in range( totalLoops ) :

   side = np.random.choice( range(0,20), 1, p=p )[0]
   idx = np.where( p == max(p) )[0][0]
   # print "{:2} {:6.2%}    expected {:2} {:6.2%}".format( side+1, p[side], idx+1, p[idx]  )
   print "{:2}".format( side + 1 )
   if p[side] > 0.05 :
      expected += 1
   count[side] += 1
   p[side] *= 0.1
   p /= sum( p ) 
   time.sleep(1)
   

print count
print p

print "STD:",np.std( count )
print "MAX:",np.max( count )
print "MIN:",np.min( count )
print "DIF:",np.max( count ) - np.min( count )
print "EXP:",expected/float(totalLoops)
