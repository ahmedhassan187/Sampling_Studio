import numpy as np 
import matplotlib.pyplot as plt
import scipy 
from scipy import signal
import streamlit as st
import pandas as pd
class logic:
    time = np.linspace(0,1,1000)
    default_signal_flag = True
    uploaded_flag = True
    def remove_Signal(index,signal_list):
        """ index : take index of item you wnt to delete
            signal_list : list of signals that you want to delete"""
        if(index > len(signal_list)-1):
            pass
        else:
            del signal_list[index]
            del st.session_state.sinW[index]
            del st.session_state.amp[index]
            del st.session_state.freq[index]
    def sampling(sample_Frequency,original_Signal):
        """ sample_Frequency: frequency at which we will sample the original signal
            original_Signal: magnitude of the original signal
            this function takes two parameters and returns points on the x and y axes at which we will take our sample
            and the third parameter it return is the periodic time
        """
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
        """sample_Frequency: frequency at which we will sample the original signal
            original_Signal: magnitude of the original signal
            time : time of signal which if saved in the csv file
            this function takes three parameters of uploaded file and returns points on the x and y axes at which we will take our sample
            and the third parameter it return is the periodic time
        """
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
        """sample_Frequency: frequency at which we will sample the original signal
            original_Signal: magnitude of the original signal
            time : time of signal which if saved in the csv file
            this function takes three parameters of uploaded file and returns the signal of the sampled points after sinc interploation  
        """
        t_Points,y_Points,T = logic.sampling_uploaded(sample_Frequency,original_Signal,time)
        [T_sample,time_of_signal] = np.meshgrid(t_Points,logic.time,indexing='ij')
        y = np.sinc((time_of_signal-T_sample)/T)*y_Points
        y_new = 0
        for i in range(sample_Frequency):
            y_new += y[i,:]
        return y_new
        
    def sinc_Interpolation(sample_Frequency,original_Signal):
        """sample_Frequency: frequency at which we will sample the original signal
            original_Signal: magnitude of the original signal
            this function takes three parameters of uploaded file and returns the signal of the sampled points after sinc interploation  
        """
        t_Points,y_Points,T = logic.sampling(sample_Frequency,original_Signal)
        [T_sample,time_of_signal] = np.meshgrid(t_Points,logic.time,indexing='ij')
        y = np.sinc((time_of_signal-T_sample)/T)*y_Points
        y_new = 0
        for i in range(sample_Frequency):
            y_new += y[i,:]
        return y_new

    def add_signals(amplitude, frequency):
        """
        amplitude : it takes coefficient that scale the sin functio
        frequency : it takes the frequency of the sin function
        this function takes 2 parameters and return sin function of 1000 point"""
        st.session_state.amp.append(amplitude)
        st.session_state.freq.append(frequency)
        st.session_state.sinW.append(amplitude*np.sin(2 * np.pi * frequency * logic.time ))

    def sum_signals():
        """
        this function is without any parameters but it is used to iterate on the signal list and return its sum """
        sum = np.zeros((1000))
        for i in range (0,len(st.session_state.amp)):
            sum = sum + st.session_state.amp[i]*np.sin(2*np.pi * st.session_state.freq[i]*logic.time)
        return sum

    def get_maxF():
        """ this function returns the maximum frequency in signal list"""
        if len(st.session_state.freq) ==0:
            maxF =1
        else:    
            maxF = max(st.session_state.freq)
        return maxF    

    def add_noise(target_Sig,snr_db):
        """
        target_Sig: signal that noise will be added to it
        snr_db: signal-to-noise ratio in dB
        this function generates noise with specific power"""
        signal_Power = pow(target_Sig,2)
        signalP_avg = np.mean(signal_Power)
        signal_avg_db = 10 * np.log10(signalP_avg)
        noise_avg_db = signal_avg_db - snr_db
        noiseP_avg = 10 ** (noise_avg_db / 10)
        mean_noise = 0
        noise = np.random.normal(mean_noise, np.sqrt(noiseP_avg), len(signal_Power))
        noised_signal = target_Sig + noise
        return noised_signal

    def save_File():
        """ this function saves csv file with name entered in the website """
        data = pd.DataFrame({'time':logic.time,'magnitude':st.session_state.constructed,'maxFreq':logic.get_maxF()})
        return data.to_csv().encode('utf-8')

    def open_File(file):
        """
        file : file you want to upload on website
        """
        data = pd.read_csv(file)
        time = data['time']
        sum = data['magnitude']
        max_freq_upload = data['maxFreq'][2]
        return time,sum,max_freq_upload 