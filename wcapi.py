from woocommerce import API
from datetime import datetime

wcapi = API(
    url="https://vagner.ar",
    consumer_key='ck_18ae89cd06ed6a9478780f2c66dc0e01a215df11',
    consumer_secret='cs_03bf6d307664c9cf20e5d55a617f4718962c7a09',
    wp_api=True,
    version='wc/v3',
    timeout=10000
)

wcapi_edit = API(
    url="https://vagner.ar",
    consumer_key='ck_3376b8e61f5936d8950a30fb796e8bce99a0be3a',
    consumer_secret='cs_b03a51cbab961fb98e3bc066b3fd733026380638',
    wp_api=True,
    version='wc/v3'
)

status = {
    'pending': 'Pendiente de pago',
    'on-hold': 'En espera',
    'cancelled': 'Cancelado',
    'processing': 'Procesando',
    'completed': 'Completado'
}

state = {
    'B': 'Buenos Aires',
    'C': 'Capital Federal',
    'K': 'Catamarca',
    'H': 'Chaco',
    'U': 'Chubut',
    'X': 'Córdoba',
    'W': 'Corrientes',
    'E': 'Entre Ríos',
    'P': 'Formosa',
    'Y': 'Jujuy',
    'L': 'La Pampa',
    'F': 'La Rioja',
    'M': 'Mendoza',
    'N': 'Misiones',
    'Q': 'Neuquén',
    'R': 'Río Negro',
    'A': 'Salta',
    'J': 'San Juan',
    'D': 'San Luis',
    'Z': 'Santa Cruz',
    'S': 'Santa Fe',
    'G': 'Santiago del Estero',
    'V': 'Tierra del Fuego',
    'T': 'Tucumán'
}

def _list_orders(params):
    orders = wcapi.get('orders', params=params).json()
    for order in orders:
        order['date_created'] = datetime.strptime(order['date_created'], '%Y-%m-%dT%H:%M:%S').strftime('%d/%m/%Y %H:%M')
        order['status'] = status.get(order['status'], order['status'])
        order['billing']['state'] = state.get(order['billing']['state'], order['billing']['state'])

    return orders
