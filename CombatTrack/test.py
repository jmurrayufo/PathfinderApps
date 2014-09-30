#!/usr/bin/env python
from datetime import datetime,timedelta
import os
import time
import json
from json import JSONEncoder
import atexit
from common import Player
from curses.wrapper import wrapper
import curses

def Main( stdscr ):
   stdscr.addstr( ">> " )
   stdscr.refresh()
   localSel = stdscr.getkey()
   stdscr.addstr( localSel )
   stdscr.addstr( "\n" )
   stdscr.addstr( str( type( localSel ) ) )
   stdscr.addstr( "\n"+str( ord( localSel ) ) )

   stdscr.refresh()
   curses.napms(2000)

 
wrapper( Main )
