import sys
from collections import Counter

print('CARC WSPR Competition Adjudicator')
print

mc = [] # member call
mcw = []  # member country worked
mzw = [] # member zone worked
msw = [] # slot = band + country
mrxband = [] #bands heard on
mtxband = [] #bands transmitting on
mp = [] # member power
te = [] # total entities worked by club members

oc = [] #observers call
oe = [] #observers entity
oz = [] #observers zone

misso = [] # missing observers

obsIncomplete=False


def uniqueappend(list, val):
   if val not in list:
      list.append(val)
   return

def freqtoband(freq):
   f=float(freq)
   if f < 0.002:
      return('REJECT')
   if f < 0.1:
      print 'unexpected band', freq
      sys.exit(0)
   if f < 0.2:
      return('2200m')
   if f < 0.5:
      return('630m')
   if f < 2.0:
      return('160m')
   if f < 4.0:
      return('80m')
   if f < 6.0:
      return('60m')
   if f < 8.0:
      return('40m')
   if f < 11.0:
      return('30m')
   if f < 15.0:
      return('20m')
   if f < 19.0:
      return('17m')
   if f < 22.0:
      return('15m')
   if f < 25.0:
      return('12m')
   if f < 30.0:
      return('10m')
   if f < 52.0:
      return('6m')
   if f < 71.0:
      return('4m')
   if f < 146.0:
      return('2m')
   if f < 438.0:
      return('70cm')
   if f < 1300.0:
      return('23cm')
   print 'unexpected band', freq
 

mf = open('members.txt', 'r')
for m in mf:
   md = m.split(',')
   mc.append(md[0].rstrip().upper())
   mzw.append([])
   mcw.append([])
   msw.append([])
   mrxband.append([])
   mtxband.append(md[1].strip())
   mp.append([])

of = open('observers.txt', 'r')
mo = open('missing-observers.txt', 'w')
for o in of:
   od = o.split(',')
   print o
   oc.append(od[0].rstrip().upper())
   oz.append(od[1].rstrip())
   oe.append(od[2].rstrip())
   if int(od[1].rstrip()) == 999:
      mo.write(o)

f = open('wsprspots.csv', 'r')
for l in f:
   ls = l.split(',')
   if ls[6] in mc :
      if ls[2] in oc:
         band = freqtoband(ls[5])
         if band <> 'REJECT':        
            obs=oc.index(ls[2])
            mem=mc.index(ls[6])
            if mtxband[mem] != 'ALL':
               band = mtxband[mem]
            uniqueappend(mzw[mem], oz[obs])
            uniqueappend(mcw[mem], oe[obs])
            uniqueappend(msw[mem], band+oe[obs])
            uniqueappend(mrxband[mem], band)
            uniqueappend(te,oe[obs])
            mp[mem].append(int(ls[8]))
      else:
         print "missing observer", ls[2], ls[3]
         if ls[2] not in misso:
            misso.append(ls[2])
            mo.write(ls[2]+' '+ls[3]+'+++'+'\n')
            obsIncomplete=True

if obsIncomplete:
   print 'Unable to adjudicate - incomplete observers list, see missing-observers.txt'
   mo.flush()
   sys.exit(0)

for m in mc:
   mem = mc.index(m)
   if  len(mzw[mem]) > 0:
      print m,  'Score = CQ zones x band slots =', len(mzw[mem])*len(msw[mem])
      print 'Countries (Entities) heard in =', len(mcw[mem]), 'Band slots =', len(msw[mem]), 'CQ zones =', len(mzw[mem])
#      print '   Max Power(dBm) =', mp[mem], 'Bands Operated  =', len(mrxband[mem])
      print 'Bands Operated  =', len(mrxband[mem])
      c = Counter(mp[mem])
      print "Number of times reported at following power in dBm", c
      print

print
print 'Number of observers that heard us =', len(oc)
print 'Total countries worked', len(te)

#print 'Individual Details'
#
#for m in mc:
#   mem = mc.index(m)
#   if  len(mzw[mem]) > 0:
#      print m
#      for bs in msw[mem]:
#               

 












