import streamlit as st
import pandas as pd
import numpy as np
import sys
from traitlets import default
from logic import logic
import matplotlib.pyplot as plt
import time
# from collections import namedtuple, defaultdict
import mpld3
# import streamlit.components.v1 as components

st.set_option('deprecation.showPyplotGlobalUse', False)
st.set_page_config(
    page_title='Sampling Studio',
    page_icon="chart_with_upwards_trend",
    layout='wide'
)

hide_st_style = """
            <style>
            # MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)


def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


local_css("style.css")

if 'sinW' not in st.session_state:
    st.session_state.sinW = []

if 'amp' not in st.session_state:
    st.session_state.amp = []

if 'freq' not in st.session_state:
    st.session_state.freq = []   

if 'sum' not in st.session_state:
    st.session_state.sum = 0

st.title(" Welcome to Sampling Studio")

@st.cache(allow_output_mutation=True)
def get_data():
    return []

fig = plt.figure()
flag_noised = False
with st.sidebar:

    st.title(':gear: Sampling Studio')
    generate_expander = st.sidebar.expander(
        "Generate/Add Signal ", expanded=False)
    Label = generate_expander.text_input("Label")
    freq = generate_expander.number_input(
        "Frecquency in Hz", step=1, min_value=1)
    Amplitude = generate_expander.number_input(
        "Amplitude", step=1, min_value=1)
    Add_button_clicked = generate_expander.button("Save", key=1)

    if Add_button_clicked:
        logic.add_signals(Amplitude, freq)
        st.session_state.sum = logic.sum_signals()

        get_data().append(
            {"Label": Label, "Frecquency in Hz": freq, "Amplitude": Amplitude})
    Signals = pd.DataFrame(get_data())
 
    st.write("")

    generate_expander_Delete = st.sidebar.expander(
        "Delete a Signal ", expanded=False)

    Deleted_Signal = generate_expander_Delete.number_input(
        "Enter the row of the Signal", step=1)
    delete_button = generate_expander_Delete.button('Delete A signal')
    if delete_button:
        if Deleted_Signal > len(Signals)-1 or Deleted_Signal < 0:
            st.text("Invalid number")
        else:
            logic.remove_Signal(int(Deleted_Signal), get_data())
            Signals.drop([Deleted_Signal], axis=0, inplace=True)

            if (len(Signals) == 0):
                st.session_state.sum = 0
            else:
                st.session_state.sum = logic.sum_signals()
    if Signals.empty:
        st.write("")
    else:
        st.write(Signals)

    generate_expander_Upload = st.sidebar.expander(
        "Upload Signal", expanded=False)
    file = generate_expander_Upload.file_uploader("")
    if generate_expander_Upload.button(" Upload a Signal"):
        Data = pd.read_csv(file)

    if st.checkbox("Add Noise"):
        if len(Signals) ==0:
            st.write("Please add a signal first.")
        else:
            snr = st.slider("SNR", 0, 100, step=1)
            noised_signal = logic.add_noise(st.session_state.sum, snr)
            flag_noised = True
        # st.session_state.sum = noised_signal
    generate_expander_save = st.sidebar.expander(
        "Save Signal", expanded=False)
    Folder_Name = generate_expander_save.text_input("Folder Name")
    
    
    data = pd.DataFrame({'time':logic.time,'magnitude':st.session_state.sum,'maxFreq':logic.get_maxF()})

    csv = logic.save_File()
    save_button_clicked = generate_expander_save.download_button(
            label="Save",
            data=csv,
            file_name=('{}.csv'.format(Folder_Name)),
            mime='text/csv',
        )


sample_rate = st.slider("Sample Rate", 1, 30, step=1)
# print(sample_rate)
maxF = logic.get_maxF()
# y = logic.sinc_Interpolation(sample_rate,maxF)
# for i in range(0, len(st.session_state.sinW)):
if file is None:
    if type(st.session_state.sum) is  np.ndarray :
      if flag_noised:
        consturcted = logic.sinc_Interpolation(sample_rate,noised_signal)
        sampled_time,sampled_signal,peroidic_time = logic.sampling(sample_rate,noised_signal)
        plt.subplot(211)
        plt.plot(logic.time,noised_signal) 
        plt.plot(sampled_time,sampled_signal,'o')  
        plt.subplot(212)
        plt.plot(logic.time,consturcted)
      else:
        consturcted = logic.sinc_Interpolation(sample_rate,st.session_state.sum)
        sampled_time,sampled_signal,peroidic_time = logic.sampling(sample_rate,st.session_state.sum)
        plt.subplot(211)
        plt.plot(logic.time,st.session_state.sum)
        plt.plot(sampled_time,sampled_signal,'o')
        plt.subplot(212)
        plt.plot(logic.time,consturcted)
else:
        time_of_uploaded,signal_uploaded,max_frequency = logic.open_File(file)
        consturcted = logic.sinc_Interpolation_uploaded(sample_rate,signal_uploaded,time_of_uploaded)
        sampled_time,sampled_signal,peroidic_time = logic.sampling_uploaded(sample_rate,signal_uploaded,time_of_uploaded)
        plt.subplot(211)
        plt.plot(time_of_uploaded,signal_uploaded)
        plt.plot(sampled_time,sampled_signal,'o')
        plt.subplot(212)
        plt.plot(time_of_uploaded,consturcted)
st.pyplot()
