import pygame,numpy
from epicycles import Epicycle
from fft1 import FFT1,FFT2,FFT3

import sys

from pygame.locals import *

def get_points(s):
    return list(map(lambda x: list(map(lambda y: float(y),x.split(','))),s.split()))
def update_data(pts):
    minX = 10e10
    maxX = -10e10
    minY = 10e10
    maxY = -10e10
    for i in pts:
        minX = min(minX,i[0])
        maxX = max(maxX,i[0])
        minY = min(minY,i[1])
        maxY = max(maxY,i[1])
    for i in pts:
        i[0] = ((i[0] - minX)/(maxX-minX) - 0.5)*2
        i[1] = ((i[1] - minY) / (maxY - minY) - 0.5)*2
    return pts

pts = update_data(get_points('''122.26765546658731,156.36515923543936
118.30763107591429,153.36871294433425
114.11028529087551,150.64245379161753
110.09607883962155,147.6865277583647
107.32394335584786,151.08893496451194
103.95629014263692,154.78515079272066
100.56746734259082,158.44185418533334
97.15237705813018,162.11074373651212
93.75017989914753,165.78204160581865
90.40242460513791,169.49242644589
90.68065488918448,167.77644708715442
91.99338944893002,162.95718369399128
93.34861608493561,158.14366842040664
91.56631574243549,155.62906565543736
87.00027648386354,153.60173553912247
82.44972280869185,151.50782049790317
77.91880655057832,149.40163190603738
73.3732026591446,147.29152268410468
68.83155207589765,145.22251537109554
67.14390999186891,144.26910708456256
72.13812440977344,144.1029703497305
77.13097861589435,143.85123263349305
80.61999720725872,143.1072559135914
81.06779950569144,138.12556558688087
81.63755323859482,133.15567481659193
82.23611271129352,128.1985099107024
82.84008608706,123.23692001285386
83.42505577451797,118.26763357310875
83.86153812986166,113.29177874794709
85.07076545534325,117.63419297701375
86.86081258714286,122.30135175732332
88.46277740900322,127.0372737264073
92.40640871271768,126.31418733585986
97.29903307024614,125.2989940036533
102.21208716375591,124.32662672739865
107.11591539565978,123.36873069667519
112.03032896949446,122.39920129151963
116.92304365105413,121.37416421676194
116.26375596015515,122.32723170811984
112.36675545856477,125.44567537321095
108.44892254077436,128.55609184285404
107.9795213263799,131.54995185899477
110.49520524186907,135.87913819373514
112.94010624742513,140.23288916548645
115.37268628094962,144.60785001705216
117.80736420464726,148.98409562324497
120.26479668048115,153.33520405504197'''))
choice = 'FFT3'

pygame.init()
fps = 60
fpsClock = pygame.time.Clock()

width, height = 1500,1000
num_of_points = 2000
dist_from_origin = 400
sensitivity = 5
screen = pygame.display.set_mode((width, height))
surface = pygame.Surface((width,height))
translate = numpy.array([-dist_from_origin,0],dtype=numpy.int)
translate2 = numpy.array([100,0],dtype=numpy.int)
translate3 = numpy.array([0,dist_from_origin],dtype=numpy.int)
zero = numpy.array([width//2,height//2],dtype=numpy.int)
pos = numpy.array([0,0],dtype=numpy.float)
points = list()
pointsX = list()
pointsY = list()
scale = 100
movementUnlocked = False

if choice == 'FFT1':
    def f(x):
        if numpy.sin(x) >= 0:
            return 1.0
        else:
            return -1.0

    def f(x):
        return x
    fft1 = FFT1(f,10,600)
    freq,amp,phase = fft1.get_freq_amp_phase(without_peaks=True)
    ep = Epicycle()
    for i in range(len(freq)):
        ep.push_back(amp[i],freq[i],phase[i])
    amps=ep.get_amps()
elif choice == 'FFT2':
    fft2 = FFT2(pts)
    freqX,freqY,ampX,ampY,phaseX,phaseY = fft2.get_freq_amp_phase(without_peaks=True)
    print(fft2.get_freq_amp_phase(without_peaks=True))
    epX = Epicycle()
    epY = Epicycle()
    for i in range(len(freqX)-1,-1,-1):
        epX.push_back(ampX[i],freqX[i],phaseX[i])
    for i in range(len(freqY)):
        epY.push_back(ampY[i],freqY[i],phaseY[i])
elif choice == 'FFT3':
    fft3 = FFT3(pts)
    freq,amp,phase = fft3.get_freq_amp_phase()
    ep = Epicycle()
    for i in range(len(freq)):
        ep.push_back(amp[i],freq[i],phase[i])
# Game loop.
while True:
    #screen.fill((0, 0, 0))
    surface.fill((0,0,0))
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEMOTION:
            if movementUnlocked:
                pos[0] += -event.rel[0] / sensitivity
                pos[1] += event.rel[1] / sensitivity
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 2:
                movementUnlocked = True
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 2:
                movementUnlocked = False
                pos[0] = 0
                pos[1] = 0

    zero += numpy.array([pos[0],pos[1]],dtype=numpy.int)
    if choice == 'FFT1':
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
    elif choice == 'FFT2':
        #'''
        for i in pts:
            surface.set_at((zero[0] + int(i[0]*scale)+-translate3[0], zero[1] - int(i[1]*scale)-translate3[1]),
                           pygame.Color('green'))
        #'''
        coordsX = epX.get_points(pygame.time.get_ticks()/7000.0)
        coordsY = epY.get_points(pygame.time.get_ticks() / 7000.0)
        pointsX.append(coordsX[-1][0])
        pointsY.append(coordsY[-1][0])
        if len(pointsX) > num_of_points + 10:
            pointsX.remove(pointsX[0])
        if len(pointsY) > num_of_points + 10:
            pointsY.remove(pointsY[0])
        for i in range(len(coordsX[:-1])):
            if(int(ampX[i]*scale)>0):
                pygame.draw.circle(surface,pygame.Color(100,100,100),zero+translate3-numpy.array(scale*coordsX[i],dtype=numpy.int),int(ampX[i]*scale),1)
            if i != 0:
                pygame.draw.line(surface,pygame.Color('white'),zero+translate3-numpy.array(coordsX[i]*scale,dtype=numpy.int),zero+translate3-numpy.array(scale*coordsX[i-1],dtype=numpy.int),2)
            if (int(ampY[i] * scale) > 0):
                pygame.draw.circle(surface, pygame.Color(100, 100, 100),
                                   zero + translate +numpy.array(scale*numpy.array([coordsY[i][1],coordsY[i][0]]), dtype=numpy.int), int(ampY[i] * scale), 1)
            if i != 0:
                pygame.draw.line(surface,pygame.Color('white'),zero+translate+numpy.array(scale*numpy.array([coordsY[i][1],coordsY[i][0]]), dtype=numpy.int),zero+translate+numpy.array(scale*numpy.array([coordsY[i-1][1],coordsY[i-1][0]]), dtype=numpy.int),2)
        if len(coordsX) > 1:
            pygame.draw.line(surface,pygame.Color('white'),zero+translate3-numpy.array(coordsX[-1]*scale,dtype=numpy.int),zero+translate3-numpy.array(scale*coordsX[-2],dtype=numpy.int),2)
        if len(coordsX) > 1:
            pygame.draw.line(surface,pygame.Color('white'),zero+translate+numpy.array(scale*numpy.array([coordsY[-1][1],coordsY[-1][0]]), dtype=numpy.int),zero+translate+numpy.array(scale*numpy.array([coordsY[-2][1],coordsY[-2][0]]), dtype=numpy.int),2)
        pygame.draw.line(surface,pygame.Color('yellow'),zero+translate3-numpy.array(scale*coordsX[-1],dtype=numpy.int),zero +numpy.array(scale*numpy.array([-pointsX[-1],pointsY[-1]])),1)
        pygame.draw.line(surface, pygame.Color('yellow'),
                         zero + translate +numpy.array(scale*numpy.array([coordsY[-1][1],coordsY[-1][0]]), dtype=numpy.int),
                         zero +numpy.array(scale*numpy.array([-pointsX[-1],pointsY[-1]]), dtype=numpy.int), 1)
        for i in range(-1,-len(pointsX[:num_of_points]),-1):
            surface.set_at((zero[0]-int(scale*pointsX[i]),zero[1]+int(scale*pointsY[i])),pygame.Color('white'))
    elif choice == 'FFT3':
        coords = ep.get_points(pygame.time.get_ticks()/1000.0)
        print( scale * numpy.array(coords,dtype=numpy.int))
        points.append(coords[-1])
        if len(points) > num_of_points + 10:
            points.remove(points[0])
        for i in range(len(coords[:-1])):
            if(int(amp[i]*scale)>0):
                pygame.draw.circle(surface,pygame.Color(100,100,100),zero+numpy.array([coords[i][0]*-scale,coords[i][1]*scale],dtype=numpy.int),int(amp[i]*scale),1)
            if i != 0:
                pygame.draw.line(surface,pygame.Color('white'),zero+numpy.array([-scale*coords[i][0],scale*coords[i][1]],dtype=numpy.int),zero+numpy.array([-scale*coords[i-1][0],scale*coords[i-1][1]],dtype=numpy.int),1)
        if len(coords) > 1:
            pygame.draw.line(surface, pygame.Color('white'),
                             zero + numpy.array([-scale * coords[-1][0], scale * coords[-1][1]], dtype=numpy.int),
                             zero + numpy.array([-scale * coords[-2][0], scale * coords[-2][1]], dtype=numpy.int),
                             1)
        for i in range(-1,-len(points[:num_of_points]),-1):
            surface.set_at((zero[0]-int(scale*points[i][0]),zero[1]+int(scale*points[i][1])),pygame.Color('yellow'))
    surface = pygame.transform.flip(surface,False,True)
    screen.blit(surface,(0,0))
    pygame.display.flip()
    fpsClock.tick(fps)


