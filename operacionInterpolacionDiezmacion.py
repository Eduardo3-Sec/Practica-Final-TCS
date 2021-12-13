from senalDiscreta import SenalDiscreta
import matplotlib.pyplot as plt
from matplotlib import pyplot
import numpy as np
from manejadorDeSenales import obtenerAudioDesdeSenalDiscreta
from manejadorDeSenales import obtenerSenalDiscretaDesdeAudio

def obtenerPendiente(y1, y2, factor):
    return float((y2-y1)/(factor))


def a1decimal(n):
    return float(int(n*10))/10


def obtenerInterpolacion(xn, factor):
    x = xn.obtener_datos()
    y = []
    # solo funciona para listas del mismo tamaño
    for i in range(0, len(x)-1):
        m = obtenerPendiente(x[i], x[i+1], factor)
        y.append(x[i])
        for j in range(1, factor):
            y.append(a1decimal(float(x[i]+(m*j))))
    y.append(x[i+1])
    return SenalDiscreta(y, xn.obtener_indice_inicio()*factor, xn.es_periodica())


def obtenerDiezmacion(xn, factor):
    x = xn.obtener_datos().copy()
    inicio = xn.obtener_indice_inicio()
    origen = xn.obtener_origen()
    index = int(0)
    for i in range(len(x)):
        pointer = inicio+i
        if pointer % factor != 0:
            del x[index]
            if pointer >= 0:
                origen -= 1
        else:
            index += 1
    return SenalDiscreta(x, -origen, xn.es_periodica())


def graficarInterpolacionDiezmacion(newX, resultado, operacion):
    #x(n) en la primera posicion
    plt.subplot(211)
    plt.plot(range(0, len(newX)), newX)
    plt.ylabel('x(n)')
    
    plt.subplot(212)
    plt.plot(range(0, len(resultado)), resultado)
    plt.ylabel('g(n)')
    plt.suptitle(operacion+' de x(n)')
    plt.show()
