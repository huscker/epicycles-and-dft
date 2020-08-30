import numpy as np
import scipy.signal
import math
import matplotlib.pyplot as plt


class FFT1:
    def __init__(self, funct, dur=10, samples=600):
        self.change_funct(funct, dur, samples)

    def change_funct(self, funct, dur=10, samples=600):
        self.dur = dur
        self.samples = samples
        self.t = np.linspace(0, self.dur, num=self.samples)
        self.funct = funct
        self.res = np.fft.fft(np.array(list(map(funct, 2 * np.pi * self.t))))[:samples // 2]
        self.peaks = scipy.signal.find_peaks(np.abs(self.res) - 5.0, height=0)[0]

    def get_freq_amp_phase(self, without_peaks=False):
        freq = list()
        amp = list()
        phase = list()
        max_amp = -1.0
        if not without_peaks:
            for i in self.peaks:
                freq.append(i / self.dur)
                amp.append(np.abs(self.res[i]))
                phase.append(math.atan2(np.imag(self.res[i]), np.real(self.res[i])) * self.dur)
                max_amp = max(max_amp, np.abs(self.res[i]))
            amp = list(map(lambda x: x / max_amp, amp))
        else:
            for i in range(len(self.res)):
                if i / self.dur > 0:
                    freq.append(i / self.dur)
                    amp.append(np.abs(self.res[i]))
                    phase.append(math.atan2(np.imag(self.res[i]), np.real(self.res[i])) * self.dur)
                    max_amp = max(max_amp, np.abs(self.res[i]))
            amp = list(map(lambda x: x / max_amp, amp))
        return [freq, amp, phase]


class FFT2:
    def __init__(self, pts):
        self.X = np.fft.fft(list(map(lambda x: x[0], pts)))[:len(pts) // 2]
        self.Y = np.fft.fft(list(map(lambda x: x[1], pts)))[:len(pts) // 2]
        self.peaksX = scipy.signal.find_peaks(np.abs(self.X) - 5.0, height=0)[0]
        self.peaksY = scipy.signal.find_peaks(np.abs(self.Y) - 5.0, height=0)[0]

    def get_freq_amp_phase(self, without_peaks=False):
        freqX, freqY, ampX, ampY, phaseX, phaseY = list(), list(), list(), list(), list(), list()
        max_ampX = -1.0
        max_ampY = -1.0
        if not without_peaks:
            for i in self.peaksX:
                freqX.append(i)
                ampX.append(np.abs(self.X[i]))
                phaseX.append(math.atan2(np.imag(self.X[i]), np.real(self.X[i])))
                max_ampX = max(max_ampX, np.abs(self.X[i]))
            ampX = list(map(lambda x: x / max_ampX, ampX))
        else:
            for i in range(len(self.X)):
                if i > 0:
                    freqX.append(i)
                    ampX.append(np.abs(self.X[i]))
                    phaseX.append(math.atan2(np.imag(self.X[i]), np.real(self.X[i])))
                    max_ampX = max(max_ampX, np.abs(self.X[i]))
            ampX = list(map(lambda x: x / max_ampX, ampX))

        if not without_peaks:
            for i in self.peaksY:
                freqY.append(i)
                ampY.append(np.abs(self.Y[i]))
                phaseY.append(math.atan2(np.imag(self.Y[i]), np.real(self.Y[i])))
                max_ampY = max(max_ampY, np.abs(self.Y[i]))
            ampY = list(map(lambda x: x / max_ampY, ampY))
        else:
            for i in range(len(self.Y)):
                if i > 0:
                    freqY.append(i)
                    ampY.append(np.abs(self.Y[i]))
                    phaseY.append(math.atan2(np.imag(self.Y[i]), np.real(self.Y[i])))
                    max_ampY = max(max_ampY, np.abs(self.Y[i]))
            ampY = list(map(lambda x: x / max_ampY, ampY))
        return (freqX, freqY, ampX, ampY, phaseX, phaseY)


class FFT3:
    def __init__(self, pts):
        self.X = myfft(list(map(lambda x: complex(x[0], x[1]), pts)))

    def get_freq_amp_phase(self):
        freq = list()
        amp = list()
        phase = list()
        max_amp = -1.0
        for i in range(len(self.X)):
            if i > 0:
                amp.append(np.abs(self.X[i]))
                phase.append(math.atan2(np.imag(self.X[i]), np.real(self.X[i])))
                if i > len(self.X) / 2:
                    freq.append(-(len(self.X) - i))
                else:
                    freq.append(i)
                max_amp = max(max_amp, np.abs(self.X[i]))
        amp = list(map(lambda x: x / max_amp, amp))
        return [freq, amp, phase]


def myfft(compl):
    n = len(compl)
    out = list()
    for k in range(n):
        sumreal = 0
        sumimag = 0
        for t in range(n):
            angle = 2 * math.pi * t * k / n
            sumreal += compl[t].real * math.cos(angle) + compl[t].imag * math.sin(angle)
            sumimag += -compl[t].real * math.sin(angle) + compl[t].imag * math.cos(angle)
        out.append(complex(sumreal, sumimag))
    return out
