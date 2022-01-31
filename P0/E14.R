x <- 1:20
y <- sin(x)
print(plot(x, y))
plot(x, y, type="l")
print(lines(x, cos(x), col="red"))
print(abline(h=0, lwd=5, col="green"))
print(plot(x, y))
print(points(x + 1, cos(x + 1), pch=15, col="green"))
print(plot(x, y, main="Texto arriba", xlab="Etiqueta", ylab="Otra etiqueta"))
