from signal import signal
from time import time
import numpy as np 
import matplotlib.pyplot as plt

class logic:
    signals_List = []
    def add_Sine(frequency,magnitude):
        time = np.linspace(0,1,100)
        result = magnitude*np.sin(2*np.pi*time*frequency)
        logic.signals_List.append(result)
    def remove_Signal(index):
        logic.signals_List.remove(index)
    