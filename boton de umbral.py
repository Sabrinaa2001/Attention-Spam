import time
import numpy as np

umbral = []
cont = 0
tiempo_inicio = time.time()

eeg = np.random.rand(10, 10)  #Remplazar por entrada de unicorn

botum = 1 #obtener del unity c#

if botum == 1:
    while cont < 10:
        umbral.append(eeg)  # Esto agregará la matriz completa, no solo una fila
        cont += 1

    umbral = np.concatenate(umbral, axis=0)
    umbral = umbral[:, 4:7]
    umbral_promedio = np.mean(umbral, axis=0)
    umbral_final = np.mean(umbral_promedio)
    print("Umbral calculado:", umbral_final)
