from woocommerce import API

wcapi = API(
    url="https://vagner.ar",
    consumer_key='ck_18ae89cd06ed6a9478780f2c66dc0e01a215df11',
    consumer_secret='cs_03bf6d307664c9cf20e5d55a617f4718962c7a09',
    wp_api=True,
    version='wc/v3'
)

wcapi_edit = API(
    url="https://vagner.ar",
    consumer_key='ck_3376b8e61f5936d8950a30fb796e8bce99a0be3a',
    consumer_secret='cs_b03a51cbab961fb98e3bc066b3fd733026380638',
    wp_api=True,
    version='wc/v3'
)
