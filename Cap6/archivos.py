"""
f = open("prueba.txt", "w+")
f.write ("Hola mundo\n")
f.close()

f = open("prueba.txt", "r")
contenido = f.read()
print(contenido)
f.close()
"""
import csv
with open ("prueba.csv", mode="w", newline="") as f:
    writer = csv.writer(f, delimiter=",")
    writer.writerow(["Nombre", "Edad"])
    writer.writerow(["Gustavo", 16])
 
with open("prueba.csv", mode="r") as f:
    reader = csv.reader(f, delimiter=",")
    for row in reader: 
        print(row)
        