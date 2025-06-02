"""
# Semana 4: listas y loops

#creando una lisat de numeros

numeros = [5, 10, 15.2, 20]
print (numeros)

print (numeros[1])
numeros = numeros[2]
print (numeros)

num = 4.3
datos = [num, "palabra", True]
print (datos)




datos = [5, "libro", [48, 'Hola'], True]
print (datos)
datos[0]=100
print(datos)
print(datos)
print(datos[2])

#usando [ : ] para copiar una lista
datos = [5, 10, 15, 20]
copia_de_datos = datos[ : ]
datos[0]=50
print ("datos: {}\t copia de datos: {}" .format(datos, copia_de_datos))

numeros=[5, 10, 15]
length= len(numeros)
print(length)

numeros = [5, 10, 15, 20, 25]
length = len(numeros)
print(length)



print( numeros[1 : 3 ] )
print( numeros[ : 2 ] )
print( numeros[ : : 2 ] )
print( numeros[ -3 :  ] )

numeros = [10, 20]
numeros.append(5)
print(numeros)


palabras = ["ball", "base" ]
print (palabras)
palabras.insert(0, "glove")
print (palabras)


items = [5, "ball", True]
items.pop( )
items_removido = items.pop(0)
print(items_removido, "\n", items)


deportes= [ "baseball", "soccer", "football", "raquetball"]
try:
    deportes.remove("soccer")
except:
    print("ese elemento no se encuentra en la lisa")
print(deportes)

numeros = [5, 3, 9]
print( min(numeros) )
print( max(numeros) )
print( sum(numeros) )
print( sum(numeros) / len(numeros) )



numeros = [5, 8, 0, 2]
numeros_ordenados = sorted(numeros)
print(numeros, numeros_ordenados )


nombres = [ "René", "Ez", "David" ]
if "Ez" in nombres:
    print("Encontrado")
if "Gustavo" not in nombres:
    print("No encontrado")

numeros = [ ]
if not numeros:
    print("la lista esta vacía")


deportes = ["baseball", "padel", "football", "basketball"]
for deporte in deportes:
    print(deporte)

nombres = ["Gustavo", "Daniel", "Jamin", "René", "David"]
while "Gus" in nombres:
    nombres.remove("Daniel")
    print(nombres)

Deportes=["Footbol", "Waterpolo", "Basketbol", "Soccer"]

for Deporte in Deportes:
    print(f"Me gusta jugar {Deporte}")

nombres=["Gustavo", "David", "Jesus", "René"]
letra =[nombre[0] for nombre in nombres]
print(letra)
"""

