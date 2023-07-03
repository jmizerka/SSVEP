# SSVEP-BASED BCI

## 1. The goal of the project 
My main goal was to create a brain-computer interface based on steady-state visual evoked potentials and the EEG method. It was implemented in Python. At this point, the interface is **not** yet finished. For now, I managed to write the whole experiment offline. It can be used to collect data to train a classifier, a neural network, for example. 

## 2. Stimulation interface
<img src="stimuli.png" alt="Description" width="300" height="200" title="A view of the interface with stimuli">

The photo above shows a view of the interface with the stimuli. The Psychopy library is responsible for the GUI and stimulus flashing controls. Signals controlling the blinking were generated using the scipy library. The stimuli were encoded using the so-called joint frequency, phase and waveform modulation method, which means that each stimulus flashes according to the values of the generated periodic functions, and individual stimuli are controlled by signals with different shapes, phase shifts, and frequencies. Such a method is intended to facilitate the recognition of stimuli when there are a lot of them and the frequency differences between them are small. The disadvantage of such a solution is the need for more complex classification methods -- for example, standard methods based on the fast Fourier transform will not work. 









## 4. Bibliography

OpenBCI Cyton: https://docs.openbci.com/Cyton/CytonLanding
