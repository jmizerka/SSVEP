from multiprocessing import Process, Value, Event
from data_acquisition.board3 import play
   
def display_stimuli(last_state,stim_off,end,stim_length):
    from ssvep_stimuli.speller import experiment2_psypy
    dd=experiment2_psypy(stim_length,1,180)
    dd.run(last_state,stim_off,end)

if __name__ == '__main__':
    stim_off = Event()
    end = Event()
    nr = int(input("Podaj numer osoby badanej: "))
    last_state = Value('i',-1)
    stim_length = 3
    proc2 = Process(target = display_stimuli, args =(last_state,stim_off,end,stim_length))
    proc2.start()
    play(last_state,nr,stim_off,end,stim_length)
    proc2.join()

