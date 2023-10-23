#!/usr/bin/python

import os
import time
import signal
from subprocess import check_output as call

known_ones = {
   'A': 'Ambient',
   'C': 'CPU',
   'N': 'Northbridge',
   'G': 'GPU',
   'M': 'Memory',
   }

wheres = {
   'P': 'Proximity',
   'V': 'Vent',
   'H': 'Heatsink',
   'D': 'Die',
   'C': 'Core',
   'R': 'Rail',
   }

fan_where = {
   'Ac': 'Current',
   'Tg': 'Target',
   'Mn': 'Min',
   'Mx': 'Max',
   'Sf': 'Safe',
   }

def key2header(key):
   if key[0] == 'F': # Fan
      where = fan_where[key[2:4]] if key[2:4] in fan_where else key[2:4]
      return f"Fan_{key[1]}_{where}_RPM"
   else:
      who = known_ones[key[1]] if key[1] in known_ones else key[1]
      where = wheres[key[3]] if key[3] in wheres else key[3]
      return f"{key[0]}_{who}_{key[2]}_{where}"

DEFAULT_LIST = [
   'F0Ac', 'F0Tg',
   'TA0P', 'TA0V',
   'TA1P', 'TA2P',
   'TC0P', 'TC0c',
   'TC1c', 'TC2c', 'TC3c', 'TCXc',
   'TG0P', 'TG1P',
   'TG0r', 'TG1r',
   'PC0C', 'PC0S',
   'PCPC', 'PCPT', 'PCTR',
   'PG0C', 'PG0S', 'PG0R',
   'PG1C', 'PG1S', 'PG1R',
   'VC0C', 'VC0S',
   'VCTR',
   'VG0C', 'VG0S', 'VG0R',
   'VG1C', 'VG1S', 'VG1R',
   'VH0R', 'VI1R',
   'IC0C', 'IC0S',
   'ICTR', 'ICTX',
   'IG0C', 'IG0S', 'IG0R',
   'IG1C', 'IG1S', 'IG1R',
   'IH0R', 'II0R',
]

exit_requested = False

def ctrlc_handler(signum, frame):
   global exit_requested
   exit_requested = True

def main():
   mypath = os.path.dirname(os.path.realpath(__file__))
   signal.signal(signal.SIGINT, ctrlc_handler)
   a = DEFAULT_LIST
   headers = [key2header(x) for x in a]
   print ','.join(['time'] + headers)
   start = time.time()
   while True and not exit_requested:
      s = call(['%s/smcprint'%mypath] + a)
      print "%f,%s"%(time.time()-start, s.strip())
      time.sleep(.5)

main()

