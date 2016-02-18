
entity=['UNKNOWN' for x in range(1,1200)]
cw =[]

ef = open('Entities.csv', 'r')
for e in ef:
   e = e.split(',')
   entity[int(e[1])]=e[0]

es=set()
of = open('observers.txt', 'r')
for o in of:
   od = o.split(',')
   ent = int(od[2].rstrip())
   if ent not in es:
      es.add(ent)

for i in es:
   cw.append(entity[i])

cw.sort()

for c in cw:
   print c+',',


