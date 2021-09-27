#Camada de abstração de hardware

import random

def temperatura():
    return random.randrange(20, 35)

def umidade():
    return random.randrange(40,50)

def aquecedor(estado: str):
    if estado == 'on':
        print('Aquecedor LIGADO')
    else:
        print('Aquecedor DESLIGADO')

def aumentarTemp(temp):
    temp += 1
    return temp

def diminuirTemp(temp):
    temp -= 1
    return temp