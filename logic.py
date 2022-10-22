import numpy as np 
import matplotlib.pyplot as plt
import scipy 
from scipy import signal
import streamlit as st
import pandas as pd

class logic:
    time = np.linspace(0,1,200)
    signals_list = []
    def add_Sine(frequency,magnitude):
        result = magnitude*np.sin(2*np.pi*logic.time*frequency)
        logic.signals_List.append(result)

    def remove_Signal(index,signal_list):
        del signal_list[index]
        del st.session_state.sinW[index]
        del st.session_state.amp[index]
        del st.session_state.freq[index]

    def sampling(sample_Frequency,original_Signal):
        T = 1/sample_Frequency
        points = np.arange(0,sample_Frequency)
        peroid_of_peaks =  scipy.signal.find_peaks(original_Signal)
        peroid_of_shift = logic.time[peroid_of_peaks[0]]
        t_Points = points*T
        t_Points = t_Points + peroid_of_shift[0]
        y_Points = np.zeros(sample_Frequency)
        for frequency in range(len(st.session_state.freq)):
            y_Points += st.session_state.amp[frequency]*np.sin(2*np.pi*st.session_state.freq[frequency]*t_Points)
        y_Points = y_Points.reshape(sample_Frequency,1)
        return t_Points,y_Points,T
    def sampling_uploaded(sample_Frequency,original_Signal,time):
        T = 1/sample_Frequency
        points = np.arange(0,sample_Frequency)
        peroid_of_peaks =  scipy.signal.find_peaks(original_Signal)
        peroid_of_shift = time[peroid_of_peaks[0]]
        t_Points = points*T
        t_Points = t_Points + peroid_of_shift[peroid_of_peaks[0][0]]
        y_Points = np.zeros(sample_Frequency)
        for frequency in range(sample_Frequency):
            difference_array = np.absolute(time-t_Points[frequency])
            Min_index = difference_array.argmin()
            y_Points[frequency] = original_Signal[Min_index]
        y_Points = y_Points.reshape(sample_Frequency,1)
        return t_Points,y_Points,T
    def sinc_Interpolation_uploaded(sample_Frequency,original_Signal,time):
        t_Points,y_Points,T = logic.sampling_uploaded(sample_Frequency,original_Signal,time)
        [Ts,timee] = np.meshgrid(t_Points,logic.time,indexing='ij')
        y = np.sinc((timee-Ts)/T)*y_Points
        y_new = 0
        for i in range(sample_Frequency):
            y_new += y[i,:]
        return y_new
    def sinc_Interpolation(sample_Frequency,original_Signal):
        t_Points,y_Points,T = logic.sampling(sample_Frequency,original_Signal)
        [Ts,timee] = np.meshgrid(t_Points,logic.time,indexing='ij')
        y = np.sinc((timee-Ts)/T)*y_Points
        y_new = 0
        for i in range(sample_Frequency):
            y_new += y[i,:]
        return y_new

    def add_signals(amplitude, frequency):
        st.session_state.amp.append(amplitude)
        st.session_state.freq.append(frequency)
        st.session_state.sinW.append(amplitude*np.sin(2 * np.pi * frequency * logic.time ))

    def sum_signals():
        sum = np.zeros((200))
        for i in range (0,len(st.session_state.amp)):
            sum = sum + st.session_state.amp[i]*np.sin(2*np.pi * st.session_state.freq[i]*logic.time)
        return sum

    def get_maxF():
        if len(st.session_state.freq) ==0:
            maxF =1
        else:    
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

    def save_File():
        data = pd.DataFrame({'time':logic.time,'magnitude':st.session_state.sum,'maxFreq':logic.get_maxF()})
        return data.to_csv().encode('utf-8')

    def open_File(file):
        data = pd.read_csv(file)
        time = data['time']
        sum = data['magnitude']
        max_freq_upload = data['maxFreq'][2]
        return time,sum,max_freq_upload 