groceries=['eggs','ham','toast','juice']
for item in groceries:
    print item
    
count = 1
for item in groceries:
    print str(count)+')'+item
    count += 1
    
a = [6,2,4,3,2,4]
n=0
print a

for e in a:
   a[n]= e*2
   n +=1
print a

for i in range(len(a)):
    a[i] *= 2
print a

m = [[3,4],[2,1]]
for i in range(2):
    for j in range(2):
        m[i][j] *= 3

print m

l = [[1,'eggs'],(2,'ham'),'toast',4.0]
print l[3]
print l[1]
print l[1][0]
print l[1][1]
print l[1][1][0]

t=('A','B','C','D','E')
for i in range(len(t)):
    for j in range(i+1,len(t)):
        print t[i], t[j]
