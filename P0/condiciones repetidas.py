x = 3
y = None
y = x * 3 if x > 5 else 6 - x
print(y)

z = None
z = 2 if x % 2 == 1 and y % 2 == 1 else 3
print(z)

if z != 1:
     print('no es uno')
 

print('hay un dos' if x == 2 or y == 2 or z == 2 else 'no hay un dos')

for i in range(1, 6):
    print(2**i)
 


while x > 0:
      print('quito uno')
      x -= 1

print(x)
