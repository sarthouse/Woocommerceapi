from wcapi import wcapi
from pprint import pprint
import pandas as pd

data = []
for i in range(int(input('¿Cuántos envíos hay?:'))):
    id = input('Número de orden: ')
    order = wcapi.get(f'orders/{id}').json()
    print(f'Pedido {order["id"]}\n{order["billing"]["first_name"]} {order["billing"]["last_name"]}')
    suc_destino = input('Ingrese código de sucursal (Dejar vacío si va a domicilio): ')
    localidad = input('Ingrese localidad (Dejar vacío si va a sucursal): ')
    print(order["billing"]["address_1"] + ' ' + order["billing"]["address_2"]+ 'CP '+order["billing"]["postcode"],)
    calle = input('Ingrese calle del domicilio (Vacío en sucursal): ')
    altura = input('Ingrese altura del domicilio (Vacío en sucursal): ')
    piso= input('Ingrese piso del domicilio (Opcional/Vacío en sucursal): ')
    depto = input('Ingrese DEPTO del domicilio (Opcional/Vacío en sucursal): ')
    cp = input('Ingrese Codigo Postal del domicilio (Vacío en sucursal): ')
    print(f'Número de teléfono: {order["billing"]["phone"]}')
    cod_cel = input('Código de área: ')
    cel = input('Celular: ')
    data.append({
        'tipo_producto(obligatorio)':'CP',
        'largo(obligatorio en CM)':'30',
        'ancho(obligatorio en CM)':'33',
        'altura(obligatorio en CM)':'13',
        'peso(obligatorio en KG)':'1.6',
        'valor_del_contenido(obligatorio en pesos argentinos)':'100000',
        'provincia_destino(obligatorio)':order['billing']['state'],
        'sucursal_destino(obligatorio solo en caso de no ingresar localidad de destino)':suc_destino,
        'localidad_destino(obligatorio solo en caso de no ingresar sucursal de destino)': localidad,
        'calle_destino(obligatorio solo en caso de no ingresar sucursal de destino)':calle,
        'altura_destino(obligatorio solo en caso de no ingresar sucursal de destino)':altura,
        'piso(opcional solo en caso de no ingresar sucursal de destino)':piso,
        'dpto(opcional solo en caso de no ingresar sucursal de destino)':depto,
        'codpostal_destino(obligatorio solo en caso de no ingresar sucursal de destino)':cp,
        'destino_nombre(obligatorio)':order["billing"]["first_name"] + " " + order["billing"]["last_name"],
        'destino_email(obligatorio, debe ser un email valido)':order["billing"]["email"],
        'cod_area_tel(opcional)':"",
        'tel(opcional)':"",
        'cod_area_cel(obligatorio)':cod_cel,
        'cel(obligatorio)':cel,

    })
    print('\n')

pprint(data)
df = pd.DataFrame(data)
df.to_csv('~/Escritorio/correo_masivo.csv', index=False, sep=';')