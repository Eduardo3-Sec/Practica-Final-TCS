from senalDiscreta import SenalDiscreta
from manejadorDeSenales import *


def obtener_reflejo(senal, tipoReflejo):
    if(tipoReflejo == 1):  # Para reflejo sobre el eje X
        datosAux = senal.obtener_datos()
        for i in range(len(datosAux)):
            datosAux[i] = datosAux[i] * -1  # Voltea la secuencia de valores
        return SenalDiscreta(datosAux, senal.obtener_indice_inicio(), senal.es_periodica())
    elif(tipoReflejo == 2):  # Para reflejo sobre el eje y
        datosAux = senal.obtener_datos()[::-1]
        inicioAux = - len(datosAux) + 1 - senal.obtener_indice_inicio()
        return SenalDiscreta(datosAux, inicioAux, senal.es_periodica())


def obtener_reflejoX(senal):

    datosAux = senal.obtener_datos()
    for i in range(len(datosAux)):
        datosAux[i] = datosAux[i] * -1  # Voltea la secuencia de valores
    return SenalDiscreta(datosAux, senal.obtener_indice_inicio(), senal.es_periodica())


def obtener_reflejoY(senal):

    datosAux = senal.obtener_datos()
    datosAux = senal.obtener_datos()[::-1]
    inicioAux = - len(datosAux) + 1 - senal.obtener_indice_inicio()
    return SenalDiscreta(datosAux, inicioAux, senal.es_periodica())


def reflejar_todo(tipoReflejo=2):
    senal = obtenerSenalDiscretaDesdeAudio()
    if(tipoReflejo == 1):  # Para reflejo sobre el eje X
        datosAux = senal.obtener_datos()
        for i in range(len(datosAux)):
            datosAux[i] = datosAux[i] * -1  # Voltea la secuencia de valores
        senalAux = SenalDiscreta(
            datosAux, senal.obtener_indice_inicio(), senal.es_periodica())
    elif(tipoReflejo == 2):  # Para reflejo sobre el eje y
        datosAux = senal.obtener_datos()[::-1]
        inicioAux = - len(datosAux) + 1 - senal.obtener_indice_inicio()
        senalAux = SenalDiscreta(datosAux, inicioAux, senal.es_periodica())
    graficarSenalDiscretaDeAudio(senal, senalAux)
    obtenerAudioDesdeSenalDiscreta(senalAux)
