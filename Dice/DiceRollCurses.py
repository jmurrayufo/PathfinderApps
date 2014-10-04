#!/usr/bin/env python
from random import randint,uniform
from time import sleep
import curses


def Main( window ):
   curses.curs_set(0)   
   (y,x) = window.getmaxyx()
   while True :
      sides = 20
      
      pause = 0.0
      total = uniform( 0.5, 2.0 )
      while pause < total :
         window.clear()
         roll = randint( 1, sides )
         window.addstr( y/2, x/2,  "{:>2}".format( roll ) )
         pause += uniform( 0, max( .01, pause ) )
         window.refresh()
         sleep( pause )
      

      window.addstr( y/2, x/2,  '{:>2}'.format( roll )  )
      window.addstr( y/2+1, x/2,  "**" )
      window.addstr( y/2-1, x/2,  "**" )
      window.refresh()
      if window.getkey() == 'x' :
         break
try:
   curses.wrapper( Main )
finally:
   curses.nocbreak()
   curses.echo()
   curses.endwin()
