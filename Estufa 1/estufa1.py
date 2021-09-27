#pip3 install paho-mqtt comando para instalar o paho no terminal

import paho.mqtt.client as mqtt #toda vez que usar o nome mqqt ele automáticamente carrega
import time
from hal import  aumentarTemp, diminuirTemp, temperatura, umidade, aquecedor
from definitions import usuario, password, client_id, server, port

def mensagem(client, user, msg):
    vetor = msg.payload.decode().split(',')
    aquecedor('on' if vetor[1] == '1' else 'off') #trocar isso pra ternário
    client.publish(f'v1/{usuario}/things/{client_id}/response', f'ok,{vetor[0]}')
    
# Conexão inicial
client = mqtt.Client(client_id)
client.username_pw_set(usuario, password)
client.connect(server, port)

# Subscriber
client.on_message = mensagem # método que será evocado quando receber uma mensagem do servidor
client.subscribe(f'v1/{usuario}/things/{client_id}/cmd/2') # dizendo qual tópico nos interessa
client.loop_start() # monitoramento do servidor

# Comportamento do sistema
# Publisher
while True:
    # 'v1/username/things/clientID/data/channel' -> formato correto
    temp = temperatura()
    umi = umidade()
    client.publish(f'v1/{usuario}/things/{client_id}/data/1', f'rel_hum,p={umi}') #publicando umidade
    client.publish(f'v1/{usuario}/things/{client_id}/data/0', f'temp,c={temp}') # publicando temperatura
    if temp < 28:
        while temp <= 30:
            temp = aumentarTemp(temp)
            client.publish(f'v1/{usuario}/things/{client_id}/data/1', f'rel_hum,p={umi}') #publicando umidade
            client.publish(f'v1/{usuario}/things/{client_id}/data/0', f'temp,c={temp}')
            time.sleep(5)
    if temp > 32:
        while temp >= 30:
            temp = diminuirTemp(temp)
            client.publish(f'v1/{usuario}/things/{client_id}/data/1', f'rel_hum,p={umi}') #publicando umidade
            client.publish(f'v1/{usuario}/things/{client_id}/data/0', f'temp,c={temp}')
            time.sleep(5)
    time.sleep(5)
