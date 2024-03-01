import pprint
from wcapi import wcapi_edit
import datetime
import pandas as pd

# data1 = {
#             'status': 'on-hold',
#             'billing': {
#                 'first_name': 'Gabriel',
#                 'last_name': 'Sarthou',
#                 'address_1': 'Gregorio de Laferrere 2728',
#                 'city': 'CABA',
#                 'phone': '1130754739',
#                 'postcode': '1439'},
#             'shipping': {
#                 'first_name': 'Gabriel',
#                 'last_name': 'Sarthou',
#                 'address_1': 'Gregorio de Laferrere 2728',
#                 'city': 'CABA',
#                 'phone': '',
#                 'postcode': '1439'},
#             'meta_data': [
#                 {'id': 156195, 'key': 'DNI', 'value': '44937958'},
#                 {'id': 156193, 'key': '_billing_dni_afip', 'value': '44937958'}],
#         }

wcapi = wcapi_edit

while True:
    op = input('''Elija la operación: 
    1 - Listar notas
    2 - Enviar mensaje de seguimiento
    3 - Agregar nota interna
    4 - Cantidad de pedidos desde el 27/11/2023
    5 - Pedidos completados desde el 01/01/2023
    6 - Listado de stock\n''')
    if op == '1':
        ID = input('Introduce numero de pedido: ')
        order = wcapi.get(f'orders/{ID}').json()
        print(order['billing']['first_name'] + ' ' + order['billing']['last_name'])
        try:
            notes = wcapi.get(f'orders/{ID}/notes').json()
            notes_data = []
            for note in notes:
                notes_data.append(note['note'])
            pprint.pprint(notes_data)
        except:
            continue

    elif op == '2':
        try:
            ID = input('Introduce numero de pedido: ')
            order = wcapi.get(f'orders/{ID}').json()
            print('Le vas a mandar mensaje a: ' + order['billing']['first_name'] + ' ' +
                  order['billing']['last_name'] + '. ¿Querés continuar?')
            cont = input('Y/N')
            if cont == 'Y' or cont == 'y' or cont == '':
                pass
            else:
                continue
            seguimiento = input('Introduce numero de seguimiento: ')
            nota = (
                f'Hola {order["billing"]["first_name"]} ¿cómo estás? Mi nombre es Gabriel,'
                f' voy a estar gestionando tu pedido.'
                f' Me podes hacer cualquier consulta. Tu pedido va a ser despachado en el día de hoy.'
                f' Te dejo el número de envío de Correo Argentino: {seguimiento},'
                f' lo podés seguir a través de este link: https://www.correoargentino.com.ar/formularios/e-commerce.'
                f' Muchas gracias por la compra')
            data = {'note': nota,
                    'customer_note': True,
                    'added_by_user': True}
            note = wcapi.post(f'orders/{ID}/notes', data).json()
            note = f'''\nNota: {note['note']},\nEnviado al cliente: {note['customer_note']},\nAutor: {note['author']}'''
            pprint.pprint(note)

        except:
            break
    elif op == '3':
        try:
            ID = input('Introduce numero de pedido: ')
            order = wcapi.get(f'orders/{ID}').json()
            nota = input('Agregar nota interna:\n')
            data = {'note': nota,
                    'added_by_user': True}
            note = wcapi.post(f'orders/{ID}/notes', data).json()
            note = f'''\nNota: {note['note']},\nEnviado al cliente: {note['customer_note']},\nAutor: {note['author']}'''
            pprint.pprint(note)
        except:
            break
    elif op == '4':
	d = int(input('Día: '))
	m = int(input('Mes: '))
	a = int(input('Año: '))
	
        page = 1
        i = 0
        while True:
            orders = wcapi.get("orders", params={"after": f"{a}-{m}-{d}T00:00:00", "page": page}).json()
            if not orders:
                break

            for order in orders:
                i += 1
                print(order['id'], order['status'])
                page += 1
                print('La cantidad de pedidos:' + str(i))

    elif op == '5':
	d = int(input('Día: '))
	m = int(input('Mes: '))
	a = int(input('Año: '))
        data = []
        page = 1
        while True:
            ordenes = wcapi.get("orders",
                                params={"status": "completed", f"after": "{a}-{m}-{d}T00:00:00", "page": page}).json()
            if not ordenes:
                break
            for orden in ordenes:

                for item in orden["line_items"]:
                    data.append({
                        'ID de Orden': orden['id'],
                        'Fecha de Creación': datetime.strptime(orden['date_created'], '%Y-%m-%dT%H:%M:%S').strftime(
                            '%d/%m/%Y %H:%M'),
                        'Productos': item['name'],
                        'Cantidad': item['quantity']
                    })
            page += 1

        df = pd.DataFrame(data)
        df.to_csv('/home/vagner/Escritorio/completados.csv', index=False)
        print('Listo!')

    elif op == '6':
        products = wcapi.get("products", params={'type': 'variable'}).json()
        data = []

        for product in products:
            product_id = product['id']
            product_name = product['name']
            variations = wcapi.get(f"products/{product_id}/variations").json()
            for variation in variations:
                attributes = variation['attributes']
                variation_name = next(
                    (attr['option'] for attr in attributes if attr['name'] == 'Talle' or attr['name'] == 'Talles'),
                    None)
                data.append({
                    'SKU': variation['sku'],
                    'Product Name': product_name + " " + str(variation_name),
                    'Quantity': variation['stock_quantity'],
                    'Real': ''
                })

        products = wcapi.get("products", params={'type': 'simple'}).json()
        for product in products:
            data.append({
                'SKU': product['sku'],
                'Product Name': product['name'],
                'Quantity': int(product['stock_quantity']),
                'Real': ''
            })

        df = pd.DataFrame(data)
        df.to_csv('/home/vagner/Escritorio/stock.csv', index=False)
        print('Listo!')

    elif op == '0':
        break

    else:
        print('¿Flaco sos pelotudo?')
        continue
