from senalDiscreta import SenalDiscreta
import matplotlib.pyplot as plt
import numpy as np
from IPython.display import Audio
from scipy.io.wavfile import read, write
import pyaudio
import wave
import numpy as np
import matplotlib.pyplot as plt

#Constantes and Variables:
formato = pyaudio.paInt16
canal = 1
frecuenciaDeMuestreo = 44100
tamanioVentana = 1024
tiempoGrabado = 3
nombreAudio = ''
audio = pyaudio.PyAudio()
flujo = audio.open(format=formato, channels=canal, rate=frecuenciaDeMuestreo,
                   input=True, frames_per_buffer=tamanioVentana)
#-----------------------------------------------------------------------------------------------------------------------


def setNomebreAudio(nombre):  # Establesemos el nombre del archivo de audio
    nombreAudio = nombre
    nombreAudio = nombreAudio+'.wav'


def getNomebreAudio():  # Obtenemos el Archivo de Audio
    return nombreAudio


def setTiempoDeGrabado(tiempo):
    tiempoGrabado = tiempo


def getTiempoDeGrabado():
    return tiempoGrabado


def grabarAudio():
    print('...Grabando')
    senial = []
    for i in range(int((frecuenciaDeMuestreo/tamanioVentana)*tiempoGrabado+1)):
        data = flujo.read(tamanioVentana)
        senialDato = np.fromstring(data, dtype=np.int16)
        senial.extend(senialDato)

    print('..fin..')

    wavefile = wave.open("entrada.wav", 'wb')
    wavefile.setnchannels(canal)
    wavefile.setsampwidth(audio.get_sample_size(formato))
    wavefile.setframerate(frecuenciaDeMuestreo)
    wavefile.writeframes(b''.join(senial))
    wavefile.close()


def obtenerNumpyDesdeAudio():
    # grabarAudio()
    # Leemos archivo obteniendo frecuencia y arreglo con canales
    Fr, data = read("entrada.wav")

    # Se toma como data solo el primer canal
    return SenalDiscreta(data, 0, False)


def obtenerSenalDiscretaDesdeAudio():
    # grabarAudio()
    # Leemos archivo obteniendo frecuencia y arreglo con canales
    Fr, data = read("entrada.wav")
    l = []
    for i in range(len(data)):
        l.append(data[i])
    return SenalDiscreta(l, 0, False)  # Se toma como data solo el primer canal


def obtenerAudioDesdeNumpy(senal):
    wavefile = wave.open('Salida.wav', 'wb')
    wavefile.setnchannels(canal)
    wavefile.setsampwidth(audio.get_sample_size(formato))
    wavefile.setframerate(frecuenciaDeMuestreo)
    wavefile.writeframes(b''.join(senal))
    wavefile.close()


def obtenerAudioDesdeSenalDiscreta(senal):
    Fr, data = read("entrada.wav")
    datos = data
    lenAux = len(data)
    senalDatos = senal.obtener_datos()
    for i in range(lenAux):
        datos[i] = senalDatos[i]
    wavefile = wave.open('Salida.wav', 'wb')
    wavefile.setnchannels(canal)
    wavefile.setsampwidth(audio.get_sample_size(formato))
    wavefile.setframerate(frecuenciaDeMuestreo)
    wavefile.writeframes(b''.join(datos))
    wavefile.close()
    #write("salida.wav", frecuenciaDeMuestreo, datos)


def graficarSenalDiscretaDeAudio(senalVieja, senalNueva):
    x = [0]
    datosViejos = senalVieja.obtener_datos()
    datosNuevos = senalNueva.obtener_datos()
    lenAux = len(datosViejos)
    for i in range(0, lenAux):
        x.append(i)
    plt.figure()
    plt.subplot(121)
    plt.plot(x[0:(lenAux-1)], np.array(datosViejos[0:(lenAux-1)]), 'o')
    plt.subplot(122)
    plt.plot(x[0:(lenAux-1)], np.array(datosNuevos[0:(lenAux-1)]), 'o')
    plt.show()
