 import argparse
from brainflow.board_shim import BoardShim, BrainFlowInputParams, BoardIds, BrainFlowPresets
from brainflow.data_filter import DataFilter, FilterTypes
import sys
import numpy as np


class Board():

    def __init__(self, eeg_channels):
        parser = argparse.ArgumentParser()
        parser.add_argument('--serial-port', type=str, help='serial port', required=False, default='COM4')  #
        parser.add_argument('--board-id', type=int, default=0)  # 1 for Ganglion, 0 for Cyton
        self.args = parser.parse_args()
        params = BrainFlowInputParams()
        params.serial_port = self.args.serial_port
        self.board = BoardShim(self.args.board_id, params)
        self.sampling_rate = self.board.get_sampling_rate(self.args.board_id)
        self.eeg_channels = eeg_channels
        self.how_much_exec = 0

    def streaming(self):
        self.board.prepare_session()
        self.board.start_stream(2000)

    def stop_streaming(self):
        self.board.stop_stream()
        self.board.release_session()

    def get_data(self, last_state, nr, stim_length):
        if self.board.get_board_data_count() >= (stim_length * 250):  #prevent multiple data collection  after the same stimulus
            self.how_much_exec += 1
            trigg_arr = np.full((1, self.sampling_rate * stim_length), last_state.value) #add triggers to data
            self.data = self.board.get_board_data()[1:len(self.eeg_channels) + 1]

            self.data = np.append(self.data[:, -(stim_length * 250):], trigg_arr, axis=0) #save only the data corresponding to stimulus
            DataFilter.write_file(self.data, 'S{}.csv'.format(nr), 'a')

    def filter_signal(self, ch):
        DataFilter.perform_bandpass(self.data[ch], sampling_rate=self.sampling_rate,
                                    start_freq=10, stop_freq=45, order=4,
                                    filter_type=FilterTypes.BUTTERWORTH.value, ripple=0)
        DataFilter.perform_bandstop(self.data[ch], sampling_rate=self.sampling_rate,
                                    start_freq=48, stop_freq=52, order=4,
                                    filter_type=FilterTypes.BUTTERWORTH.value, ripple=0)


def play(last_state, nr, stim_off, end, stim_length):
    eeg_channels = [1, 2, 3, 4]
    cyton = Board(eeg_channels)
    cyton.streaming()
    while True:
        stim_off.wait()  # wait until a stimulus is turned off
        cyton.get_data(last_state, nr, stim_length)
        if end.is_set():  # exit if stimulation has ended
            cyton.stop_streaming()
            print(cyton.how_much_exec)
            sys.exit()
