from psychopy import visual, event, core
from scipy import signal
import numpy as np

class experiment2_psypy():

    def __init__(self, time_stim, time_break, n_loops):
        self.window = visual.Window([1920, 1080], monitor="testMonitor", units='cm', fullscr=True, color=[-1, -1, -1],
                                    screen=0,waitBlanking=False)
        self.n_loops = n_loops
        self.time_stim = time_stim
        self.time_break = time_break
        self.times = np.concatenate(
            [np.array([self.time_stim * 60]), np.array([self.time_break * 60])] * self.n_loops)
        self.times = np.cumsum(self.times)  # define start of stimulation and breaks in frames
        self.define_signals()
        self.define_stimuli()
        self.break_points = [self.times[int(len(self.times)/3-2)],self.times[int(len(self.times)/3*2-2)]]
    def define_signals(self):
        t = np.linspace(0, 60-1, 60)
        constant = 2 * np.pi * 15 * (t / 60)
        phases = [0.4, 0.8, 1.2]
        # define array of signals: (4 types x 3 phases) x t
        self.func_list = np.vstack([np.concatenate([(0.5 * (1 + np.sin(constant + np.pi * phase)),
                                                     0.5 * (1 - signal.sawtooth(constant - np.pi * phase)),
                                                     0.5 * (1 + signal.square(constant + np.pi * phase)),
                                                     0.5 * (1 - signal.sawtooth(constant - np.pi * phase, width=0.5)))])
                                    for phase in phases])
    def define_stimuli(self):
        self.squares_list = []

        # grid of stimuli:
        # 5 6 7 8
        # 1 2 3 4
        # 9 10 11 12

        for x, y in np.array(
                [(-24, -2), (-8, -2), (8, -2), (24, -2), (-24, 8), (-8, 8), (8, 8), (24, 8), (-24, -12), (-8, -12),
                 (8, -12), (24, -12)]):
            stimulus = visual.Rect(win=self.window, units="cm", width=4, height=4, fillColor=[0, 1, 0],
                                   pos=(x, y), opacity=100)
            stimulus.autoDraw = True
            self.squares_list.append(stimulus)
        self.seq = np.array(np.arange(0, len(self.squares_list), 1))
        np.random.shuffle(self.seq) #order of stimuli in the first run
        self.seq_nr = 0
        print(self.seq)

    def run(self, last_state, stim_off, end):
        core.wait(3)
        self.squares_list[self.seq[self.seq_nr]].color = (255, 215, 0)
        self.window.flip()
        core.wait(1)
        self.squares_list[self.seq[self.seq_nr]].color = (0, 255, 0)
        current_frame = 0
        stimuli_on = True
        last_state.value = -1
        state = self.seq[self.seq_nr]
        i = 0

        while i != self.n_loops*2: # until frames reach the last value in time array (num_of_stim + num_of_breaks)
            if stimuli_on: # flickering happens here
                index = np.mod(current_frame, self.func_list[0].shape[0])
                for j in range(len(self.squares_list)):
                    self.squares_list[j].opacity = self.func_list[j][index]
            self.window.flip()
            current_frame += 1
            if current_frame == self.times[i]:
                i += 1
                if i % 2 == 0:
                    stimuli_on = True
                    self.squares_list[self.seq[self.seq_nr]].color = (0, 255, 0)
                    last_state.value = state
                    state = self.seq[self.seq_nr]
                    stim_off.clear()
                else:
                    stim_off.set()
                    stimuli_on = False
                    last_state.value = self.seq[self.seq_nr]
                    state = -1
                    self.seq_nr += 1
                    if self.seq_nr > 11: #if it is the last element, shuffle again for the next round
                        np.random.shuffle(self.seq)
                        self.seq_nr = 0
                    if current_frame in self.break_points:
                        stim_off.clear()
                        event.waitKeys()
                    self.squares_list[self.seq[self.seq_nr]].color = (255, 215, 0)



            for key in event.getKeys():
                if key in ['escape', 'q']:
                    core.quit()
        stim_off.set()
        end.set()
        self.window.flip()
        self.window.close()
