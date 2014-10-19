#!/usr/bin/env python

import numpy as np
import time

sided = 20

p = np.ones(sided,dtype=float)
p /= sum( p )

count = np.zeros(sided,dtype=int)

def ShowStats( ):
   global count
   global p
   global loops
   
   for idx,(x,y) in enumerate( zip( count, p ) ):
      print "#{:2} Count: {:2}  Odds: {:.2%}".format(idx+1,x,y)
   print "STD:",np.std( count )
   print "MAX:",np.max( count )
   print "MIN:",np.min( count )
   print "DIF:",np.max( count ) - np.min( count )
   print "Loops:",loops
   

loops = 0
rollover = 0

print "Press Enter to roll..."

try:
   while 1 :
      user_sel = raw_input()

      if user_sel in ['u'] :
         ShowStats()
         continue

      loops += 1
      side = np.random.choice( range(0,sided), 1, p=p )[0]
      idx = np.where( p == max(p) )[0][0]
      if idx == side :
         print "{:2} [{:5,.1%}]        Got: {:2} [{:5,.1%}]".format( side+1, p[side], idx+1, p[idx])
      else:
         print "{:2} [{:5,.1%}]   Expected: {:2} [{:5,.1%}]".format( side+1, p[side], idx+1, p[idx])
      count[side] += 1

      p[side] *= 0.7 + np.random.random()*0.1
      
      p /= sum( p ) 

      #time.sleep(0.01)
      
except (KeyboardInterrupt) :
   pass
   
ShowStats()
