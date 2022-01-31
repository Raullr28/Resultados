file.choose("/Users/raullagunes/Desktop/ejemplo.csv")

datos <- read.csv("/Users/raullagunes/Desktop/ejemplo.csv", header=TRUE, sep=" ", stringsAsFactors=FALSE)
print(datos)
  
datos$Estatura <- as.numeric(datos$Estatura)
datos$Gatos <- as.numeric(datos$Gatos)
datos$Perros <- as.numeric(datos$Perros)
print(sum(datos$Gatos))

print(sum(datos$Gatos) > sum(datos$Perros))

print(datos$Gatos == datos$Perros)
print(datos[datos$Nombre == "Elisa",])

prom <- mean(datos$Estatura)
print(datos[datos$Estatura > prom,])

print(datos[datos$Estatura > prom,]$Gatos)

datos <- rbind(datos, c("Tania", 175, 0, 2))
print(datos)
 
datos$Estudiante <- c(FALSE, TRUE, TRUE, TRUE, FALSE, FALSE)
print(datos)
  
print(datos[3,])
  
print(datos[2:4,])
  
print(datos[2:4,3])

datos$Estudiante <- as.factor(datos$Estudiante)
print(datos$Estudiante)
