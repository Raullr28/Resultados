x <- 3
y <- NULL
if (x > 5) { y <- x * 3 } else { y <- 6 - x }
print(y)

z <- NULL
if (x %% 2 == 1 & y %% 2 == 1) { z <- 2 } else { z <- 3 }

print(z)

print(if (z != 1) { print("no es uno") })


print(if (x == 2 | y == 2 | z == 2) { print("hay un dos") } else { print("no hay un dos") })

print(for (i in 1:5) { print(2**i) })

print(while (x > 0) { print("quito uno"); x <- x - 1 })


print(x) 

