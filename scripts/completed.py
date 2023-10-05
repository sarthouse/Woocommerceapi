from wcapi import wcapi
import pandas as pd
from datetime import datetime

data = []
page = 1
while True:
    ordenes = wcapi.get("orders", params={"status": "completed", "after": "2023-06-21T00:00:00", "page": page}).json()
    if not ordenes:
        break
    for orden in ordenes:

        for item in orden["line_items"]:
            data.append({
                'ID de Orden': orden['id'],
                'Fecha de Creación': datetime.strptime(orden['date_created'], '%Y-%m-%dT%H:%M:%S').strftime(
                    '%d/%m/%Y %H:%M'),
                'Productos': item['name'],
                'Cantidad': item['quantity']})

    page += 1

df = pd.DataFrame(data)
df.to_csv('./files/completados.csv', index=False)
