# ver 1.0

from psychopy import visual, event, core
from scipy import signal
import numpy as np


class experiment2_psypy():
    def __init__(self, time_stim, time_break, n_loops):
        self.window = visual.Window([1920, 1080], monitor="testMonitor", units='cm', fullscr=True, color=[-1, -1, -1],
                                    screen=0, waitBlanking=False)  # ,
        self.n_stim = 1  # POPRAWIĆ TO BO JEŻELI ZWIĘKSZĘ PRZERWĘ MIĘDZY BODŹCAMI TO SIĘ WSZYSTKO ROZJEDZIE
        self.n_loops = n_loops
        self.time_stim = time_stim
        self.time_break = time_break
        w_stim = 6
        self.squares_list = []

        for x, y in np.array(
                [(-20, 8),(20, 8), (-20, -12),(20, -12)]): #10, 12, 14,16 
            stimulus = visual.Rect(win=self.window, units="cm", width=w_stim, height=w_stim, fillColor=[0, 1, 0],
                                   pos=(x, y), opacity=100)
            stimulus.autoDraw = True
            self.squares_list.append(stimulus)
        self.window.flip()

        self.times = np.concatenate(
            [np.array([self.time_stim * 60]), np.array([self.time_break * 60])] * (self.n_loops * self.n_stim))
        self.times = np.cumsum(self.times)
        self.t = np.linspace(0, 299, 300)
        #constant = 2 * np.pi * 15 * (self.t / 60)
        #phases = [0.4, 0.8, 1.2]

        stim10 = 0.5 * (1 - np.sin(2 * np.pi * 10 * (self.t / 60)))
        stim12 = 0.5 * (1 - np.sin(2 * np.pi * 12 * (self.t / 60)))
        stim14 = 0.5 * (1 - np.sin(2 * np.pi * 14 * (self.t / 60)))
        stim16 = 0.5 * (1 - np.sin(2 * np.pi * 16 * (self.t / 60)))
        self.func_list = np.vstack([stim10,stim12,stim14,stim16])
        print(self.func_list.shape)
        core.wait(3)

    def run(self, last_state, stim_off, end):
        current_frame = 0

        order = [i for i in range(self.n_stim)] * self.n_loops
        stimuli_on = True
        last_state.value = -1
        state = 1
        i = 0

        while i != self.n_stim * self.n_loops * 2:

            if stimuli_on:
                index = np.mod(current_frame, 300)
                for j in range(len(self.squares_list)):
                    self.squares_list[j].opacity = self.func_list[j][index]

            self.window.flip()
            current_frame += 1
            if current_frame == self.times[i]:
                i += 1
                if i % 2 == 0:
                    stimuli_on = True
                    last_state.value = state
                    state = 1
                    stim_off.clear()
                else:
                    stim_off.set()
                    stimuli_on = False

                    last_state.value = 1
                    state = -1


            for key in event.getKeys():
                if key in ['escape', 'q']:
                    core.quit()
        stim_off.set()
        end.set()
        self.window.flip()
        self.window.close()
