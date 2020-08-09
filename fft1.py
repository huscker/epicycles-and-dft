import numpy as np
import scipy
import math
class FFT1:
    def __init__(self,funct,dur=10,samples=600):
        self.change_funct(funct,dur,samples)
    def change_funct(self,funct,dur=10,samples=600):
        self.dur = dur
        self.samples = samples
        self.t = np.linspace(0, dur, num=samples)
        self.funct = funct
        self.res = np.fft.fft(np.array(list(map(funct, 2 * np.pi * self.t))))[:samples // 2]
        self.peaks = scipy.signal.find_peaks(np.abs(self.res)-5.0,height=0)[0]
    def get_freq_amp_phase(self,without_peaks=False):
        freq = list()
        amp = list()
        phase = list()
        max_amp = -1.0
        if not without_peaks:
            for i in self.peaks:
                freq.append(i/self.dur)
                amp.append(np.abs(self.res[i]))
                phase.append(math.atan2(np.imag(self.res[i]),np.real(self.res[i]))*self.dur)
                max_amp = max(max_amp,np.abs(self.res[i]))
            amp = list(map(lambda x:x/max_amp,amp))
        else:
            for i in range(len(self.res)):
                if i/self.dur > 0:
                    freq.append(i/self.dur)
                    amp.append(np.abs(self.res[i]))
                    phase.append(math.atan2(np.imag(self.res[i]),np.real(self.res[i]))*self.dur)
                    max_amp = max(max_amp,np.abs(self.res[i]))
            amp = list(map(lambda x:x/max_amp,amp))
        return [freq,amp,phase]