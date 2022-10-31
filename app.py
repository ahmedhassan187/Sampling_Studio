from platform import mac_ver
import streamlit as st
import pandas as pd
import numpy as np
import sys
from traitlets import default
from logic import logic
import matplotlib.pyplot as plt

st.set_option('deprecation.showPyplotGlobalUse', False)
st.set_page_config(
    page_title='Sampling Studio',
    page_icon="chart_with_upwards_trend",

)


reduce_header_height_style = """
    <style>
        div.block-container {padding-top:0rem;}
    </style>
"""
st.markdown(reduce_header_height_style, unsafe_allow_html=True)


st.write(
    '<style>div.row-widget.stRadio > div{flex-direction:row;justify-content: left;} </style>', unsafe_allow_html=True)



if 'label_generated' not in st.session_state:
    st.session_state.label_generated = 0


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
    st.session_state.sum = logic.sum_signals()
if 'constructed' not in st.session_state:
    st.session_state.constructed = 0
if 'deleted_flag ' not in st.session_state:
    st.session_state.deleted_flag = True
if 'sample_rate' not in st.session_state:
    st.session_state.sample_rate = 1


@st.cache(allow_output_mutation=True)
def get_data():
    return []


fig = plt.figure()
flag_noised = False

col4, col5 = st.columns((2, 1))

with col4:
    Signal_Selected = st.selectbox(
        "Select the Signal", ("Sampled", "Reconstructed", "Both"))

with col5:
    sample_option = st.radio("Sample Rate option", [
                             "Sample Rate", "Max Frequency Scale"])
    if logic.default_signal_flag:
        st.session_state.sum = 1 *np.sin(2*np.pi*2*logic.time)
        st.session_state.freq.append(2)
        st.session_state.amp.append(1)
        st.session_state.sinW.append(
            1*np.sin(2*np.pi*2*logic.time))
        get_data().append(
            {"Label": 'Default Signal', "Frequency(Hz)": 2, "Amplitude(V)": 1})
        logic.default_signal_flag = False
with st.sidebar:

    st.title('Sampling Studio')
    with st.form(key="my_form"):

        Label = st.text_input("label")

        col1, col2 = st.columns((1, 1))

        with col1:
            freq = st.number_input("Frequency", step=1, min_value=1)

        with col2:
            Amplitude = st.number_input("Amplitude", step=1, min_value=1)
        submitted = st.form_submit_button("Add")
        if submitted:
            logic.add_signals(Amplitude, freq)
            st.session_state.sum = logic.sum_signals()
            if Label == "" or Label == " ":
                Label = 'Signal' + str(st.session_state.label_generated)
                st.session_state.label_generated += 1
            get_data().append(
                {"Label": Label, "Frequency(Hz)": freq, "Amplitude(V)": Amplitude})
    Signals = pd.DataFrame(get_data())
    file = st.file_uploader("Upload", type=["csv"])
    if st.checkbox("Add Noise"):
        snr = st.slider("SNR", 1, 100, step=1)
        if file is None:
            if len(Signals) == 0:
                st.write("Please add a signal first.")
            else:
                noised_signal = logic.add_noise(st.session_state.sum, snr)
                flag_noised = True
        else:
            flag_noised = True
        
    # if len(Signals) == 0:
    #     delete_max = 0
    # else:
    #     delete_max = len(Signals)-1
    
    col6, col7 = st.columns((1, 1))

    with col6:
        
        Deleted_Signal_name = st.selectbox(
            "Signals",Signals)
    with col7:
        st.write("")
        st.write("")

        delete_button = st.button('Delete')
    if delete_button:
        for i in range(0,len(Signals)):
            if Deleted_Signal_name == Signals['Label'][i] :
                Deleted_Signal = i
        if (int(Deleted_Signal) == 0) and (len(Signals) > 1):
            logic.default_signal_flag = False
        if Deleted_Signal > len(Signals)-1 or Deleted_Signal < 0:
            st.text("Invalid number")
        else:
            logic.remove_Signal(int(Deleted_Signal), get_data())
            if Signals['Label'][Deleted_Signal] == "Uploaded":
                logic.uploaded_flag = True
            Signals.drop([Deleted_Signal], axis=0, inplace=True)
            if (len(Signals) == 0):
                st.session_state.sum = 0
                logic.default_signal_flag = True
            else:
                st.session_state.sum = logic.sum_signals()
        # logic.sample_rate = st.session_state.sample_rate
    st.write("")
    csv = logic.save_File()
    save_button_clicked = st.download_button(
        label="Download",
        data=csv,
        file_name=('Signal.csv'),
        mime='text/csv',
    )

    st.write("")

maxF = logic.get_maxF()
if sample_option == "Sample Rate":
    st.session_state.sample_rate = st.slider("Sample Rate", 1, 60, step=1)
if sample_option == "Max Frequency Scale":
    fmax_scale = st.slider("Max Frequency Scale", 1, 20, step=1)
    st.session_state.sample_rate = fmax_scale * maxF
# with col2:
#     Frecquency_default = st.slider("Frequency(Hz)", 1, 30, step=1)
#     if st.session_state.freq == []:
#         pass
#     else:
#         if (logic.default_signal_flag):
#             st.session_state.freq[0] = Frecquency_default

# with col3:
#     Amplitude_default = st.slider("Amplitude(V)", 1, 15, step=1)
#     if st.session_state.amp == []:
#         pass
#     else:
#         if (logic.default_signal_flag):
#             st.session_state.amp[0] = Amplitude_default
#             st.session_state.sum = logic.sum_signals()

if file is None:
    if type(st.session_state.sum) is np.ndarray:
        if flag_noised:
            st.session_state.constructed = logic.sinc_Interpolation(
                st.session_state.sample_rate, noised_signal)
            sampled_time, sampled_signal, peroidic_time = logic.sampling(
                st.session_state.sample_rate, noised_signal)
            plt.subplot(211)
            fig_1, = plt.plot(logic.time, noised_signal,)
            fig_2, = plt.plot(sampled_time, sampled_signal,
                              'o',)
            plt.xlabel("Time(sec)")
            plt.ylabel("Amplitude(V)")
            plt.tight_layout()
            fig_3, = plt.plot(logic.time, st.session_state.constructed,
                              label="Reconstructed Signals")
            if Signal_Selected == "Sampled":
                fig_3.remove()
            elif Signal_Selected == "Reconstructed":
                fig_1.remove()
            plt.xlabel("Time(sec)")
            plt.ylabel("Amplitude(V)")
        else:
            st.session_state.constructed = logic.sinc_Interpolation(
                st.session_state.sample_rate, st.session_state.sum)
            sampled_time, sampled_signal, peroidic_time = logic.sampling(
                st.session_state.sample_rate, st.session_state.sum)
            plt.subplot(211)
            fig_1, = plt.plot(logic.time, st.session_state.sum)
            fig_2, = plt.plot(sampled_time, sampled_signal,
                              'o')
            plt.xlabel("Time(sec)")
            plt.ylabel("Amplitude(V)")
            plt.tight_layout()
            fig_3, = plt.plot(logic.time, st.session_state.constructed,
                              label="Reconstructed Signal")
            if Signal_Selected == "Sampled":
                fig_3.remove()
            elif Signal_Selected == "Reconstructed":
                fig_1.remove()
            plt.xlabel("Time(sec)")
            plt.ylabel("Amplitude")
    # else:
        # st.session_state.sum = 1 * \
        #     np.sin(2*np.pi*2*logic.time)
        # st.session_state.freq.append(2)
        # st.session_state.amp.append(1)
        # st.session_state.sinW.append(
        #     1*np.sin(2*np.pi*2*logic.time))
        # get_data().append(
        #     {"Label": 'Default Signal', "Frequency(Hz)": 2, "Amplitude(V)": 1})
        # st.session_state.constructed = logic.sinc_Interpolation(
        #     sample_rate, st.session_state.sum)
        # sampled_time, sampled_signal, peroidic_time = logic.sampling(
        #     sample_rate, st.session_state.sum)
        # plt.subplot(211)
        # fig_1, = plt.plot(logic.time, 1 *
        #                   np.sin(2*np.pi * 2 * logic.time))
        # fig_2, = plt.plot(sampled_time, sampled_signal, 'o')
        # plt.xlabel("Time(sec)")
        # plt.ylabel("Amplitude(V)")
        # plt.tight_layout()
        # fig_3, = plt.plot(logic.time, st.session_state.constructed,
        #                   label="Reconstructed Signal")
        # if Signal_Selected == "Sampled":
        #     fig_3.remove()
        # elif Signal_Selected == "Reconstructed":
        #     fig_1.remove()
        # plt.xlabel("Time(sec)")
        # plt.ylabel("Amplitude(V)")
        # plt.legend(loc='upper right')
        # st.experimental_rerun()
else:
    if flag_noised == False:
        time_of_uploaded, signal_uploaded, max_frequency = logic.open_File(
            file)
        maxF = max_frequency
        if len(time_of_uploaded) == 1000:
            if logic.uploaded_flag:
                logic.add_signals(1, max_frequency)
                get_data().append(
                    {"Label": "Uploaded", "Frequency(Hz)": max_frequency, "Amplitude(V)": 1})
                logic.uploaded_flag = False
                st.session_state.sum = logic.sum_signals()
                # st.experimental_rerun()
            st.session_state.constructed = logic.sinc_Interpolation_uploaded(
                st.session_state.sample_rate, (st.session_state.sum), time_of_uploaded)
            sampled_time, sampled_signal, peroidic_time = logic.sampling_uploaded(
                st.session_state.sample_rate, (st.session_state.sum), time_of_uploaded)
            plt.subplot(211)
            fig_1, = plt.plot(time_of_uploaded, (st.session_state.sum))
            fig_2, = plt.plot(sampled_time, sampled_signal, 'o')
            plt.xlabel("Time(sec)")
            plt.ylabel("Amplitude(V)")
            fig_3, = plt.plot(time_of_uploaded, st.session_state.constructed,
                              label="Reconstructed Signal")
            if Signal_Selected == "Sampled":
                fig_3.remove()
            elif Signal_Selected == "Reconstructed":
                fig_1.remove()
            plt.xlabel("Time(sec)")
            plt.ylabel("Amplitude(V)")
        else:
            st.warning("File size not supported")
    else:
        time_of_uploaded, signal_uploaded, max_frequency = logic.open_File(
            file)
        noised_signal = logic.add_noise(signal_uploaded, snr)
        st.session_state.constructed = logic.sinc_Interpolation_uploaded(
            st.session_state.sample_rate, noised_signal, time_of_uploaded)
        sampled_time, sampled_signal, peroidic_time = logic.sampling_uploaded(
            st.session_state.sample_rate, noised_signal, time_of_uploaded)
        if logic.uploaded_flag:
            logic.add_signals(1, max_frequency)
            get_data().append(
                {"Label": "Uploaded", "Frequency(Hz)": max_frequency, "Amplitude(V)": 1})
            logic.uploaded_flag = False
            st.experimental_rerun()
        plt.subplot(211)
        fig_1, = plt.plot(time_of_uploaded, noised_signal,)
        fig_2, = plt.plot(sampled_time, sampled_signal, 'o')
        plt.xlabel("Time(sec)")
        plt.ylabel("Amplitude(V)")
        plt.tight_layout()
        fig_3, = plt.plot(time_of_uploaded, st.session_state.constructed,
                          label="Reconstructed Signal")
        if Signal_Selected == "Sampled":
            fig_3.remove()
        elif Signal_Selected == "Reconstructed":
            fig_1.remove()
        else:
            fig_2.remove()
        plt.xlabel("Time(sec)")
        plt.ylabel("Amplitude(V)")
st.pyplot()



 