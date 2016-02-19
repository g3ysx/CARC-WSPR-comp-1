import sys
from collections import Counter

print('CARC WSPR Competition Adjudicator - Global Picture')
print(sys.version)
print

entity=['UNKNOWN' for x in range(1,1200)]
cw =[]
ub = 0

spots = 0
observers = []
bandobservers = []
o2200m = 0
o630m = 0
o160m = 0
o80m = 0
o60m = 0
o40m = 0
o30m = 0
o20m = 0
o17m = 0
o15m = 0
o12m = 0
o10m = 0
o6m = 0
o4m = 0
o2m = 0
o70cm = 0
o23cm = 0
checkbandobservers = 0

def uniqueappend(list, val):
   if val not in list:
      list.append(val)
   return

def freqtoband(freq):
   f=float(freq)
   if f < 0.1:
      #print 'unexpected band', freq
      return('REJECT')
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
   if f < 72.0:
      return('4m')
   if f < 146.0:
      return('2m')
   if f < 460.0:
      return('70cm')
   if f < 1300.0:
      return('23cm')
   #print 'unexpected band', freq
   return('REJECT')


f = open('wsprspots.csv', 'r')
for l in f:
   ls = l.split(',')
   spots = spots + 1
   band = freqtoband(ls[5])
   if band != 'REJECT':
      uniqueappend(observers, ls[2])
      uniqueappend(bandobservers,str(band)+ls[2])
   else:
      ub = ub+1


print 'Total Spots = ', spots
print '\nObservers = ', len(observers)
print '\nTotal unique band observers = ',len(bandobservers)
print '\n'
for bo in bandobservers:
   if bo.startswith('2200m'):
      o2200m = o2200m+1
   elif bo.startswith('630m'):
      o630m = o630m + 1
   elif bo.startswith('160m'):
      o160m = o160m + 1
   elif bo.startswith('80m'):
      o80m = o80m + 1
   elif bo.startswith('60m'):
      o60m = o60m + 1
   elif bo.startswith('40m'):
      o40m = o40m + 1
   elif bo.startswith('30m'):
      o30m = o30m + 1
   elif bo.startswith('20m'):
      o20m = o20m + 1
   elif bo.startswith('17m'):
      o17m = o17m + 1
   elif bo.startswith('15m'):
      o15m = o15m + 1
   elif bo.startswith('12m'):
      o12m = o12m + 1
   elif bo.startswith('10m'):
      o10m = o10m + 1
   elif bo.startswith('6m'):
      o6m = o6m + 1
   elif bo.startswith('4m'):
      o4m = o4m + 1
   elif bo.startswith('2m'):
      o2m = o2m + 1
   elif bo.startswith('70cm'):
      o70cm = o70cm + 1
   elif bo.startswith('23cm'):
      o23cm = o23cm + 1


print '2200m observbers = ', o2200m
print '630m observbers  = ', o630m
print '160m observbers  = ', o160m
print '80m observbers   = ', o80m
print '60m observbers   = ', o60m
print '40m observbers   = ', o40m
print '30m observbers   = ', o30m
print '20m observbers   = ', o20m
print '17m observbers   = ', o17m
print '15m observbers   = ', o15m
print '12m observbers   = ', o12m
print '10m observbers   = ', o10m
print '6m observbers    = ', o6m
print '4m observbers    = ', o4m
print '2m observbers    = ', o2m
print '70cm observbers  = ', o70cm
print '23cm observbers  = ', o23cm
print '\ncheck total = ', o2200m+o630m+o160m+o80m+o60m+o40m+o30m+o20m+o17m+o15m+o12m+o10m+o6m+o4m+o2m+o70cm+o23cm

print
print 'Unexpected band seen', ub, 'times'
print

ef = open('Entities.csv', 'r')
for e in ef:
   e = e.split(',')
   entity[int(e[1])]=e[0]

eq=[]
es=set()
of = open('observers.txt', 'r')
for o in of:
   od = o.split(',')
   ent = int(od[2].rstrip())
   if ent not in es:
      es.add(ent)
   eq.append(ent)

for i in es:
   cw.append(entity[i])

cw.sort()

print 'Countries that heard us:'

for c in cw:
   print c+',',
print
print

c = str(Counter(eq))
c = c[9:-2]

cl = c.split(',')

print 'Number of observers by country (entity):'

for r in cl:
   rc = r.split(':')
   print entity[int(rc[0])], ' : ',  int(rc[1])






