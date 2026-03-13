vehiculo = {'matricula': 100,'tipo': 'coche'}
destinos = ['Alicante', 'Madrid']
productos = ['queso','leche']
pedido=[]
error_1=0
error_2=0
error_3=0
while error_1==0:
    print('Elige un producto:',productos)
    prod=input()
    if prod in productos:
        pedido.append(prod)
        error_1=1
    else:
        print('error')
while error_2==0:
    print('Elige un destino:',destinos)
    dest=input()
    if dest in destinos:
        pedido.append(dest)
        error_2=1
    else:
        print('error')
while error_3==0:
    print('Elige un transporte:',vehiculo['tipo'])
    trans=input()
    if trans in vehiculo['tipo']:
        pedido.append(vehiculo['matricula'])
        error_3=1
    else:
        print('error')
print(pedido)
