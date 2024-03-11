from wcapi import wcapi, wcapi_edit
from pprint import pprint
while True:
    sku = input('Ingresa sku producto:')
    p = wcapi.get('products', params={'sku': sku}).json()[0]
    pid=p['parent_id']
    id= p['id']
    if int(pid) == 0:
        continue
    else:
        v=wcapi.get(f'products/{pid}/variations/{id}').json()
        name = p['name'] + " " + v['name']
        pprint(name)
        cont = input('Continuar? S/n')
        if cont == 'S' or cont == 's' or cont == '':
            # data = {'name':name}
            # wcapi_edit.put(f"products/{id}", data)
            pprint(wcapi.get(f'products/{id}').json()['name'])
        else:
            continue
        