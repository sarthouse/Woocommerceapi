import pandas as pd
from wcapi import wcapi
from datetime import datetime
from report import report_pdf


# Mapeo provincias

mapping = {
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

#Las funciones para que llame las ordenes

def obtener_detalles_cliente(orden):
   
   return {
        
    }

def obtener_detalles_productos(orden):
	detalles_productos = []
	for item in orden["line_items"]:
		detalles_productos.append({
			"Producto": item["name"],
			"Cantidad": item["quantity"]
			})
	return detalles_productos

data = []
page = 1
while True:
	ordenes = wcapi.get("orders", params={"status": "processing", "page": page}).json()
	if not ordenes:
		break
	for orden in ordenes:
		estado = orden["billing"]["state"]
		provincia = mapping.get(estado, estado)
		detalles_productos = obtener_detalles_productos(orden)
		
		productos_agrupados = ", ".join(f'{producto["Producto"]} ({producto["Cantidad"]})' for producto in detalles_productos)
		seguimiento = input(f'{orden["id"]} - Ingrese seguimiento : ')       
		mensaje =  f'Hola {orden["billing"]["first_name"]} ¿cómo estás? Mi nombre es Gabriel, voy a estar gestionando tu pedido nº {orden["id"]}. Me podes hacer cualquier consulta. Tu pedido va a ser despachado en el día de hoy. Te dejo el número de envío del correo: {seguimiento}, lo podes seguir a través de este link: https://www.correoargentino.com.ar/formularios/e-commerce. Muchas gracias por la compra'

		data.append({
			'ID de Orden': orden['id'],
			'Fecha de Creación': datetime.strptime(orden['date_created'], '%Y-%m-%dT%H:%M:%S').strftime('%d/%m/%Y %H:%M'),
			"Nombre": orden["billing"]["first_name"],
			"Apellido": orden["billing"]["last_name"],
			"Nombre completo":orden["billing"]["first_name"] + " " + orden["billing"]["last_name"],
			"Dirección": orden["billing"]["address_1"] +' '+ orden["billing"]["address_2"],
			"Código Postal": orden["billing"]["postcode"],
			"Ciudad": orden["billing"]["city"],
			"Estado": provincia,
			"Email": orden["billing"]["email"],
			"Teléfono": orden["billing"]["phone"],
			'Tipo de envío': orden['shipping_lines'][0]['method_title'],
			'Productos': productos_agrupados,
			'Seguimiento': seguimiento,
			'Mensaje': mensaje})
	
	page += 1
	
df = pd.DataFrame(data)
df.to_csv('/home/vagner/Documentos/Woocommerceapi/procesando.csv', index=False)

report_pdf()

