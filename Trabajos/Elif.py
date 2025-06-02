"""
# condicionales con elif

x, y = 5, 10

if x > y:
    print ("x es mayor que y")
elif x < y:
    print ("x es menor que y")
elif x == y: 
    print ("x es igual a y")
"""
numero1 =input("ingresa un número:")
numero2 =input("ingresa otro número:")
if numero1 > numero2:
    print(numero1, "es mayor")
elif numero1 < numero2:
    print(numero2, "es mayor")
elif numero1 == numero2:
    print("ambos numeros son iguales")

#------------------------------------------------------------
#usando else
nombre = print(imput('Escribe un nombre:'))
if nombre == 'Gustavo':
    print("Hola Gustavo")
