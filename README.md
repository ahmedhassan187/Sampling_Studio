
# Signal Sampling Studio

Designing a signal recovery web-application that depicts the Nyquist rate, using streamlit, an open source framework.


## Features
- generating sinusoidal signals at the user-specified frequency and amplitude.
- Reading of csv signal files and the sampled points are marked on the signal.
- Adjusting the sample rate through a slider that ranges from 0 Hz to  Hz.
- Reconstructing the signal from the sampled points.
- The sum of the generated sinusoidals is shown on a single graph.
- A button to delete the user-choosen sinusoidal.
- A slider for adding noise to the signal by a user-specified SNR value.
- Saving the generated sinusoidal to the user's computer using save button.

## Deployment

To deploy this project run

```bash
  pip install -r requirements.txt 
```

```bash
  streamlit run Demo1.py
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

Insert gif or link to demo

### Team Members

Name
--- |
Sara Amgad 
Sohaila Mahmoud
Habiba Fathallah
Ahmed Hassan 
