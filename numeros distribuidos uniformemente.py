from random import random
print(random())

from numpy.random import rand
print(rand(5))

from numpy.random import uniform
print(uniform(4, 10, size = 2))

print(random() < 0.5)

print(random() < 0.5)

print(random() < 0.5)

print(rand(5) < 0.5)

from random import sample
print(sample([i for i in range(1, 11)], 3))

print(sample([i for i in range(1, 11)], 3))

from random import shuffle
a = [i for i in range(1, 11)]
print(a)

shuffle(a)
print(a)

from numpy.random import choice
print(choice([2, 4, 6], size = 10, replace = True, p = [0.1, 0.2, 0.7]))
