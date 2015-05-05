import numpy as np
from matplotlib.pylab import hist, show
"""
Modelos y simulacion TP6 - Etapas de simulacion y modelos
"""


CORRIDAS = 100
EXPERIMENTOS = 60


def kmaximo(valores, maximo):
    for k, v in valores.iteritems():
        if v == maximo:
            return k


def main():
    criticidad = {'sup': 0, 'inf': 0, 'med': 0}
    promedios = []
    for i in range(EXPERIMENTOS):
        tiempo = 0
        for j in range(CORRIDAS):
            sup = np.random.uniform(6, 12)
            med = np.random.uniform(6, 12)
            inf = np.random.uniform(6, 12)
            valores = {'sup': sup, 'med': med, 'inf': inf}
            maximo = max(valores.values())
            k_maximo = kmaximo(valores, maximo)
            valores[k_maximo] += 1
            criticidad[k_maximo] += 1
            tiempo += valores[k_maximo]
        promedios.append(tiempo/CORRIDAS)
    desv = np.std(promedios)
    promedio = np.average(promedios)
    print "Desvio %s " % desv
    print "Promedio %s" % promedio
    print "Intervalos de confianza %.2f <= u <= %.2f , con un 99%% de confianza" \
        % (promedio - 2.57 * desv, promedio + 2.57 * desv)
    for k, v in criticidad.iteritems():
        print "criticidad %s, %.2f %%" % (k, v*100.00/(CORRIDAS*EXPERIMENTOS))
    hist(promedios, 6)
    show()

if __name__ == '__main__':
    main()
