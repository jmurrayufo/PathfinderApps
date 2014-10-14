#!/usr/bin/env python

import numpy as np
import time

sided = 10

p = np.ones(sided,dtype=float)
p /= sum( p )

count = np.zeros(sided,dtype=int)
base  = np.zeros(sided,dtype=int)

totalLoops = 10000
expected = 0

for i in range( totalLoops ) :

   side = np.random.choice( range(0,sided), 1, p=p )[0]
   side2 = np.random.choice(range(0,sided))
   idx = np.where( p == max(p) )[0][0]
   # print "{:2} {:6.2%}    expected {:2} {:6.2%}".format( side+1, p[side], idx+1, p[idx]  )
   print "{:2} {:2}".format( side + 1, side2 + 1 )
   if p[side] > 0.05 :
      expected += 1
   count[side] += 1
   base[side2] += 1

   p[side] *= 0.1
   
   p /= sum( p ) 
   time.sleep(0.1)
   

# print count
# print p
print "\nWeighted:"
print "STD:",np.std( count )
print "MAX:",np.max( count )
print "MIN:",np.min( count )
print "DIF:",np.max( count ) - np.min( count )

print "\nBalanced:"
print "STD:",np.std( base )
print "MAX:",np.max( base )
print "MIN:",np.min( base )
print "DIF:",np.max( base ) - np.min( base )