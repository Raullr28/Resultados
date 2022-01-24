a = [1, 2, 3]
b = [1, 2, 4]
c = [x == y for (x, y) in zip(a, b)]
print(c)


print(all(c))

print (any(c))

