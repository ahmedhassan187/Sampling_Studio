import numpy as np 
import matplotlib.pyplot as plt
import scipy 
from scipy import signal
import streamlit as st

if 'i' not in st.session_state:
    st.session_state.i = 0

if 'y' not in st.session_state:
    st.session_state.y = []

if 'amp' not in st.session_state:
    st.session_state.amp = []

if 'freq' not in st.session_state:
    st.session_state.freq = []   

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

    def add_signals(amplitude, frequency):
        st.session_state.amp.append(amplitude)
        st.session_state.freq.append(frequency)
        st.session_state.y.append(amplitude*np.sin(2 * np.pi * frequency * time ))
        # st.session_state.i +=1

    def sum_signals():
        l = 0
        # for i in range (0,len(st.session_state.y)):
        #     # print(i)
        #     l = l + st.session_state.y[i]
        for i in range (0,len(st.session_state.amp)):
            l = l + st.session_state.amp[i]*np.sin(2*np.pi * st.session_state.freq[i]*time)
        return l

    def delete_Signal(i):
        st.session_state.y[i] = st.session_state.y[i+1]
        st.session_state.y[len(st.session_state.y)-1] = 0
        # st.session_state.y.(len(st.session_state.y)) -=1 
        # st.session_state.Signal[m] = st.session_state.Signal[m+1]    
        # st.session_state.Signal[len(st.session_state.Signal)-1] = 0
        # st.session_state.Signal[len(st.session_state.Signal)] -=1 

    def get_maxF():
        maxF = max(st.session_state.freq)
        return maxF    

    def add_noise(target_Sig,snr_db):
        signalP = pow(target_Sig,2)
        signalP_avg = np.mean(signalP)
        signal_avg_db = 10 * np.log10(signalP_avg)
        noise_avg_db = signal_avg_db - snr_db
        noiseP_avg = 10 ** (noise_avg_db / 10)
        mean_noise = 0
        noise = np.random.normal(mean_noise, np.sqrt(noiseP_avg), len(signalP))
        noised_signal = target_Sig + noise

        return noised_signal    