Toño = ["David Hernandez", 16, 50000, "Supervisor de ventas"]
Rene = ["Rene Mauricio", 16, 30000, "Vendedor"]
# print(Toño[0])
# print(Rene[2])
print (Rene[0].split()[-1])
personas = [Toño, Rene]
for persona in personas:
    print(persona)

for persona in personas:
    print (persona[2])

personas = [Toño, Rene]
personas.append(["Jisa", 16, 0, None])
for persona in personas:
    print(persona)

