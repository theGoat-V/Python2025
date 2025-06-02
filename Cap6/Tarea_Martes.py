
datos = {}
datos['nombre']= input("Ingrese su nombre: ")
datos['direccion']= input("Ingrese su dirección: ")
datos['telefono']= input("ingrese su numero se telefono: ")

print("\n Informacion ingresada")
for clave, valor in datos.items():
    print(f"{clave.capitalize()}:{valor}")

"""
#codigo malo
persona = {"nombre", "Enrique Barajas"}
print( persona["nombre"])

#codigo bien, cambiamos la "," por ":"
persona = {"nombre": "Enrique Barajas"}
print( persona["nombre"])
"""