#!/usr/bin/env python

import numpy as np
import time

sided = 20

p = np.ones(sided,dtype=float)
p /= sum( p )

count = np.zeros(sided,dtype=int)
base  = np.zeros(sided,dtype=int)


expected = 0
loops = 0
rollover = 0

try:
   while 1 :
      loops += 1
      side = np.random.choice( range(0,sided), 1, p=p )[0]
      side2 = np.random.choice(range(0,sided))
      idx = np.where( p == max(p) )[0][0]
      # print "{:2} {:6.2%}    expected {:2} {:6.2%}".format( side+1, p[side], idx+1, p[idx]  )
      print "{:2}   {:2}".format( side + 1, side2 + 1 )
      if p[side] > 0.05 :
         expected += 1
      count[side] += 1
      base[side2] += 1

      p[side] *= 1.1
      
      p /= sum( p ) 
      
      rollover += 1
      if rollover > 1000 :
         for i in p:
            print "{:.2%} ".format(i),
            pass
         print
         rollover = 0
      for i in p:
         if i > 0.999 :
            raise KeyboardInterrupt
except (KeyboardInterrupt) :
   pass
   

# print count
# print p
#print "\nLeft Side:"
#print "STD:",np.std( count )
#print "MAX:",np.max( count )
#print "MIN:",np.min( count )
#print "DIF:",np.max( count ) - np.min( count )

#print "\nRight Side:"
#print "STD:",np.std( base )
#print "MAX:",np.max( base )
#print "MIN:",np.min( base )
#print "DIF:",np.max( base ) - np.min( base )

print "Loops:",loops
