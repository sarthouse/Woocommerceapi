from wcapi import _list_orders
import pandas as pd
import datetime

data = []
page = 1
while True:
    ordenes = _list_orders({'status': 'processing', 'per_page': 20, 'page': page})
    if not ordenes:
        break
    for order in ordenes:
        detalles_productos = []
        for item in order["line_items"]:
            detalles_productos.append({
                "Producto": item["name"],
                "Cantidad": item["quantity"],
                "SKU": item['sku']
            })
        productos_agrupados = "\n".join(
            f'{producto["Producto"]} ({producto["Cantidad"]}) SKU:{producto["SKU"]}' for producto in
            detalles_productos)
        
        data.append({
            'Orden': order['id'],
            'Fecha': order['date_created'],
            'Nombre completo': order["billing"]["first_name"] + " " + order["billing"]["last_name"],
            'Localidad': order["billing"]["city"],
            'Provincia': order['billing']['state'],
            'Dirección': order["billing"]["address_1"] + ' ' + order["billing"]["address_2"],
            'CP': order["billing"]["postcode"],
            'Teléfono': order["billing"]["phone"],
            "Email": order["billing"]["email"],
            'Tipo de envío': order['shipping_lines'][0]['method_title'],
            'Productos': productos_agrupados})
    page += 1

df = pd.DataFrame(data)
with open('/home/vagner/Escritorio/pedidos.txt', 'w') as f:
    
    date = datetime.datetime.now().strftime('%d/%m/%Y %H:%M')
    f.write(f'Ultima actualización: {date}\n')
    for i in data:            
        p = f'''
Pedido {i['Orden']}
{i['Fecha']}
{i['Nombre completo']}
{i['Dirección']}, CP:{i['CP']}, {i['Localidad']}, {i['Provincia']}
{i['Teléfono']}, {i['Email']}
{i['Tipo de envío']}
--- PEDIDO ---
{i['Salto']}


'''
        f.write(p)
