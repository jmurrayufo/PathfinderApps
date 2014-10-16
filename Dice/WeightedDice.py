#!/usr/bin/env python

import numpy as np
import time

sided = 20

p = np.ones(sided,dtype=float)
p[19] = 5000
p /= sum( p )

count = np.zeros(sided,dtype=int)


loops = 0
rollover = 0

try:
   while 1 :
      loops += 1
      side = np.random.choice( range(0,sided), 1, p=p )[0]
      idx = np.where( p == max(p) )[0][0]
      if idx == side :
         print "{:2} [{:5,.1%}]        Got: {:2} [{:5,.1%}]".format( side+1, p[side], idx+1, p[idx])
      else:
         print "{:2} [{:5,.1%}]   Expected: {:2} [{:5,.1%}]".format( side+1, p[side], idx+1, p[idx])
      count[side] += 1

      p[side] *= 0.5
      
      p /= sum( p ) 
      time.sleep(0.05)
      
except (KeyboardInterrupt) :
   pass
   

print count
print p
print "\nLeft Side:"
print "STD:",np.std( count )
print "MAX:",np.max( count )
print "MIN:",np.min( count )
print "DIF:",np.max( count ) - np.min( count )


print "Loops:",loops
