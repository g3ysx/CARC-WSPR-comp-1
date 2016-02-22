import sys
from collections import Counter

print('CARC WSPR Competition Adjudicator')
print

mc = [] # member call
mcw = []  # member country worked
mzw = [] # member zone worked
msqw = [] # member square worked
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
   msqw.append([])
   mrxband.append([])
   mtxband.append(md[1].strip())
   mp.append([])

of = open('observers.txt', 'r')
mo = open('missing-observers.txt', 'w')
for o in of:
   od = o.split(',')
   print o
   oc.append(od[0].rstrip().upper())
   oz.append(str(int(od[1].rstrip())))
   oe.append(str(int(od[2].rstrip())))
   if int(od[1].rstrip()) == 999:
      mo.write(o)

if len(sys.argv)==1:
   print "Usage: CWCA.py <wsprSpotsFile>"
   sys.exit()

spotsFile = sys.argv[1]
print 'Spots file = ', spotsFile
f = open(spotsFile, 'r')
for l in f:
   ls = l.split(',')
   if ls[6] in mc :
      if ls[2] in oc:
         band = freqtoband(ls[5])
         if band <> 'REJECT':        
            obs=oc.index(ls[2])
            mem=mc.index(ls[6])
            mrxband[mem].append(band)
            if mtxband[mem] != 'ALL': # correct the slots for the single band entrants
               band = mtxband[mem]
            uniqueappend(msw[mem], band+oe[obs])
            uniqueappend(mzw[mem], oz[obs])
            uniqueappend(mcw[mem], oe[obs])
            uniqueappend(te,oe[obs])
            mp[mem].append(int(ls[8]))
            sq = ls[3][:2]
            uniqueappend(msqw[mem], sq)
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

sm = [] #scoring member
nsm = 0 #num scoring members
cq_score = 0
mh_score = 0

for m in mc:
   mem = mc.index(m)
   if  len(mzw[mem]) > 0:
      mzw[mem] = [int(z) for z in mzw[mem]] #convert zones to int
      mzw[mem].sort(key=int)
      cq_score = len(mzw[mem])*len(msw[mem])
      mh_score = len(msqw[mem])*len(msw[mem])
      print m,  'Score = CQ zones x band slots =', cq_score
      print 'Countries (Entities) heard in =', len(mcw[mem]), ', Band slots =', len(msw[mem]), ', CQ zones =', len(mzw[mem])
      b = str(Counter(mrxband[mem]))
      b = b[9:-2] # trim the beginning and end of the Counter standard format
      b = b.replace("'","") # get rid of the quote char from Counter standard format
      print 'Number of times reported on the following bands', b
      c = str(Counter(mp[mem]))
      c = c[9:-2]
      print "Number of times reported at following power in dBm", c
      print 'Number of Maidenhead large squares heard in =', len(msqw[mem])
      print 'Maidenhead score = M Sq * band slots =', mh_score
      print 'Maidenhead squares are : ',
      msqw[mem].sort()
      for sq in msqw[mem]:
         print sq+',',
      print
      print 'CQ Zones are : ',
      for z in mzw[mem]:
         print z,',',
      print
      print
      nsm = nsm + 1 #num scoring members
      sm.append([m, cq_score, mh_score])

print
print
print 'Number of observers that heard us =', len(oc)
print 'Total countries worked', len(te)


sm = sorted(sm,key=lambda x: x[1], reverse=True)

print
print
print 'Posn\tMember\tCQscore\tMHscore'
print 

for m in sm:
   print sm.index(m)+1,'\t',m[0], '\t', m[1], '\t', m[2] 



 












