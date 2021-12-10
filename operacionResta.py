from senalDiscreta import *


def obtenerResta(x, h):
    """
    Función que resta dos señales discretas y devuelve el resultado

    Parameters:
        x (SenialDiscreta): Señal discrecta x(n)
        h (SenialDiscreta): Señal discrecta h(n)

    Returns:
        SenialDiscreta: El resultado de x(n)-h(n)
    """
    g = []
    if x.obtener_longitud() == h.obtener_longitud():
        for i in range(x.obtener_longitud()):
            g.append(x.obtener_datos()[i] - h.obtener_datos()[i])

    gn = SenalDiscreta(g, x.obtener_indice_inicio(), x.es_periodica())

    return gn
