import numpy as np
import scipy.stats
import time
from matplotlib import pyplot as plt


fair = np.zeros(20,dtype=int)
cheated = np.zeros(20,dtype=int)
trials = 50

weighting = np.ones(20)
weighting[0] *= 1.05
# for idx in range(10):
   # weighting[idx] *= 1.1 


weighting /= sum( weighting )

# print weighting
# print weighting[0] / weighting[1]

print "Roll Dice"
x = []
y = []
totalTest = 100000
for i in xrange( totalTest ) :
   # fair[ np.random.choice( range(len(fair)) ) ] += 1
   cheated[ np.random.choice( range(len(cheated)), p=weighting ) ] += 1

   # fresults = scipy.stats.chisquare( fair )
   cresults = scipy.stats.chisquare( cheated )
   if( i % 100 ):
      x.append(i)
      y.append( scipy.stats.chisquare( cheated )[1] * 100. )

   # print "Fair: {:6.2%}   Cheated: {:6.2%} ".format( fresults[1], cresults[1] )
   # time.sleep(.1)
# print scipy.stats.chisquare( fair )
print scipy.stats.chisquare( cheated )

plt.bar( range(1,21), cheated )
plt.figure()
plt.semilogy(x,y,'-')
plt.show()