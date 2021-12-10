from tkinter import *
import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib import pyplot
import numpy as np
from pydub import AudioSegment
from pydub.playback import play
#######Imports de Archivos#######
from senalDiscreta import *
from operacionSuma import *
from operacionResta import *
from operacionAmplificacionAtenuacion import *
from operacionReflejo import *
from operacionDesplazamiento import *
from operacionInterpolacionDiezmacion import *
from operacionConvolucion import *
from operacionFFT import *
#####Decalracion de varibles Globales#####

class tkinterApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title("Practica Señales - Equipo")
        self.minsize(850, 550)
        self.maxsize(850, 570)

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, Page1, Page2):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

# Thrid Window - Frame StarPage (Page 2)


class StartPage(tk.Frame):
    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Menú de Selección", font=("Consolas", 24))
        label.place(x=300, y=20)

        button3 = tk.Button(self, text="Secuencia Valores", cursor="hand2", bd=10, background="#063970",
                            height=0, font=("Consolas", 19),foreground="white", command=lambda: controller.show_frame(Page1))
        button3.place(x=480, y=100)
        button4 = tk.Button(self, text="Señal de audio", cursor="hand2", bd=10, background="#063970",
                            height=0, font=("Consolas", 19),foreground="white", command=lambda: controller.show_frame(Page2))
        button4.place(x=190, y=100)

        portada = """
            Programa que permite realizar Operaciones Básicas a una señal de entrada ingresada por el usuario, \n
            siendo ésta ya sea una secuencia de valores x(n) & h(n) o una señal de audio desde micrófono de máximo \n
            3 segundos, de acuerdo a un menú principal\n
            Integrantes:\n
            Balbuena Galván Alan Jair 3CV17  \n
            Carmona Aguirre Eduardo Samuel 3CV17 \n
            Enrique Adrian Alvarez Luis 3CV18 \n
            Nambo Velazquez Carlos 3CV17 \n
            Salinas Franco Carlos Enrique 3CV17 \n
           
        """
        tk.Label(self, text=portada,
                 font=("Consolas", 9)).place(x=10, y=170)

# Second Window - Frame 2 (Page 1)

class Page1(tk.Frame):
         
    def __init__(self, parent, controller):
        #######Definicion de las variables de esta clase#######
        global puntosEjeH 
        puntosEjeH = []# lista tiene los puntos donde se grafica las listas en el eje horizontal
        xesperiodica = BooleanVar()
        hesperiodica = BooleanVar()
        resultadoXn = StringVar()
        resultadoHn = StringVar()
        resultadoGn = StringVar()
        multiplicador = StringVar()
        udsDesplazamiento = IntVar()
        factorInterpolacionDiezmacion = StringVar()
        global newH # lista para H(n) de longitud estandar
        global newX # lista para H(n) de longitud estandar
        newH = []  # lista para H(n) de longitud estandar
        newX = []  # lista para X(n) de longitud estandar
    
        #> Varibles de Entrada para las Señales <#
        xL = StringVar()
        xO = StringVar()
        xR = StringVar()
        hL = StringVar()
        hO = StringVar()
        hR = StringVar()
        #######Graficar Reflejo #######
        def graficarReflejo(puntosEjeH,ejeX,ejeY,operacion):
            plt.subplot(311)
            markerline, stemlines, baseline = plt.stem(puntosEjeH, ejeX, '-.')
            pyplot.axhline(0, color="black")
            pyplot.axvline(0, color="black")
            plt.ylabel('En X')
            plt.subplot(313)
            markerline, stemlines, baseline = plt.stem(puntosEjeH, ejeY, '-.')
            plt.suptitle(operacion+' x(n) en el eje X y Y')
            plt.setp(baseline)
            plt.ylabel('En Y')
            pyplot.axhline(0, color="black")
            pyplot.axvline(0, color="black")
            plt.show()
        #######Graficar #######
        def graficar(puntosEjeH,newX,newH,resultado,operacion):
            plt.subplot(311)
            markerline, stemlines, baseline = plt.stem(puntosEjeH, newX, '-.')
            pyplot.axhline(0, color="black")
            pyplot.axvline(0, color="black")
            plt.ylabel('x(n)')
            plt.subplot(312)
            markerline, stemlines, baseline = plt.stem(puntosEjeH, newH, '-.')
            pyplot.axhline(0, color="black")
            pyplot.axvline(0, color="black")
            plt.ylabel('h(n)')
            plt.subplot(313)
            markerline, stemlines, baseline = plt.stem(puntosEjeH, resultado, '-.')
            plt.suptitle(operacion+' x(n) con h(n)')
            plt.setp(baseline)
            plt.ylabel('g(n)')
            pyplot.axhline(0, color="black")
            pyplot.axvline(0, color="black")
            plt.show()
        #######Obtener Secuencia#######
        def obtenerSecuencia(variable,senal):
            secuencia = variable + "(n) = ["
            for e in senal.obtener_datos():
                if e != "":
                    secuencia = secuencia + str(e) + ","
                else:
                    secuencia = secuencia + str(e)
            secuencia = secuencia + "]"
            return secuencia
        #######Definicion para emparejar puntosEjeHConInicio
        def emparejarPuntosEjeHConInicio(senal):
            global puntosEjeH
            puntosEjeH = []
            for i in range(senal.obtener_indice_inicio(), senal.obtener_longitud() + senal.obtener_indice_inicio()):
                puntosEjeH.append(i)
        #######Definicion para Emparejar los valores y regresar las listas de las señales#######
        def emparejarValores():
            global puntosEjeH,newH,newX
            #Obtenemos los valores de las entradas
            hLAux = hL.get().split(",")
            xLAux = xL.get().split(",")
            hRAux = hR.get().split(",")
            xRAux = xR.get().split(",")
            #Reset
            newH = []
            
            puntosEjeH = []
            
            if len(xLAux)>len(hLAux):
                for i in range(len(xLAux)-len(hLAux)):
                    newH.append(float(0))
                    
            for elemento in hLAux:
                if elemento != "":
                    newH.append(float(elemento))
                else:
                    newH.append(float(0))
            newH.append(float(hO.get()))
            
            for i in range(len(newH)):
                puntosEjeH.append(i*(-1))
                
            puntosEjeH.reverse()
                        
            for elemento in hRAux:
                if elemento != "":
                    newH.append(float(elemento))
                else:
                    newH.append(float(0))
            
            for i in range(len(xRAux) - len(hRAux)):
                newH.append(float(0))
            for i in range(len(newH)-len(puntosEjeH)):
                puntosEjeH.append(i+1)
                
            xls = []
            xrs = []
            for i in xLAux:
                if i != '':
                    xls.append(float(i))
            for i in xRAux:
                if i != '':
                    xrs.append(float(i))
            hls = []
            hrs = []
            for i in hLAux:
                if i != '':
                    hls.append(float(i))
            for i in hRAux:
                if i != '':
                    hrs.append(float(i))
        
            indice_x = 0
            if len(xLAux) > 0:
                if xLAux[0] != '':
                    indice_x = -len(xLAux)
            indice_h = 0
            if len(hLAux) > 0:
                if hLAux[0] != '':
                    indice_h = -len(hLAux)
            xn = SenalDiscreta(xls + [float(xO.get())] + xrs, indice_x, xesperiodica.get())
            hn = SenalDiscreta(hls + [float(hO.get())] + hrs, indice_h, hesperiodica.get())
            xn.empatar(hn)
            return [xn, hn]
        #######Concatenar Secuencia X #######
        def concatenarSecuenciaX():
            global puntosEjeH,newX
            xLAux = xL.get().split(",")
            xRAux = xR.get().split(",")
            newX = []
            puntosEjeH = []
            for elemento in xLAux:
                if elemento != "":
                    newX.append(float(elemento))
                else:
                    newX.append(float(0))
            newX.append(float(xO.get()))
            for i in range(len(newX)):
                puntosEjeH.append(i*(-1))
            puntosEjeH.reverse()
            for elemento in xRAux:
                if elemento != "":
                    newX.append(float(elemento))
                else:
                    newX.append(float(0))
            for i in range(len(newX)-len(puntosEjeH)):
                puntosEjeH.append(i+1)
            xn = SenalDiscreta(newX, -len(xLAux), xesperiodica.get())
            return [xn]
        #######Graficar Solo 2 #######
        def graficarSolo2(puntosEjeH,newX,resultado,operacion):
            plt.subplot(311)
            markerline, stemlines, baseline = plt.stem(puntosEjeH, newX, '-.')
            pyplot.axhline(0, color="black")
            pyplot.axvline(0, color="black")
            plt.ylabel('x(n)')
            plt.subplot(313)
            markerline, stemlines, baseline = plt.stem(puntosEjeH, resultado, '-.')
            plt.suptitle(operacion+' x(n)')
            plt.setp(baseline)
            plt.ylabel('g(n)')
            pyplot.axhline(0, color="black")
            pyplot.axvline(0, color="black")
            plt.show()
        #######Definicion de la Funcion Sumar (Suma) #######   
        def Sumar():
            print("Operacion Sumar")
            senales = emparejarValores()
            xn = senales[0]
            hn = senales[1]
            if xn.es_periodica():
                xn.expandir_periodo_izquierda(1)
                xn.expandir_periodo_derecha(1)
                hn.empatar(xn)

            if hn.es_periodica():
                hn.expandir_periodo_izquierda(1)
                hn.expandir_periodo_derecha(1)
                xn.empatar(hn)
            emparejarPuntosEjeHConInicio(xn)
            gn = obtenerSuma(xn, hn) # ------------------LINEA A CAMBIAR
            gn.empatar(xn)
            gn.empatar(hn)
            operacion = "Suma"           
            resultadoXn.set(obtenerSecuencia("x", xn))
            resultadoHn.set(obtenerSecuencia("h", hn))
            resultadoGn.set(obtenerSecuencia("g", gn))
            graficar(puntosEjeH, xn.obtener_datos(), hn.obtener_datos(), gn.obtener_datos(), operacion)

        def Restar():
            senales = emparejarValores()
            xn = senales[0]
            hn = senales[1]
            if xn.es_periodica():
                xn.expandir_periodo_izquierda(1)
                xn.expandir_periodo_derecha(1)
                hn.empatar(xn)
            if hn.es_periodica():
                hn.expandir_periodo_izquierda(1)
                hn.expandir_periodo_derecha(1)
                xn.empatar(hn)
            emparejarPuntosEjeHConInicio(xn)
            gn = obtenerResta(xn, hn)  
            gn.empatar(xn)
            gn.empatar(hn)
            operacion = "RESTA"
            resultadoXn.set(obtenerSecuencia("x", xn))
            resultadoHn.set(obtenerSecuencia("h", hn))
            resultadoGn.set(obtenerSecuencia("g", gn))
            graficar(puntosEjeH, xn.obtener_datos(),hn.obtener_datos(), gn.obtener_datos(), operacion)
        #######Amplificar y Atenuar #######
        def amplificarAtenuar():
            global newX
            concatenarSecuenciaX()
            gn = obtenerAmplificacionAtenuacion(newX, float(multiplicador.get())) 

            if float(multiplicador.get())>1:
                operacion = "Amplificacion"
            else:
                operacion = "Atenuacion" 
            resx = "x(n)={"
            for e in newX:
                if e != "":
                    resx = resx + str(e) + ","
                else:
                     resx = resx + str(e)
            resx = resx + "}"

            resg = "g(n)={"
            for e in gn:
                if e != "":
                    resg = resg+str(e)+","
                else:
                    resg = resg + str(e)
            resg = resg+"}"
            
            resultadoXn.set(resx)
            resultadoGn.set(resg)
            graficarSolo2(puntosEjeH, newX, gn, operacion)
        #######Reflejo En X y Y #######
        def reflejoEnXyY():
            senal = concatenarSecuenciaX()
            xn = senal[0]
            
            senal = SenalDiscreta(xn.obtener_datos(),xn.obtener_indice_inicio(),xn.es_periodica())
            gnY = obtener_reflejoY(xn)
            gnY = obtener_reflejoY(xn)

            datosAux = xn.obtener_datos()
            for i in range(len(datosAux)):
                datosAux[i] = datosAux[i] * -1

            gnX = SenalDiscreta(datosAux, xn.obtener_indice_inicio(), xn.es_periodica())

            originalData =  senal.obtener_datos()[:]
            for i in range(len(originalData)):
                originalData[i]*=-1
            senal.asignar_datos(originalData)

            operacion = "Reflejar" # ------------------------LINEA A CAMBIAR
            # Se configura la GU
            #configurarPantalla(operacion, obtenerSecuencia("f", senal), obtenerSecuencia("x", gnX), obtenerSecuencia("y", gnY))
            resultadoXn.set(obtenerSecuencia("f", senal))
            resultadoHn.set(obtenerSecuencia("x", gnX))
            resultadoGn.set(obtenerSecuencia("y", gnY))
            # Grafica
            graficarReflejo(puntosEjeH, gnX.obtener_datos(), gnY.obtener_datos(), operacion)
        #######Operacion Desplazar #######
        def desplazar():
            global newX,newX2,puntosEjeH
            xn = concatenarSecuenciaX()[0]
            xncopia = SenalDiscreta(xn.obtener_datos(), xn.obtener_indice_inicio(), xn.es_periodica())
            gn = obtener_Desplazamiento(xn, udsDesplazamiento.get())
            operacion = "Desplazar"
            # Se configura la GUI
            #configurarPantallaDeUnSoloValor(operacion, xncopia.obtener_datos(), gn.obtener_datos())
            # Grafica
            xnn = xncopia.obtener_datos()
            gnn = gn.obtener_datos()
            
            resx = "x(n)={"
            for e in xnn:
                if e != "":
                    resx = resx + str(e) + ","
                else:
                    resx = resx + str(e)
            resx = resx + "}"

            resg = "g(n)={"
            for e in gnn:
                if e != "":
                    resg = resg+str(e)+","
                else:
                    resg = resg + str(e)
            resg = resg+"}"

            resultadoXn.set(resx)
            resultadoGn.set(resg)
            graficarSolo2(range(gn.obtener_indice_inicio(), gn.obtener_longitud() + gn.obtener_indice_inicio()), xncopia.obtener_datos(), gn.obtener_datos(), operacion)
        ####### Diezmar #######
        def diezmar():
            senales = concatenarSecuenciaX()
            xn = senales[0]
            operacion = "Diezmación"
            if(xn.obtener_indice_inicio() > 0):
                xn.asignar_indice_inicio(-xn.obtener_indice_inicio())
            # Se realiza la operación
            gn = obtenerDiezmacion(xn, int(factorInterpolacionDiezmacion.get()))
            
            # Se configura la GUI
            #configurarPantallaDeUnSoloValor(operacion, xn.obtener_datos(), gn.obtener_datos())
            xnn = xn.obtener_datos()
            gnn = gn.obtener_datos()
            resx = "x(n)={"
            for e in xnn:
                if e != "":
                    resx = resx + str(e) + ","
                else:
                    resx = resx + str(e)
            resx = resx + "}"

            resg = "g(n)={"
            for e in gnn:
                if e != "":
                    resg = resg+str(e)+","
                else:
                    resg = resg + str(e)
            resg = resg+"}"
            resultadoXn.set(resx)
            resultadoGn.set(resg)
            # Grafica
            gn.empatar(xn)
            graficarSolo2(range(gn.obtener_indice_inicio(), gn.obtener_longitud()+gn.obtener_indice_inicio()), xn.obtener_datos(), gn.obtener_datos(), operacion)
            
        ####### Interpolar #######
        def interpolar():
            #Obtiene datos de la GUI
            seniales = concatenarSecuenciaX()
            xn = seniales[0]
            operacion = "Interpolación"
            if(xn.obtener_indice_inicio() > 0):
                xn.asignar_indice_inicio(-xn.obtener_indice_inicio())
            # Se realiza la operación
            gn = obtenerInterpolacion(xn, int(factorInterpolacionDiezmacion.get()))
            # Se configura la GUI
            xnn = xn.obtener_datos()
            gnn = gn.obtener_datos()
            resx = "x(n)={"
            for e in xnn:
                if e != "":
                    resx = resx + str(e) + ","
                else:
                    resx = resx + str(e)
            resx = resx + "}"

            resg = "g(n)={"
            for e in gnn:
                if e != "":
                    resg = resg+str(e)+","
                else:
                    resg = resg + str(e)
            resg = resg+"}"
            resultadoXn.set(resx)
            resultadoGn.set(resg)
            # Grafica
            gn.empatar(xn)
            graficarSolo2(range(gn.obtener_indice_inicio(), gn.obtener_longitud()+gn.obtener_indice_inicio()), xn.obtener_datos(), gn.obtener_datos(), operacion)
        def convolusionar():
            senales = emparejarValores()
            xn = senales[0]
            hn = senales[1]
            gn = convolucionar(xn, hn) # ------------------LINEA A CAMBIAR

            # Se realiza emparejamiento
            xn.empatar(gn)
            hn.empatar(gn)
            emparejarPuntosEjeHConInicio(gn)

            operacion = "Convolución" # ------------------------LINEA A CAMBIAR
            # Se configura la GUI
            #configurarPantalla(operacion, obtenerSecuencia("x", xn), obtenerSecuencia("h", hn), obtenerSecuencia("g", gn))
            resultadoXn.set(obtenerSecuencia("x", xn))
            resultadoHn.set(obtenerSecuencia("h", hn))
            resultadoGn.set(obtenerSecuencia("g", gn))
            # Grafica
            graficar(puntosEjeH, xn.obtener_datos(), hn.obtener_datos(), gn.obtener_datos(), operacion)

        def fft():
            senales = concatenarSecuenciaX()
            xn = senales[0]
            gn = obtener_FFT(xn) 
            operacion = "FFT" 
            xnn = xn.obtener_datos()
            gnn = gn.obtener_datos()
            resx = "x(n)={"
            for e in xnn:
                if e != "":
                    resx = resx + str(e) + ","
                else:
                    resx = resx + str(e)
            resx = resx + "}"

            resg = "g(n)={"
            for e in gnn:
                if e != "":
                    resg = resg+str(e)+","
                else:
                    resg = resg + str(e)
            resg = resg+"}"
            resultadoXn.set(resx)
            resultadoGn.set(resg)
                    
        tk.Frame.__init__(self, parent)
        #######LABEL DE TITULO SECUENCIA DE VALORES#######
        label1 = tk.Label(self, text="Secuencia Valores", font=("Consolas", 16))
        label1.grid(row=0, column=2, padx=0, pady=0)
        #######EMPIEZA CONTENIDO DE WIDGETS#######
        labelOrigen = tk.Label(self,text="Origen",font=("Consolas", 12))
        labelOrigen.grid(row=1, column=2, padx=0, pady=0)
        
        #######Fila Valores de H(n)#######
        labelXn = tk.Label(self,text="X(n) {",font=("Consolas", 14))
        labelXn.grid(row=2,column=0,pady=0)
        
        entryIzqXn = tk.Entry(self, font=("Consolas", 12),textvariable=xL)
        entryIzqXn.grid(row=2, column=1, padx=0, pady=0)
        
        entryXn = tk.Entry(self,font=("Consolas",12),textvariable=xO)
        entryXn.grid(row=2,column=2,padx=0,pady=0)
        
        entryDerXn = tk.Entry(self,font=("Consolas",12),textvariable=xR)
        entryDerXn.grid(row=2,column=3,padx=0,pady=0)
        
        labelCor = tk.Label(self,text="}",font=("Consolas", 12))
        labelCor.grid(row=2, column=4, padx=0, pady=0)
        
        checkPerXn = tk.Checkbutton(self,text="Periódica",font=("Consolas",12),variable=xesperiodica)
        checkPerXn.grid(row=2,column=5,padx=0,pady=0)

        #######Fila Valores de H(n)#######
        labelHn = tk.Label(self,text="H(n) {",font=("Consolas", 14))
        labelHn.grid(row=3,column=0)
        
        entryIzqHn = tk.Entry(self, font=("Consolas", 12),textvariable=hL)
        entryIzqHn.grid(row=3, column=1, padx=0, pady=0)

        entryHn = tk.Entry(self, font=("Consolas", 12),textvariable=hO)
        entryHn.grid(row=3, column=2, padx=0, pady=0)

        entryDerHn = tk.Entry(self, font=("Consolas", 12),textvariable=hR)
        entryDerHn.grid(row=3, column=3, padx=0, pady=0)
        
        labelCor2 = tk.Label(self,text="}",font=("Consolas", 12))
        labelCor2.grid(row=3, column=4, padx=0, pady=0)
        
        checkPerHn = tk.Checkbutton(self,text="Periódica",font=("Consolas",12),variable=hesperiodica)
        checkPerHn.grid(row=3,column=5,padx=0,pady=0)
        #######BOTONES DE OPERACIONES#######
        
        btnSuma = tk.Button(self, text="Sumar", font=(
            "Consolas", 12), background="#063970", foreground="white", cursor="hand2",command=Sumar)
        btnSuma.grid(row=4,column=1,padx=0,pady=5)
        
        btnResta = tk.Button(self, text="Restar", font=(
            "Consolas", 12), background="#063970", foreground="white", cursor="hand2",command=Restar)
        btnResta.grid(row=4,column=2,padx=0,pady=5)
        
        btnAmpli = tk.Button(self, text="Amplificación/Atenuación", font=(
            "Consolas", 10), background="#063970", foreground="white", cursor="hand2",command=amplificarAtenuar)
        btnAmpli.grid(row=5,column=1,padx=0,pady=5)
        
        lblMult = tk.Label(self,text="Multiplicador : ",font=("Consolas",10))
        lblMult.grid(row=5,column=2,padx=0,pady=5)
        
        entryMult = tk.Entry(self, font=("Consolas", 12),textvariable=multiplicador)
        entryMult.grid(row=5,column=3,padx=0,pady=5)
        
        btnReflejo = tk.Button(self, text="Reflejo en X y Y", font=(
            "Consolas", 12), background="#063970", foreground="white", cursor="hand2",command=reflejoEnXyY)
        btnReflejo.grid(row=6,column=1,padx=0,pady=5)
        
        btnDespla = tk.Button(self, text="Desplazamiento", font=(
            "Consolas", 12), background="#063970", foreground="white", cursor="hand2", command=desplazar)
        btnDespla.grid(row=7,column=1,padx=0,pady=5)
        
        lblDespla = tk.Label(self,text="U a desplazar : ",font=("Consolas",10))
        lblDespla.grid(row=7,column=2,padx=0,pady=5)
        
        entryDespla = tk.Entry(self, font=("Consolas", 12),
                               textvariable=udsDesplazamiento)
        entryDespla.grid(row=7, column=3, padx=0, pady=5)
        
        btnDiez = tk.Button(self, text="Diezmación", font=(
            "Consolas", 12), background="#063970", foreground="white", cursor="hand2", command=diezmar)
        btnDiez.grid(row=8, column=1, padx=0, pady=5)
        
        btnInterpo = tk.Button(self, text="Interpolación", font=(
            "Consolas", 12), background="#063970", foreground="white", cursor="hand2", command=interpolar)
        btnInterpo.grid(row=8, column=2, padx=0, pady=5)
        
        lblFactor = tk.Label(self,text="Factor Diez/Inter : ",font=("Consolas",10))
        lblFactor.grid(row=8,column=3,padx=0,pady=5)
        
        entryDiezInter = tk.Entry(self, font=("Consolas", 12),textvariable=factorInterpolacionDiezmacion)
        entryDiezInter.grid(row=8, column=5, padx=0, pady=5)
        
        btnConvo = tk.Button(self, text="Convolución", font=(
            "Consolas", 12), background="#063970", foreground="white", cursor="hand2", command=convolusionar)
        btnConvo.grid(row=9, column=1, padx=0, pady=5)
        
        btnFFT = tk.Button(self, text="FFT", font=(
            "Consolas", 12), background="#063970", foreground="white", cursor="hand2",command=fft)
        btnFFT.grid(row=10, column=1, padx=0, pady=5)
        #######Pintar Resultados########
        lblResultadoXn = tk.Label(self,text="Resultado",font=("Consolas",10))
        lblResultadoXn.grid(row=11, column=1, padx=0, pady=5,columnspan=4)
        
        lblResultadoXn = tk.Entry(self,font=("Consolas",10),textvariable=resultadoXn,width=70)
        lblResultadoXn.grid(row=12, column=1, padx=0, pady=5,columnspan=4)
        
        lblResultadoHn = tk.Entry(self,font=("Consolas", 10), textvariable=resultadoHn, width=70)
        lblResultadoHn.grid(row=13, column=1, padx=0, pady=5,columnspan=4)
        
        lblResultadoGn = tk.Entry(self,font=("Consolas", 10), textvariable=resultadoGn, width=70)
        lblResultadoGn.grid(row=14, column=1, padx=0, pady=5,columnspan=4)
        #######BOTON REGRESAR A PAGINA PRINCIPAL#######
        button1 = tk.Button(self, text="Regresar",background="#063970",foreground="white",cursor="hand2",bd=5,
                            command=lambda: controller.show_frame(StartPage))
        button1.grid(row=15, column=2, padx=0, pady=5)

# Thrid Window - Frame 3 (Page 2)


class Page2(tk.Frame):
    def __init__(self, parent, controller):
        
        estadoGrabacion = StringVar()
        multiplicador = StringVar()
        udsDesplazamiento = IntVar()
        factorInterpolacionDiezmacion = StringVar()
        ####### Grabar Audio ######
        def grabarGUI():
            estadoGrabacion.set("Grabando...")
            global senal
            grabarAudio()
            senal = obtenerSenalDiscretaDesdeAudio()
            estadoGrabacion.set("Audio grabado")
            
        def reproducirEntrada():
            song = AudioSegment.from_wav("entrada.wav")
            play(song)

        def reproducirSalida():
            song = AudioSegment.from_wav("Salida.wav")
            play(song)
        ####### Amplificar y Atenuar #######
        def amplificarAtenuarAudio():
                # Se realiza la operación
            gn = obtenerAmplificacionAtenuacion(senal.obtener_datos().copy(), float(multiplicador.get()))

            if float(multiplicador.get())>1:
                operacion = "Amplificacion"
            else:
                operacion = "Atenuacion"
            obtenerAudioDesdeSenalDiscreta(SenalDiscreta(gn, 0, False))
            # Grafica
            graficarInterpolacionDiezmacion(senal.obtener_datos(), gn, operacion)
        ####### Desplazar Audio #######
        def desplazarAudio():
            DesplazarCompletoAudio(udsDesplazamiento.get()*int(44100/2))
        ###### Interpolar y Diezmar Audio #######
        def diezmarAudio():
            xn = SenalDiscreta(senal.obtener_datos().copy(), 0, False)
            operacion = "Diezmación"
            factor = int(factorInterpolacionDiezmacion.get())
            # Se realiza la operación
            gn = obtenerDiezmacion(xn, factor)
            # Grafica
            gn.asignar_indice_inicio(0)
            gn.empatar(xn)
            obtenerAudioDesdeSenalDiscreta(gn)
            graficarInterpolacionDiezmacion(xn.obtener_datos(), gn.obtener_datos(), operacion)

        def interpolarAudio():
            xn = SenalDiscreta(senal.obtener_datos().copy(), 0, False)
            operacion = "Interpolación"
            factor = int(factorInterpolacionDiezmacion.get())
            # Se realiza la operación
            gn = obtenerInterpolacion(xn, factor)
            # Grafica
            gn.empatar(xn)
            obtenerAudioDesdeSenalDiscreta(gn)
            graficarInterpolacionDiezmacion(xn.obtener_datos(), gn.obtener_datos(), operacion)
        
        ####### FFT AUDIO #######
        def fft_audio():
            T1N = graficarFFT2(obtenerNumpyDesdeAudio().obtener_datos())
            obtenerAudioDesdeNumpy(T1N)
            plt.subplot(121)
            plt.plot(T1N)
            plt.show()
        ####### Reflejo X #######
        def reflejarEnX():
            print("Aqui deberia de ir el codigo de Reflejo X pero no funciona bien")
        ####### Reflejo Y #######
        def reflejarEnY():
            print("Aqui deberia de ir el codigo de Reflejo Y pero no funciona bien")
            
        
        tk.Frame.__init__(self, parent)
        #######Titulo de la Pagina Señal de Audio#######
        label1 = tk.Label(self, text="Señal de Audio", font=("Consolas", 16))
        label1.grid(row=0, column=2, padx=0, pady=5)
        #######Comienzo Widgets#######
        
        btnGrabar = tk.Button(self, text="Grabar", font=(
            "Consolas", 12), background="#063970", foreground="white", cursor="hand2", command=grabarGUI)
        btnGrabar.grid(row=2,column=1,padx=30,pady=5)
        
        labelGrabar = tk.Label(self, text="Sin Grabar", font=(
            "Consolas", 12), foreground="red", textvariable=estadoGrabacion)
        labelGrabar.grid(row=2, column=2, padx=0, pady=5)
                
        btnEEntrada = tk.Button(self, text="Escuchar Entrada", font=(
            "Consolas", 12), background="#063970", foreground="white", cursor="hand2",command=reproducirEntrada)
        btnEEntrada.grid(row=3,column=1,padx=0,pady=5)
        
        btnESalida = tk.Button(self, text="Escuchar Salida", font=(
            "Consolas", 12), background="#063970", foreground="white", cursor="hand2",command=reproducirSalida)
        btnESalida.grid(row=3, column=2, padx=0, pady=5)
        
        btnAmpli = tk.Button(self, text="Amplificación/Atenuación", font=(
            "Consolas", 10), background="#063970", foreground="white", cursor="hand2", command=amplificarAtenuarAudio)
        btnAmpli.grid(row=5, column=1, padx=10, pady=15)

        lblMult = tk.Label(self, text="Multiplicador : ",
                           font=("Consolas", 10))
        lblMult.grid(row=5, column=2, padx=0, pady=5)

        entryMult = tk.Entry(self, font=("Consolas", 12),textvariable=multiplicador)
        entryMult.grid(row=5, column=3, padx=0, pady=5)
        
        btnReflejoX = tk.Button(self, text="Reflejo X", font=(
            "Consolas", 12), background="#063970", foreground="white", cursor="hand2",command=reflejarEnX)
        btnReflejoX.grid(row=6,column=1,padx=0,pady=5)
        
        btnReflejoY = tk.Button(self, text="Reflejo Y", font=(
            "Consolas", 12), background="#063970", foreground="white", cursor="hand2",command=reflejarEnY)
        btnReflejoY.grid(row=6,column=2,padx=0,pady=5)
        
        btnDespla = tk.Button(self, text="Desplazamiento", font=(
            "Consolas", 12), background="#063970", foreground="white", cursor="hand2", command=desplazarAudio)
        btnDespla.grid(row=7, column=1, padx=0, pady=5)

        lblDespla = tk.Label(self, text="U a desplazar : ",
                             font=("Consolas", 10))
        lblDespla.grid(row=7, column=2, padx=0, pady=5)

        entryDespla = tk.Entry(self, font=("Consolas", 12),
                               textvariable=udsDesplazamiento)
        entryDespla.grid(row=7, column=3, padx=0, pady=5)

        btnDiez = tk.Button(self, text="Diezmación", font=(
            "Consolas", 12), background="#063970", foreground="white", cursor="hand2", command=diezmarAudio)
        btnDiez.grid(row=8, column=1, padx=0, pady=5)

        btnInterpo = tk.Button(self, text="Interpolación", font=(
            "Consolas", 12), background="#063970", foreground="white", cursor="hand2", command=interpolarAudio)
        btnInterpo.grid(row=8, column=2, padx=0, pady=5)

        lblFactor = tk.Label(
            self, text="Factor Diez/Inter : ", font=("Consolas", 10))
        lblFactor.grid(row=8, column=3, padx=0, pady=5)

        entryDiezInter = tk.Entry(self, font=("Consolas", 12),textvariable=factorInterpolacionDiezmacion)
        entryDiezInter.grid(row=8, column=5, padx=0, pady=5)
        
        btnFFT = tk.Button(self, text="FFT", font=(
            "Consolas", 12), background="#063970", foreground="white", cursor="hand2", command=fft_audio)
        btnFFT.grid(row=10, column=1, padx=0, pady=5)
        
        #######Boton de Regreso a Pagina Principal######
        button1 = tk.Button(self, text="Regresar",background="#063970",foreground="white",cursor="hand2",bd=5,
                            command=lambda: controller.show_frame(StartPage))
        button1.grid(row=11, column=2, padx=0, pady=0)

app = tkinterApp()
app.mainloop()
