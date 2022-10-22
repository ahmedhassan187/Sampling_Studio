from tkinter import Y, Label
import streamlit as st
import pandas as pd
import numpy as np
import sys
from logic import logic
# from streamlit_option_menu import option_menu
from scipy.misc import electrocardiogram
import matplotlib.pyplot as plt
import time
from collections import namedtuple, defaultdict
import mpld3
import streamlit.components.v1 as components

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


st.title(" Welcome to Sampling Studio")


@st.cache(allow_output_mutation=True)
def get_data():
    return []


fig = plt.figure()

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
    st.write(Signals)

    Deleted_Signal = st.number_input(
        "Enter the row of the Signal", step=1)
    delete_button = st.button('Delete A signal')
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

    st.write("")

    if st.button(" Upload a Signal"):
        file = st.file_uploader("Upload Your Signal")
        Data = pd.read_csv(file)

    if st.checkbox("Add Noise"):
        snr = st.slider("SNR", 0, 100, step=1)
        noised_signal = logic.add_noise(st.session_state.sum, snr)

    st.button("Save")

sample_rate = st.slider("Sample Rate", 1, 5, step=1)
# print(sample_rate)
maxF = logic.get_maxF()
# y = logic.sinc_Interpolation(sample_rate,maxF)
# for i in range(0, len(st.session_state.sinW)):
if type(st.session_state.sum) is np.ndarray:
    y_new = logic.sinc_Interpolation(sample_rate*logic.get_maxF())
    plt.subplot(211)
    plt.plot(logic.time, y_new)
    plt.subplot(212)
    plt.plot(logic.time, st.session_state.sum)
st.pyplot()
