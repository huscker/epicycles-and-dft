import numpy as np
import scipy.signal
import math


class FFT_1D:
    def __init__(self, funct, dur: float = 10, samples: int = 600):
        # funct - function to transform
        self.change_funct(funct, dur, samples)

    def change_funct(self, funct, dur: float = 10, samples: int = 600):
        self.dur = dur
        self.samples = samples
        self.t = np.linspace(0, self.dur, num=self.samples)
        self.funct = funct
        self.res = np.fft.fft(np.array(list(map(funct, 2 * np.pi * self.t))))[:samples // 2]

    def get_freq_amp_phase(self, peak_threshold: float = 0.0):
        freq = list()
        amp = list()
        phase = list()
        max_amp = -1.
        if peak_threshold > 0.0:  # get peaks
            peaks = scipy.signal.find_peaks(np.abs(self.res) - peak_threshold, height=0)[0]
            for i in peaks:  # parse fft
                freq.append(i / self.dur)
                amp.append(np.abs(self.res[i]))
                phase.append(math.atan2(np.imag(self.res[i]), np.real(self.res[i])) * self.dur)
                max_amp = max(max_amp, np.abs(self.res[i]))
            amp = list(map(lambda x: x / max_amp, amp))  # normalize
        else:  # without peaks
            for i in range(len(self.res)):  # parse fft
                if i / self.dur > 0:
                    freq.append(i / self.dur)
                    amp.append(np.abs(self.res[i]))
                    phase.append(math.atan2(np.imag(self.res[i]), np.real(self.res[i])) * self.dur)
                    max_amp = max(max_amp, np.abs(self.res[i]))
            amp = list(map(lambda x: x / max_amp, amp))  # normalize
        return [freq, amp, phase]


class FFT_2D_DOUBLE:
    def __init__(self, pts: list):
        self.X = np.fft.fft(list(map(lambda x: x[0], pts)))[:len(pts) // 2]
        self.Y = np.fft.fft(list(map(lambda x: x[1], pts)))[:len(pts) // 2]

    def get_freq_amp_phase(self, peak_threshold: float = 0.0):
        freqX, freqY, ampX, ampY, phaseX, phaseY = list(), list(), list(), list(), list(), list()
        max_ampX = -1.0
        max_ampY = -1.0
        if peak_threshold > 0.0:  # get peaks
            peaksX = scipy.signal.find_peaks(np.abs(self.X) - peak_threshold, height=0)[0]
            peaksY = scipy.signal.find_peaks(np.abs(self.Y) - peak_threshold, height=0)[0]
            for i in peaksX:  # parse fft
                freqX.append(i)
                ampX.append(np.abs(self.X[i]))
                phaseX.append(math.atan2(np.imag(self.X[i]), np.real(self.X[i])))
                max_ampX = max(max_ampX, np.abs(self.X[i]))
            ampX = list(map(lambda x: x / max_ampX, ampX))  # normalize
            for i in peaksY:  # parse fft
                freqY.append(i)
                ampY.append(np.abs(self.Y[i]))
                phaseY.append(math.atan2(np.imag(self.Y[i]), np.real(self.Y[i])))
                max_ampY = max(max_ampY, np.abs(self.Y[i]))
            ampY = list(map(lambda x: x / max_ampY, ampY))  # normalize
        else:  # without peaks
            for i in range(len(self.X)):  # parse fft
                if i > 0:
                    freqX.append(i)
                    ampX.append(np.abs(self.X[i]))
                    phaseX.append(math.atan2(np.imag(self.X[i]), np.real(self.X[i])))
                    max_ampX = max(max_ampX, np.abs(self.X[i]))
            ampX = list(map(lambda x: x / max_ampX, ampX))  # normalize
            for i in range(len(self.Y)):  # parse fft
                if i > 0:
                    freqY.append(i)
                    ampY.append(np.abs(self.Y[i]))
                    phaseY.append(math.atan2(np.imag(self.Y[i]), np.real(self.Y[i])))
                    max_ampY = max(max_ampY, np.abs(self.Y[i]))
            ampY = list(map(lambda x: x / max_ampY, ampY))  # normalize
        return (freqX, freqY, ampX, ampY, phaseX, phaseY)


class FFT_2D_PURE:
    def __init__(self, pts: list):
        self.res = np.fft.fft(list(map(lambda x: np.complex(x[0], x[1]), pts)))

    def get_freq_amp_phase(self, peak_threshold: float = 0.0):
        freq = list()
        amp = list()
        phase = list()
        max_amp = -1.0
        if peak_threshold > 0.0:  # parse fft
            peaks = scipy.signal.find_peaks(np.abs(self.res) - peak_threshold, height=0)[0]
            for i in peaks:  # parse fft
                amp.append(np.abs(self.res[i]))
                phase.append(math.atan2(np.imag(self.res[i]), np.real(self.res[i])))
                if i > len(self.res) / 2:  # check for negative freqs
                    freq.append(-(len(self.res) - i))
                else:
                    freq.append(i)
                max_amp = max(max_amp, np.abs(self.res[i]))
            amp = list(map(lambda x: x / max_amp, amp))  # normalize
        else:  # without peaks
            for i in range(len(self.res)):  # parse fft
                if i > 0:
                    amp.append(np.abs(self.res[i]))
                    phase.append(math.atan2(np.imag(self.res[i]), np.real(self.res[i])))
                    if i > len(self.res) / 2:  # check for negative freqs
                        freq.append(-(len(self.res) - i))
                    else:
                        freq.append(i)
                    max_amp = max(max_amp, np.abs(self.res[i]))
            amp = list(map(lambda x: x / max_amp, amp))  # normalize
        return [freq, amp, phase]
