from woocommerce import API
import pprint

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

wcapi = API(
    url="https://vagner.ar",
    consumer_key='ck_3376b8e61f5936d8950a30fb796e8bce99a0be3a',
    consumer_secret='cs_b03a51cbab961fb98e3bc066b3fd733026380638',
    wp_api=True,
    version='wc/v3'
)

while True:
    op = input('''Elija la operación: 
    1 - Listar notas
    2 - Enviar mensaje de seguimiento
    3 - Agregar nota interna\n''')
    if op == '1':
        ID = input('Introduce numero de pedido: ')
        order = wcapi.get(f'orders/{ID}').json()
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
            print('Le vas a mandar mensaje a: ' + order['billing']['first_name'] + ' ' + order['billing'][
                'last_name'] + '. ¿Queres continuar?')
            cont = input('Y/N')
            if cont == 'Y' or cont == 'y':
                pass
            else:
                continue
            seguimiento = input('Introduce numero de seguimiento: ')
            nota = f'Hola {order["billing"]["first_name"]} ¿cómo estás? Mi nombre es Gabriel, voy a estar gestionando tu pedido nº {order["id"]}. Me podes hacer cualquier consulta. Tu pedido va a ser despachado en el día de hoy. Te dejo el número de envío del correo: {seguimiento}, lo podes seguir a través de este link: https://www.correoargentino.com.ar/formularios/e-commerce. Muchas gracias por la compra'
            data = {'note': nota,
                    'customer_note': True,
                    'added_by_user': True}
            note = wcapi.post(f'orders/{ID}/notes', data).json()
            note = f'''
                        Nota: {note['note']},
                        Enviado al cliente: {note['customer_note']},
                        Autor: {note['author']}'''
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
            note = f'''
            Nota: {note['note']},
            Enviado al cliente: {note['customer_note']},
            Autor: {note['author']}'''
            pprint.pprint(note)
        except:
            break
    elif op == '0':
        break
    else:
        print('¿Flaco sos pelotudo?')
        continue
