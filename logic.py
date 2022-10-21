import numpy as np 
import matplotlib.pyplot as plt

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
        t_Points = points*T
        y_Points = np.sin(2*np.pi*signal_Frequency*t_Points)
        return t_Points,y_Points,T
    def sinc_Interpolation(sample_Frequency,signal_Frequency):
        t_Points,y_Points,T = logic.sampling(sample_Frequency,signal_Frequency)
        [Ts,timee] = np.meshgrid(t_Points,logic.time,indexing='ij')
        y = np.sinc((Ts-timee)/T)*np.sin(2*np.pi*signal_Frequency*logic.time)
        y_new = 0
        for i in range(sample_Frequency):
            y_new += y[i,:]
        return y_new

