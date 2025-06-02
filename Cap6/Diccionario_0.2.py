"""
carro = {"año": 2028}
carro['color']= 'azul'
print ('año: {} \t color: {}'.format(carro['año'], carro['color']))

carro = {"año": 2028}
carro['color']= 'Negro'
print ('año: {} \t color: {}'.format(carro['año'], carro['color']))

try:
    del carro ['color']
    print (carro)
except: print ("no se puede eliminar el elemento")


persona = {'nombre': 'Gustavo', 'edad': 16}
for llave in persona.keys( ):
    print(llave)
    print( persona [llave] )
print ('\n')

persona = {'nombre': 'Gustavo', 'edad': 16}
for valor in  persona.values( ):
    print(valor)
print ('\n')


persona = {'nombre': 'Gustavo', 'edad': 16}
for llave, valor  in persona.items( ):
    print( "{}:{}".format(llave, valor) )
"""