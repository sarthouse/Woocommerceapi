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
        productos_agrupados = ", ".join(
            f'{producto["Producto"]} ({producto["Cantidad"]}) SKU:{producto["SKU"]}' for producto in
            detalles_productos)

        data.append({
            'ID de Orden': order['id'],
            'Fecha de Creación': order['date_created'],
            'Nombre completo': order["billing"]["first_name"] + " " + order["billing"]["last_name"],
            'Provincia': order['billing']['state'],
            'Ciudad': order["billing"]["city"],
            'Dirección': order["billing"]["address_1"] + ' ' + order["billing"]["address_2"],
            'Código Postal': order["billing"]["postcode"],
            'Teléfono': order["billing"]["phone"],
            "Email": order["billing"]["email"],
            'Tipo de envío': order['shipping_lines'][0]['method_title'],
            'Productos': productos_agrupados})
    page += 1

df = pd.DataFrame(data)
df.to_csv('~/Escritorio/pedidos.csv', index=False)

with open('/home/vagner/Escritorio/pedidos.txt', 'w') as f:
    date = datetime.datetime.now().strftime('%d/%m/%Y %H:%M')
    f.write(f'Ultima actualización: {date}\n')
    for i in data:
        p = f'''
Pedido {i['ID de Orden']}
{i['Fecha de Creación']}
{i['Nombre completo']}
{i['Provincia']}
{i['Ciudad']}
{i['Dirección']}
{i['Código Postal']}
{i['Teléfono']}
{i['Email']}
{i['Tipo de envío']}
--- PEDIDO ---
{i['Productos']}
'''
        f.write(p)
