# SSVEP-BASED BCI

## 1. The goal of the project 
My main goal was to create a brain-computer interface based on steady-state visual evoked potentials and the EEG method. It was implemented in Python. At this point, the interface is **not** yet finished. For now, I managed to write the whole experiment offline. It can be used to collect data to train a classifier, a neural network, for example. 

## 2. Stimulation interface
<img src="stimuli.png" alt="Description" width="300" height="200" title="A view of the interface with stimuli">

The photo above shows a view of the interface with the stimuli. The Psychopy library is responsible for the GUI and stimulus flashing controls. Signals controlling the blinking were generated using the scipy library. The stimuli were encoded using the so-called joint frequency, phase and waveform modulation method, which means that each stimulus flashes according to the values of the generated periodic functions, and individual stimuli are controlled by signals with different shapes, phase shifts, and frequencies. Such a method is intended to facilitate the recognition of stimuli when there are a lot of them and the frequency differences between them are small. The disadvantage of such a solution is the need for more complex classification methods - for example, standard methods based on the fast Fourier transform will not work. 

## 3. EEG data acquisition
<img src="Cyton.jpg" alt="Description" width="200" height="200" title="3D-printed EEG Ultracortex Mark III cap">

To collect data and test the interface, I used an 8-channel Cyton amplifier from OpenBCI [1] with a sampling rate of 250 Hz. EEG cap was 3D-printed according to the project by OpenBCI [2] with small modifications. The cap uses gel-free electrodes which significantly reduces testing preparation time.

<img src="cap.png" alt="Description" width="200" height="300" title="3D-printed EEG Ultracortex Mark III cap">


## 4. Project structure
![Drzewo projektu](drzewo.png)

The data_acquisition package contains a module responsible for communicating with the OpenBCI device using the brainflow library [3] and filtering and saving data.

The ssvep_stimuli package contains speller.py module which implements stimulation matrix and is responsible for flickering stimuli and precise timing.

In the main.py file multiprocessing is implemented to ensure proper synchronization between the EEG device and the program responsible for stimulation. 

## 5. Resources

[1] OpenBCI Cyton: https://docs.openbci.com/Cyton/

[2] Ultracortex Mark II Nova Revised: https://github.com/OpenBCI/Ultracortex/tree/master/Mark_III_Nova_REVISED

[3] Brainflow: https://brainflow.org/
