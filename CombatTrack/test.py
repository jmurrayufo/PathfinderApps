#!/usr/bin/env python
from datetime import datetime,timedelta
import os
import time
import json
from json import JSONEncoder
import atexit
from common import Player


class PlayerEncoder( JSONEncoder):
   def default(self, o):
      if( type( o ) == Player ):
         d = {}
         d['Name'] = o.Name
         d['Active'] = o.Active
         d['Initiative'] = o.Initiative
         d['TimeTaken'] = o.TimeTaken
         d['TurnStart'] = o.TurnStart
         d['Turns'] = o.Turns
         d['Status'] = o.Status
      elif( type( o ) == datetime ):
         return o.isoformat()
      elif( type( o ) == timedelta ):
         return o.total_seconds()
      else:
         print "Cannot encode!"
         print type(o)
         return o

      return d

def EmergencyReload( ):
   global GLOB_PLAYERS
   with open(".playerdata.json",'r') as fp:
      for i in json.load(fp):
         GLOB_PLAYERS.append(Player())
         GLOB_PLAYERS[-1].Name = i['Name']
         GLOB_PLAYERS[-1].Active = i['Active']
         GLOB_PLAYERS[-1].Initiative = i['Initiative']
         GLOB_PLAYERS[-1].TimeTaken = timedelta( seconds = float( i['TimeTaken'] ) )
         GLOB_PLAYERS[-1].TurnStart = i['TurnStart']
         if( i['TurnStart'] ):
            GLOB_PLAYERS[-1].TurnStart = datetime.strptime( i['TurnStart'] , "%Y-%m-%dT%H:%M:%S.%f")
         GLOB_PLAYERS[-1].Turns = i['Turns']


players = []

mule = Player()

mule.Status['Sleeping'] = 4
mule.Status['Stunned'] = 3
mule.Status['Angry @ Nate'] = -1

players.append(mule)

with open('tmp.json','w') as fp :
   json.dump( players, fp, cls=PlayerEncoder, indent=3)
