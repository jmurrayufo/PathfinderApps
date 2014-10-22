import numpy as np
import scipy as sp
import scipy.stats
import time
from matplotlib import pyplot as plt


def mean_confidence_interval(data, confidence=0.95):
    a = 1.0*np.array(data)
    n = len(a)
    m, se = np.mean(a), scipy.stats.sem(a)
    h = se * sp.stats.t._ppf((1+confidence)/2., n-1)
    return m, m-h, m+h, h

sides = np.zeros(20,dtype=int)

while 1:
   print "Next..."
   try:
      roll = input("> ")
   except (ValueError,SyntaxError):
      continue
   except (KeyboardInterrupt):
      break
   sides[roll-1]+=1
   print scipy.stats.chisquare( sides )
   for idx,val in enumerate( sides ) :
      print "{}:{} ".format(idx+1,val),
   print
   print mean_confidence_interval( sides )
   print

x = [x-.4 for x in range(1,21)]

plt.bar( x, sides )
plt.show()