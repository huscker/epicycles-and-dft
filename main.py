import pygame,numpy
from epicycles import Epicycle
from fft1 import FFT1,FFT2

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

pts = update_data(get_points('''47.21826513449527,35.465074736371115
51.76168261564302,34.91704893177915
55.776000339608665,31.977961308454276
59.17338106326294,28.304448029235843
58.10061057408858,26.63387741277981
56.759669135810846,31.458686484233866
56.002674663991534,36.39208851657303
55.42279020455265,41.35861927183075
54.7873819577271,46.31427486907963
53.76484156194205,51.20677985154312
51.432169481769556,55.18291074848557
50.08270186599732,51.942170562957784
53.344768099803815,48.14997746614843
56.940734711079344,44.684368533530176
60.602542693493504,41.279318653889746
64.25445743280696,37.86520097204596
67.56751402978516,34.1198536254883
69.72146086205227,29.7250416946878
66.12908126156358,29.785685134351382
64.08717991644288,34.32461224224855
62.74772619217527,39.1417255324513
62.00449441688443,44.07353588009741
62.092733255986225,49.07289138340332
64.63580950704957,52.56248892105104
67.3571264990821,48.48599593157913
69.6265797824989,44.048396609606826
72.86895356190158,41.34598286308482
68.55787576282135,43.309582420542135
65.73834075959863,47.40288062367071
67.06007733351542,51.51711619087675
71.4191467584696,49.72357713466932
73.89652018016278,45.42286376573179
73.7112084157699,42.039606469433025
72.61800439159538,46.90023312250854
74.45094825616457,49.30415914431764
77.10136769875379,45.073138047109445
80.25074203570946,41.22553105668464
82.17547007812503,41.619275687500014
78.52248095022951,43.64177399471898
77.4068228230858,48.49375235701372
79.15341351270749,51.74329579990997
82.22708204663948,47.89329742011645
84.17523910903934,51.669002226562526
87.75044060492179,49.418807866056945
89.64931463558963,44.817828081298856
90.67240577864656,39.91591341575642
88.5708859841123,38.067006740359325
86.6560232803102,42.657352834173224
87.83345822796394,45.39832388515523
90.15217891979763,41.04048972430142
90.69227268667318,44.948840522855306
90.82785900000003,49.89261840625002'''))
choice = 'FFT1'

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
        return numpy.sin(x)

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
    for i in range(len(freqX)):
        epX.push_back(ampX[i],freqX[i],phaseX[i])
    for i in range(len(freqY)):
        epY.push_back(ampY[i],freqY[i],phaseY[i])
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
        coordsX = epX.get_points(pygame.time.get_ticks()/10000.0)
        coordsY = epY.get_points(pygame.time.get_ticks() / 10000.0)
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

    surface = pygame.transform.flip(surface,False,True)
    screen.blit(surface,(0,0))
    pygame.display.flip()
    fpsClock.tick(fps)


