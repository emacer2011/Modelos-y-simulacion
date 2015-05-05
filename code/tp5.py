import numpy as np
from matplotlib.pylab import hist, show
import math
"""
Modelos y simulacion TP5 - Generacion de numeros
"""

# #normal
# norm = np.random.normal(10,1.6,100)
# hist(norm, 100)
# show()


# uniforme
def uniforme(tam):
    uni = np.random.uniform(size=tam)
    hist(uni, 10)
    show()

frecuencias = {'0':0,'0.1':0,'0.2':0,'0.3':0,'0.4':0,'0.5':0,'0.6':0,'0.7':0,'0.8':0,'0.9':0}


def intervalos(value):
    if value >= 0 and value < 0.1:
        frecuencias['0']+= 1 
    if value >= 0.1 and value < 0.2:
        frecuencias['0.1']+= 1
    if value >= 0.2 and value < 0.3:
        frecuencias['0.2']+= 1
    if value >= 0.3 and value < 0.4:
        frecuencias['0.3']+= 1
    if value >= 0.4 and value < 0.5:
        frecuencias['0.4']+= 1
    if value >= 0.5 and value < 0.6:
        frecuencias['0.5']+= 1
    if value >= 0.6 and value < 0.7:
        frecuencias['0.6']+= 1
    if value >= 0.7 and value < 0.8:
        frecuencias['0.7']+= 1
    if value >= 0.8 and value < 0.9:
        frecuencias['0.8']+= 1
    if value >= 0.9 and value <= 1.0:
        frecuencias['0.9']+= 1


def exponencial(tam):
    exp = np.random.exponential(1/6,tam)
    print(exp)
    media = np.average(exp)
    var = np.var(exp)
    desv = np.std(exp)
    print('media:', media)
    print('variancia:', var )
    print('desv std:', desv)
    inferior = media-1.96*(desv/math.sqrt(tam))
    superior = media+1.96*(desv/math.sqrt(tam))
    print(' %s <= u <= %s ' % (inferior, superior))
    hist(exp,10)
    show()

uniforme(100)
uniforme(1000)
exponencial(100)
exponencial(1000)