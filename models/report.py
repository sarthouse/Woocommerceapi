import pandas as pd
from jinja2 import Environment, FileSystemLoader
import pdfkit

def report_pdf():
	# Cargar los datos desde el archivo CSV
	df = pd.read_csv('/home/vagner/Documentos/Woocommerceapi/procesando.csv')
	ordenes = df.to_dict('records')

	# Configurar el entorno de Jinja2
	env = Environment(loader=FileSystemLoader('/home/vagner/Documentos/Woocommerceapi/templates'))  # Ajusta el directorio según sea necesario

	# Cargar el template HTML
	template = env.get_template('template.html')  # Ajusta el nombre del archivo según sea necesario

	# Renderizar el template con los datos de las órdenes
	html_output = template.render(orders=ordenes)

	# Guardar el HTML en un archivo temporal (opcional)
	with open('/home/vagner/Documentos/Woocommerceapi/temp.html', 'w') as f:
		f.write(html_output)

	# Convertir el HTML a PDF
	options = {
		'page-size':'A4',
		'orientation':'Landscape',
		'encoding':'UTF-8',
		'margin-right':'20mm',
		'margin-left':'20mm',
		}
	pdfkit.from_file('/home/vagner/Documentos/Woocommerceapi/temp.html', '/home/vagner/Documentos/Woocommerceapi/reporte.pdf', options=options)

	# Eliminar el archivo temporal (opcional)
	#import os
	#os.remove('/home/vagner/Documentos/Woocommerceapi/temp.html')

	print('El PDF se ha generado correctamente.')


