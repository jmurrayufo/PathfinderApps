#!/usr/bin/env python

import numpy as np
import time

sides = {}

for i in range(1,21):
   sides[i] = 1.0

count = np.zeros(20)

p = np.array([sides[x] for x in sides])
p /= sum(p)


for i in range(500000):
   result = np.random.choice(sides.keys(),p=p)
   count[ result-1 ] += 1
   continue
   sides[ result ] *= 0.95 
   # Recalculate Prob
   p = np.array([sides[x] for x in sides])
   p /= sum(p)
   continue
   print result
   print p
   time.sleep(1)
print p

for idx,val in enumerate( count ):
   print "{:2}: {:,.0f}".format( idx,val )

print "std: {}".format( np.std(count ) )
print "min: {}".format( np.min(count ) )
print "max: {}".format( np.max(count ) )
