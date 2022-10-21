import numpy as np 
import matplotlib.pyplot as plt
import scipy 
from scipy import signal
class logic:
    time = np.linspace(0,1,200)
    def add_Sine(frequency,magnitude):
        time = np.linspace(0,1,100)
        result = magnitude*np.sin(2*np.pi*time*frequency)
        logic.signals_List.append(result)
    def remove_Signal(index,signal_list):
        del signal_list[index]
    def sampling(sample_Frequency,signal_Frequency):
        T = 1/sample_Frequency
        points = np.arange(0,sample_Frequency)
        original_Signal = np.sin(2*np.pi*signal_Frequency*logic.time)
        peroid_of_peaks =  scipy.signal.find_peaks(original_Signal)
        peroid_of_shift = logic.time[peroid_of_peaks[0]]
        t_Points = points*T
        t_Points = t_Points + peroid_of_shift[0]
        print(t_Points)
        y_Points = np.sin(2*np.pi*signal_Frequency*t_Points)
        y_Points = y_Points.reshape(sample_Frequency,1)
        return t_Points,y_Points,T
    def sinc_Interpolation(sample_Frequency,signal_Frequency):
        t_Points,y_Points,T = logic.sampling(sample_Frequency,signal_Frequency)
        [Ts,timee] = np.meshgrid(t_Points,logic.time,indexing='ij')
        y = np.sinc((timee-Ts)/T)*y_Points
        y_new = 0
        for i in range(sample_Frequency):
            y_new += y[i,:]
        return y_new

