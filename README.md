
# Signal Sampling Studio

Designing a signal recovery web-application that depicts the Nyquist rate, using streamlit, an open source framework.


## Features
- generating sinusoidal signals at the user-specified frequency and amplitude.
- Reading of csv signal files and the sampled points are marked on the signal.
- Adjusting the sample frequency with sample rate slider or slider of maximum frequency scale.
- Reconstructing the signal from the sampled points.
- The sum of the generated sinusoidals, and the reconstructed ones are shown on a single graph, where user can choose which to be shown.
- A button to delete the user-choosen sinusoidal.
- A slider for adding noise to the signal by a user-specified SNR value.
- Saving the reconstructed signal to the user's computer using download button.

## Deployment

To deploy this project run

```bash
  pip install -r requirements.txt 
```

```bash
  streamlit run app.py
```

## Screenshots

- Default Signal

![1](https://user-images.githubusercontent.com/81927516/198858840-5eca850f-1656-4987-9c28-afc4005ad56c.png)

- Sampling an added signal without noise

![2](https://user-images.githubusercontent.com/81927516/198858843-be6dbc31-e45c-45f1-9872-62a1ef6edda2.png)

![3](https://user-images.githubusercontent.com/81927516/198858846-6f32ec74-6cb7-4075-9c47-5f79d1d884fd.png)

- Sampling an added signal with noise

![4](https://user-images.githubusercontent.com/81927516/198858848-d5fc6a93-cda0-442e-8d7f-bd0d84d0c8f7.png)



## Demo

![SamplingStudio](https://user-images.githubusercontent.com/81927516/199120894-87641f6c-56cf-4c1b-be19-eeef1151b3ea.gif)


## About Us

- This project was made for a task in the fifth semester of SBME, for digital signal processing course, and was submitted to the course's doctor in 10/31/2022

### Team Number : 21

### Team Members

Name| Section | Bench Number |
--- | --- | --- |
Habiba Fathallah | 1 | 27
Sohaila Mahmoud | 1 | 45
Ahmed Hassan | 1 | 4
Sara Amgad | 1 | 38
