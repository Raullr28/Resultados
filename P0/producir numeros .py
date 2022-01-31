from numpy.random import normal, exponential
print(normal(size = 10) )# media cero, desv. est. 1
print(normal(loc = 5, scale = 1.3, size = 10))

       
print(exponential(size = 2))

print(exponential(scale = 1 / 3, size = 2))
