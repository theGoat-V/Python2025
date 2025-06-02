datos = {}
datos['nombre'] = input("Ingrese su nombre: ")
datos['direccion'] = input("Ingrese su dirección: ")
datos['telefono'] = input("Ingrese su número de teléfono: ")

print("\nDatos ingresados:")
for clave, valor in datos.items():
    print(f"{clave.capitalize()}: {valor}")