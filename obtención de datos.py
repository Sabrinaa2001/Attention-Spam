import socket
import time
import UnicornPy
import numpy as np
import pandas as pd
import scipy
from scipy.fft import fft
import matplotlib.pyplot as plt
from scipy import signal

# Configuración del servidor
server_ip = '127.0.0.1'  # Cambia esto a la dirección IP del servidor
server_port = 12345
# Crear un socket TCP/IP
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Conectar al servidor
client_socket.connect((server_ip, server_port))
##########################################################################
# Enviar datos al servidor
message = "Hola desde Python"
client_socket.sendall(message.encode())
# Recibir datos del servidor
data = client_socket.recv(1024)
print('Mensaje del servidor:', data.decode())
###########################################################################

def boton_umbral(data1):
    umbral = []
    cont = 0
    data1 = np.random.rand(10, 10)  #Remplazar por entrada de unicorn
    botum = 1 #obtener del unity c#
    if botum == 1:
        while cont < 10:
            umbral.append(data1)  # Esto agregará la matriz completa, no solo una fila
            cont += 1
    umbral = np.concatenate(umbral, axis=0)
    umbral = umbral[:, 4:7]
    umbral_promedio = np.mean(umbral, axis=0)
    umbral_final = np.mean(umbral_promedio)

def main():
    # Specifications for the data acquisition.
    #-------------------------------------------------------------------------------------
    TestsignaleEnabled = False;
    FrameLength = 1;
    AcquisitionDurationInSeconds = 10; #n�mero de duraci�n en segundos
    DataFile = "eeg.csv";

    print("Unicorn Acquisition Example")
    print("---------------------------")
    print()

    try:
        # Get available devices.
        #-------------------------------------------------------------------------------------

        # Get available device serials.
        deviceList = UnicornPy.GetAvailableDevices(True) #una de las funciones de UnicornPy

        if len(deviceList) <= 0 or deviceList is None:
            raise Exception("No device available.Please pair with a Unicorn first.")

        # Selecci�n
        deviceID = 0

        # Open selected device.
        #-------------------------------------------------------------------------------------
        print()
        print("Trying to connect to '%s'." %deviceList[deviceID])
        device = UnicornPy.Unicorn(deviceList[deviceID]) #Con esto se conectan al dispositivo
        print("Connected to '%s'." %deviceList[deviceID])
        print()

        # Create a file to store data.
        file = open(DataFile, "wb")

        # Initialize acquisition members.
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        numberOfAcquiredChannels = device.GetNumberOfAcquiredChannels()

        # Allocate memory for the acquisition buffer.
        receiveBufferBufferLength = FrameLength * numberOfAcquiredChannels * 4
        receiveBuffer = bytearray(receiveBufferBufferLength)

        try:
            # Start data acquisition.
            #-------------------------------------------------------------------------------------
            device.StartAcquisition(TestsignaleEnabled)
            print("Data acquisition started.")

            # Calculate number of get data calls. Cu�ntas veces se obtienen datos borrar
            numberOfGetDataCalls = int(AcquisitionDurationInSeconds * UnicornPy.SamplingRate / FrameLength);
        
            # Limit console update rate to max. 25Hz or slower to prevent acquisition timing issues.                   
            consoleUpdateRate = int((UnicornPy.SamplingRate / FrameLength) / 25.0);
            if consoleUpdateRate == 0:
                consoleUpdateRate = 1

            data=[0, 0, 0]
            umbral_final=0

            # Acquisition loop.
            #-------------------------------------------------------------------------------------
            for i in range (0,numberOfGetDataCalls):
                # Receives the configured number of samples from the Unicorn device and writes it to the acquisition buffer.
                device.GetData(FrameLength,receiveBuffer,receiveBufferBufferLength)
                # Convert receive buffer to numpy float array 
                F=250 #Sampling frequency (Hz)
                if i % 100==0:
                    eeg = np.frombuffer(receiveBuffer, dtype=np.float32, count=numberOfAcquiredChannels * FrameLength)
                    eeg = np.reshape(eeg, (FrameLength, numberOfAcquiredChannels))
                    np.savetxt(file,eeg,delimiter=',',fmt='%.3f',newline='\n')
                    fft_vals = np.absolute(np.fft.rfft(eeg)) # Get real amplitudes of FFT (only in postive frequencies)
                    fft_freq = np.fft.rfftfreq(len(eeg), 1.0/F) # Get frequencies for amplitudes in Hz

                Time=eeg[:,16]
                E1=eeg[0, 5]
                E2=eeg[0, 6]
                E3=eeg[0, 7]
                E=[E1, E2, E3]
                data=np.vstack((data,E))
                N=len(data) #Number of samples
                T=N/F # Period (s)

                eeg_bands = {'Delta': (0, 4),
                             'Theta': (4, 8),
                             'Alpha': (8, 12),
                             'Beta': (12, 30),
                             'Gamma': (30, 45)} # Define EEG bands


                eeg_band_fft = dict() # Take the mean of the fft amplitude for each EEG band
                for band in eeg_bands:
                    freq_ix = np.where((fft_freq >= eeg_bands[band][0]) & (fft_freq <= eeg_bands[band][1]))[0]
                    if len(freq_ix) > 0:
                        eeg_band_fft[band] = np.mean(fft_vals[freq_ix])
                    else:
                        eeg_band_fft[band] = np.nan  # Si no hay datos en la banda, se asigna NaN (Not a Number)
                # Crea un DataFrame para los datos
                df = pd.DataFrame(columns=['band', 'val'])
                df['band'] = eeg_bands.keys()
                df['val'] = [eeg_band_fft[band] for band in eeg_bands]
                # Grafica los datos
                ax = df.plot.bar(x='band', y='val', legend=False)
                ax.set_xlabel("Banda EEG")
                ax.set_ylabel("Amplitud media de la banda")

                #eeg.insert(loc=0, column='Time', value=np.arange(1, len(eeg) + 1)) # Add time vector
                grabacion=1 #Data to get from Unity
                matriznueva=[0, 0, 0,]
                boton_umbral(data)
                #matriznueva = eeg # New matrix = old one
                #matriznueva = matriznueva.drop(columns=matriznueva.columns[0]) # Drop time
                if grabacion == 1: # Start
                    matriznueva = np.vstack((matriznueva, data))
                    print(matriznueva)
                    #matriznueva.insert(loc=0, column='Time', value=np.arange(1, len(matriznueva) + 1)) # Reinsert time to start at 0
                if grabacion == 2: # End
                    #matriznueva = matriznueva.iloc[:N,:] # Stop
                    #Activar el boton de post-p
                    print("finaliza grabación")

                y=df['val'] # Get amplitude
                for band in eeg_bands: # Compare occipital averages vs others
                    if np.average(y[[0,1]])>np.average(y[[2,3,4]]):
                        concentracion=1
                    else:
                        concentracion=0
                    info=[]
                    info=np.hstack((info, concentracion))
            print(info)                

                # Update console to indicate that the data acquisition is running.
                #if i % consoleUpdateRate == 0:
                 #   print('.',end='',flush=True)

            # Stop data acquisition.
            #-------------------------------------------------------------------------------------
            device.StopAcquisition();
            print()
            print("Data acquisition stopped.");

        except UnicornPy.DeviceException as e:
            print(e)
        except Exception as e:
            print("An unknown error occured. %s" %e)
        finally:
            # release receive allocated memory of receive buffer
            del receiveBuffer

            #close file
            file.close()

            # Close device.
            #-------------------------------------------------------------------------------------
            del device
            print("Disconnected from Unicorn")

    except UnicornPy.DeviceException as e:
        print(e)
    except Exception as e:
        print("An unknown error occured. %s" %e)

    input("\n\nPress ENTER key to exit")

#execute main
main()

# Cerrar el socket
client_socket.close()