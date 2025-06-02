nombre = input("por favor ingrese su nombre")
edad = input("ahora ingrese su edad: ")

usuario = {
    "nombre" : nombre,
    "edad" : edad
}

print("\nDiccionario creado:")
print(usuario)

pizza = {
    "ingredientes": ["queso", "salsa", "pimientos"]
}

print("Ingredientes de la pizza:")
for ingrediente in pizza["ingredientes"]:
    print(f"- {ingrediente}")