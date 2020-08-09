import pygame,numpy
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
from numpy import pi
from epicycles import Epicycle
from fft1 import FFT1

import sys

import pygame
from pygame.locals import *

pygame.init()
'''
ep = Epicycle()
ep.push_back(4.0/pi,1.0,0.0)
ep.push_back(4.0/(3.0*pi),3.0,0.0)
ep.push_back(4.0/(5.0*pi),5.0,0.0)
amps = ep.get_amps()
'''
fps = 60
fpsClock = pygame.time.Clock()
'''
t = numpy.linspace(0,20,num=600)
s = numpy.sin(2*numpy.pi*t)+numpy.sin(2*pi*3*t)*0.5
s = numpy.array(list(map(lambda x: 1.0 if x > 0 else 0.0,numpy.sin(2*pi*t))))
#plt.plot(t,s)
s = numpy.fft.fft(s)[:300]
freq = list()
amp = list()
for i in range(len(s)):
    freq.append( i/20)
    amp.append(numpy.abs(s[i]))
w = find_peaks(numpy.abs(s)-5.0,height=0)[0]
s = list()
for i in w:
    s.append(amp[i])
print(w)
print(s,len(s))
'''
def f(x):
    if numpy.sin(x) >= 0:
        return 1.0
    else:
        return -1.0

fft1 = FFT1(f,10,1000)
freq,amp,phase = fft1.get_freq_amp_phase(without_peaks=False)
print(freq)
print(amp)
print(phase)

width, height = 1000,800
num_of_points = 200
screen = pygame.display.set_mode((width, height))
surface = pygame.Surface((width,height))
translate = numpy.array([-200,0],dtype=numpy.int)
translate2 = numpy.array([100,0],dtype=numpy.int)
zero = numpy.array([width//2,height//2],dtype=numpy.int)
points = list()
scale = 100
ep = Epicycle()
for i in range(len(freq)):
    ep.push_back(amp[i],freq[i],phase[i])
amps=ep.get_amps()
# Game loop.
while True:
    #screen.fill((0, 0, 0))
    surface.fill((0,0,0))
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # Update.

    # Draw.
    coords = ep.get_points(pygame.time.get_ticks()/1000.0)
    points.append(coords[-1][1])
    if len(points) > num_of_points + 10:
        points.remove(points[0])
    #print(points)
    for i in range(len(coords[:-1])):
        if(int(amps[i] * scale) > 0):
            pygame.draw.circle(surface, pygame.Color(100,100,100), zero + translate+numpy.array(scale*coords[i],dtype=numpy.int), int(amps[i] * scale), 1)
            if i != 0:
                pygame.draw.line(surface,pygame.Color('white'),zero+translate+numpy.array(scale*coords[i],dtype=numpy.int),zero+translate+numpy.array(scale*coords[i-1],dtype=numpy.int),2)
    if len(coords) > 1:
        pygame.draw.line(surface, pygame.Color('white'), zero + translate + numpy.array(scale * coords[-1], dtype=numpy.int),
                     zero + translate + numpy.array(scale * coords[-2], dtype=numpy.int), 2)
    pygame.draw.line(surface,pygame.Color('yellow'),translate+zero+numpy.array(coords[-1]*scale,dtype=numpy.int),((zero)[0]+translate2[0],((zero)[1]+translate2[1]+int(scale*points[-1]))),1)
    for i in range(-1,-len(points[:num_of_points]),-1):
        surface.set_at((zero[0]-i+translate2[0],zero[1]+int(scale*points[i])+translate2[1]),pygame.Color('yellow'))
    surface = pygame.transform.flip(surface,False,True)
    screen.blit(surface,(0,0))
    pygame.display.flip()
    fpsClock.tick(fps)


