import sys
from collections import Counter

print('CARC WSPR Competition Adjudicator - Simplified version')
print

mc = [] # member call
#mcw = []  # member country worked
mbzw = [] # member zone worked
#msqw = [] # member square worked
msw = [] # slot = band + country
#mbec = [] # band entity count
#mrxband = [] #bands heard on
#mtxband = [] #bands transmitting on
#mp = [] # member power
#te = [] # total entities worked by club members

oc = [] #observers call
oe = [] #observers entity
oz = [] #observers zone

#misso = [] # missing observers

#obsIncomplete=False



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
      return('630m') # fixup for spurious observations
   if f>0.4742-tol and f<0.4742+tol:
      return('630m')
   if f>1.8366-tol and f<1.8366+tol:
      return('160m')
   if f>3.5926-tol and f<3.5926+tol:
      return('80m')
   if f>3.5 and f<3.7:
      return('80m') #Fixup
   if f>5.2872-tol and f<5.2872+tol:
      return('60m')
   if f>7.0386-tol and f<7.0386+tol:
      return('40m')
   if f>7.0 and f<7.2:
      return('40m') #another fixup
   if f>10.1387-tol and f<10.1387+tol:
      return('30m')
   if f>10.0 and f<10.2:
      return('30m') #fixup for spurious freq report
   if f>14.0956-tol and f<14.0956+tol:
      return('20m')
   if f>18.1046-tol and f<18.1046+tol:
      return('17m')
   if f>21.0946-tol and f<21.0946+tol:
      return('15m')
   if f>24.9246-tol and f<24.9246+tol:
      return('12m')
   if f>28.1246-tol and f<28.1246+tol:
      return('10m')
   if f>50.293-tol and f<50.293+tol:
      return('6m')
   if f>70.091-tol and f<70.091+tol:
      return('4m')
   if f>144.489-tol and f<144.489+tol:
      return('2m')
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

   mbzw.append(set([]))
#   mcw.append([])
   msw.append(set([]))
#   msqw.append([])
#   mrxband.append([])
#   mtxband.append(md[1].strip())
#   mp.append([])
#   mbec.append([])

#debugObservers = False 
#if len(sys.argv) == 3: 
#   debugObservers = sys.argv[2].startswith('-d')

of = open('observers.txt', 'r')
for o in of:
   od = o.split(',')
   oc.append(od[0].rstrip().lstrip().upper())
   oz.append(str(int(od[1])))
   oe.append(str(int(od[2])))


spotsFile = sys.argv[1]
print 'Spots file = ', spotsFile
print

#rejectedReports = 0
f = open(spotsFile, 'r')
#r = open('RejectedFrequency.txt', 'w') 
for l in f:
   ls = l.split(',')
   if ls[6] in mc :
      if ls[2] in oc:
         band = freqtoband(ls[5])
         if band <> 'REJECT':        
            obs=oc.index(ls[2])
            mem=mc.index(ls[6])
            mbzw[mem].add(str(oz[obs]+"B"+band))
            msw[mem].add(band+str(oe[obs]))

      else:
         print "missing observer", ls[2], ls[3]
         sys.exit()

for m in mc:
   mem = mc.index(m)
   if  len(mbzw[mem]) > 0:
     print m
     print "slots worked :"
     print sorted(msw[mem])
     print "zones worked :"
     print sorted(mbzw[mem])
     print


 












