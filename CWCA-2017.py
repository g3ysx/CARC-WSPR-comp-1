import sys
from collections import Counter

print('CARC WSPR Competition Adjudicator 2017')
print

mc = [] # member call
mcw = []  # member country worked
mow = []  # first observer in country on band
msw = [] # slot = band + country
mrxband = [] #bands heard on
mtxband = [] #bands transmitting on
mp = [] # member power
te = [] # total entities worked by club members

obsWhoHeardUs = [] #observers who heard us
oc = [] #observers call
oe = [] #observers entity
ocountry = [] #observers country

misso = [] # missing observers

obsIncomplete=False



def uniqueappend(list, val):
   if val not in list:
      list.append(val)
      return(True)
   else:
      return(False)


def freqtoband(freq):
   f=float(freq)
   tol = 0.005 #5KHz

   if f>0.136-tol and f<0.136+tol:
      return('2200m')
   if f>0.5 and f<0.51:
      return('+630m') # fixup for spurious observations
   if f>0.4742-tol and f<0.4742+tol:
      return('+630m')
   if f>1.8366-tol and f<1.8366+tol:
      return('+160m')
   if f>3.5926-tol and f<3.5926+tol:
      return('++80m')
   if f>3.5 and f<3.7:
      return('++80m') #Fixup
   if f>5.2872-tol and f<5.2872+tol:
      return('++60m')
   if f>7.0386-tol and f<7.0386+tol:
      return('++40m')
   if f>7.0 and f<7.2:
      return('++40m') #another fixup
   if f>10.1387-tol and f<10.1387+tol:
      return('++30m')
   if f>10.0 and f<10.5:
      return('++30m') #fixup for spurious freq report
   if f>14.0956-tol and f<14.0956+tol:
      return('++20m')
   if f>14.0 and f<14.35:
      return('++20m')
   if f>18.1046-tol and f<18.1046+tol:
      return('++17m')
   if f>21.0946-tol and f<21.0946+tol:
      return('++15m')
   if f>24.9246-tol and f<24.9246+tol:
      return('++12m')
   if f>28.1246-tol and f<28.1246+tol:
      return('++10m')
   if f>50.293-tol and f<50.293+tol:
      return('+++6m')
   if f>70.091-tol and f<70.091+tol:
      return('+++4m')
   if f>144.489-tol and f<144.489+tol:
      return('+++2m')
   if f>432.3-tol and f<432.3+tol:
      return('70cm')
   if f>1296.5-tol and f<1296.5+tol:
      return('23cm')   
   return('REJECT')
 

#
# Main program starts here
#

if len(sys.argv)==1:
   print "Usage: CWCA.py wsprSpotsFile <-d>"
   sys.exit()


mf = open('members.txt', 'r')
for m in mf:
   md = m.split(',')
   mc.append(md[0].rstrip().lstrip().upper())
   mcw.append([])
   msw.append([])
   mrxband.append([])
   mtxband.append(md[1].strip())
   mp.append([])
   mow.append([])

debugObservers = False 
if len(sys.argv) == 3: 
   debugObservers = sys.argv[2].startswith('-d')

of = open('observers2017.txt', 'r')
mo = open('missing-observers.txt', 'w')
for o in of:
   od = o.split(',')
   if debugObservers:
      print o
   oc.append(od[0].rstrip().lstrip().upper())
   oe.append(str(int(od[1])))
   ocountry.append(od[2].rstrip().lstrip().upper())
   if int(od[1].rstrip()) == 999:
      mo.write(o)


spotsFile = sys.argv[1]
print 'Spots file = ', spotsFile
print

rejectedReports = 0
f = open(spotsFile, 'r')
r = open('RejectedFrequency.txt', 'w') 
for l in f:
   ls = l.split(',')
   if ls[6] in mc :
      if ls[2] in oc:
         band = freqtoband(ls[5])
         if band <> 'REJECT':        
            obs=oc.index(ls[2])
            uniqueappend(obsWhoHeardUs, obs)
            mem=mc.index(ls[6])
            mrxband[mem].append(band)
            if mtxband[mem] != 'ALL': # correct the slots for the single band entrants
               band = mtxband[mem]
            if uniqueappend(msw[mem], band+oe[obs]):
               uniqueappend(mow[mem], band+ocountry[obs])
            uniqueappend(mcw[mem], oe[obs])
            uniqueappend(te,oe[obs])
            mp[mem].append(int(ls[8]))
            sq = ls[3][:2]
         else:
            r.write(str(ls)+'\n')
            rejectedReports=rejectedReports+1
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


for m in mc:
   mem = mc.index(m)
   if  len(mcw[mem]) > 0:
      print 'Member: ', m
      print 'Countries (Entities) heard in =', len(mcw[mem]), ', Band slots =', len(msw[mem])
      print 'Countries:'
      mow[mem]=sorted(mow[mem])
      bnd = '999'
      slotString = ''
      bndCnt = 0
      for observer in mow[mem]:
         obsData = observer.split('m')
         if obsData[0] <> bnd:
            if bndCnt<>0:
               print slotString + '  (Total: ' + str(bndCnt) + ')'
            bnd = obsData[0]
            obsData[0] = obsData[0].replace('+','')
            print
            print 'Band: '+obsData[0]+'m'
            slotString = obsData[1]
            bndCnt = 1
         else:
            slotString = slotString+', '+obsData[1]
            bndCnt = bndCnt + 1
      print slotString + '  (Total: ' + str(bndCnt) + ')'
       
      b = str(Counter(mrxband[mem]))
      b = b[9:] # trim the beginning and end of the Counter standard format
      for char in "{}()'+":
         b = b.replace(char,'')
      print
      print 'Number of times reported on the following bands', b
      c = str(Counter(mp[mem]))
      c = c[9:]
      for char in "{}()'+":
         c=c.replace(char,'')
      print 'Number of times reported at following power in dBm', c
      print
      print
      nsm = nsm + 1 #num scoring members
      sm.append([m, len(msw[mem]), len(mcw[mem])])

print 'Number of observers that heard us =', len(obsWhoHeardUs)
print 'Total countries worked = ', len(te)
print 'Rejected Reports = ', rejectedReports

sm = sorted(sm,key=lambda x: x[1], reverse=True)

print
print
print 'Posn\tMember\tSlots\tCountries'
print 

for m in sm:
   print sm.index(m)+1,'\t',m[0], '\t', m[1], '\t', m[2] 



 












