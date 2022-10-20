import numpy as np 
import matplotlib.pyplot as plt

class logic:
    def add_Sine(frequency,magnitude):
        time = np.linspace(0,1,100)
        result = magnitude*np.sin(2*np.pi*time*frequency)
        logic.signals_List.append(result)
    def remove_Signal(index,signal_list):
        signal_list.remove(index)