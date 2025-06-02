Toño = {"Nombre": "David Hernandez", "Edad": 16, "Salario": 50000, "Trabajo": "Supervisor de ventas"}
René = {"Nombre": "René Vargas", "Edad": 16, "Salario": 30000, "Trabajo": "Vendedor"}

# print(Toño["Salario"])
# print (Toño["Nombre"].split()[-1])

personas = [Toño, René]

for persona in personas:
    print(persona["Nombre"], persona["Edad"], sep = ", ")
