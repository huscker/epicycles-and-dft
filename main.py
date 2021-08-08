import pygame, numpy, sys, copy
from epicycles import Epicycle
from fft import FFT_1D, FFT_2D_DOUBLE, FFT_2D_PURE
from pygame.locals import *

def get_points(s):
    return list(map(lambda x: list(map(lambda y: float(y), x.split(','))), s.split()))

def update_data(pts):
    minX = 10e10
    maxX = -10e10
    minY = 10e10
    maxY = -10e10
    for i in pts:
        minX = min(minX, i[0])
        maxX = max(maxX, i[0])
        minY = min(minY, i[1])
        maxY = max(maxY, i[1])
    for i in pts:
        i[0] = ((i[0] - minX) / (maxX - minX) - 0.5) * 2
        i[1] = ((i[1] - minY) / (maxY - minY) - 0.5) * 2
    return pts

# input data

user_pts = update_data(get_points('''122.26765546658731,156.36515923543936 
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
pts = list()

# render options
fps = 60
width, height = 1500, 1000
num_of_points = 2000
dist_from_origin = 400
sensitivity = 5
time_scale = 1/4000.0
# modes:
# FFT1 - 1 epicycle, 1D input data
# FFT2 - 2 epicycles, 2D input data
# FFT3 - 1 epicycle, 2D input data
choice = 'FFT2'
if choice == 'FFT1':
    def fft_1d_funct(x):
        if numpy.sin(x) >= 0:
            return 1
        else:
            return -1

pygame.init()
fpsClock = pygame.time.Clock()
screen = pygame.display.set_mode((width, height))
surface = pygame.Surface((width, height))
translate = numpy.array([-dist_from_origin, 0], dtype=numpy.int)
translate2 = numpy.array([100, 0], dtype=numpy.int)
translate3 = numpy.array([0, dist_from_origin], dtype=numpy.int)
zero = numpy.array([width // 2, height // 2], dtype=numpy.int)
pos = numpy.array([0, 0], dtype=numpy.float)
points = list()
pointsX = list()
pointsY = list()
scale = 100
scale_val = 1
movementUnlocked = False
isScalling = False
isAdding = False
isShowing = True
pygame.time.set_timer(pygame.MIDIOUT,50)
ep,epX,epY = Epicycle(),Epicycle(),Epicycle()
def redraw():
    global ep,epX,epY,pts,user_pts,amps,amp,freq,phase,freqX,freqY,ampX,ampY,phaseX,phaseY
    pts.clear()
    pts = copy.deepcopy(user_pts)
    if choice == 'FFT1': 
        ep = Epicycle()
        fft_parser = FFT_1D(fft_1d_funct, 10, 600)
        freq, amp, phase = fft_parser.get_freq_amp_phase()
        for i in range(len(freq)):
            ep.push_back(amp[i], freq[i], phase[i])
        amps = ep.get_amps()
    elif choice == 'FFT2':
        epX = Epicycle()
        epY = Epicycle()
        fft_parser = FFT_2D_DOUBLE(pts)
        freqX, freqY, ampX, ampY, phaseX, phaseY = fft_parser.get_freq_amp_phase()
        for i in range(len(freqX) - 1, -1, -1):
            epX.push_back(ampX[i], freqX[i], phaseX[i])
        for i in range(len(freqY)):
            epY.push_back(ampY[i], freqY[i], phaseY[i])
    elif choice == 'FFT3':
        fft_parser = FFT_2D_PURE(pts)
        freq, amp, phase = fft_parser.get_freq_amp_phase()
        ep = Epicycle()
        for i in range(len(freq)):
            ep.push_back(amp[i], freq[i], phase[i])
redraw()
while True:
    surface.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MIDIOUT:
            if isAdding:
                user_pts.append((-numpy.array(pygame.mouse.get_pos())+zero)/scale)
        if event.type == pygame.MOUSEMOTION:
            if movementUnlocked and not isScalling:
                pos[0] += -event.rel[0] / sensitivity
                pos[1] += event.rel[1] / sensitivity
            if isScalling:
                scale_val = min(max(1.0, scale_val + event.rel[1] / 20.0), 20.0)
                scale = int(100 * scale_val)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                movementUnlocked = True
            if event.button == 3:
                isAdding = True
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                movementUnlocked = False
                pos[0] = 0
                pos[1] = 0
            if event.button == 3:
                isAdding = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_c:
                isScalling = True
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.key == pygame.K_SPACE:
                points.clear()
                pointsX.clear()
                pointsY.clear()
                redraw()
            if event.key == pygame.K_e:
                user_pts.clear()
            if event.key == pygame.K_s:
                isShowing = not isShowing
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_c:
                isScalling = False

    zero += numpy.array([pos[0], pos[1]], dtype=numpy.int)
    if choice == 'FFT1':
        coords = ep.get_points(pygame.time.get_ticks()*time_scale)
        points.append(coords[-1][1])
        if len(points) > num_of_points + 10:
            points.remove(points[0])
        for i in range(len(coords[:-1])):
            if (int(amps[i] * scale) > 0):
                pygame.draw.circle(surface, pygame.Color(100, 100, 100),
                                   zero + translate + numpy.array(scale * coords[i], dtype=numpy.int),
                                   int(amps[i] * scale), 1)
            if i != 0:
                pygame.draw.line(surface, pygame.Color('white'),
                                 zero + translate + numpy.array(scale * coords[i], dtype=numpy.int),
                                 zero + translate + numpy.array(scale * coords[i - 1], dtype=numpy.int), 2)
        if len(coords) > 1:
            pygame.draw.line(surface, pygame.Color('white'),
                             zero + translate + numpy.array(scale * coords[-1], dtype=numpy.int),
                             zero + translate + numpy.array(scale * coords[-2], dtype=numpy.int), 2)
        pygame.draw.line(surface, pygame.Color('yellow'),
                         translate + zero + numpy.array(coords[-1] * scale, dtype=numpy.int),
                         ((zero)[0] + translate2[0], ((zero)[1] + translate2[1] + int(scale * points[-1]))), 1)
        for i in range(-1, -len(points[:num_of_points]), -1):
            surface.set_at((zero[0] - i + translate2[0], zero[1] + int(scale * points[i]) + translate2[1]),
                           pygame.Color('yellow'))
    elif choice == 'FFT2':
        coordsX = epX.get_points(pygame.time.get_ticks()*time_scale)
        coordsY = epY.get_points(pygame.time.get_ticks()*time_scale)
        pointsX.append(coordsX[-1][0])
        pointsY.append(coordsY[-1][0])
        if len(pointsX) > num_of_points + 10:
            pointsX.remove(pointsX[0])
        if len(pointsY) > num_of_points + 10:
            pointsY.remove(pointsY[0])
        for i in range(len(coordsX[:-1])):
            if (int(ampX[i] * scale) > 0):
                pygame.draw.circle(surface, pygame.Color(100, 100, 100),
                                   zero + translate3 - numpy.array(scale * coordsX[i], dtype=numpy.int),
                                   int(ampX[i] * scale), 1)
            if i != 0:
                pygame.draw.line(surface, pygame.Color('white'),
                                 zero + translate3 - numpy.array(coordsX[i] * scale, dtype=numpy.int),
                                 zero + translate3 - numpy.array(scale * coordsX[i - 1], dtype=numpy.int), 2)
            if (int(ampY[i] * scale) > 0):
                pygame.draw.circle(surface, pygame.Color(100, 100, 100),
                                   zero + translate + numpy.array(scale * numpy.array([coordsY[i][1], coordsY[i][0]]),
                                                                  dtype=numpy.int), int(ampY[i] * scale), 1)
            if i != 0:
                pygame.draw.line(surface, pygame.Color('white'),
                                 zero + translate + numpy.array(scale * numpy.array([coordsY[i][1], coordsY[i][0]]),
                                                                dtype=numpy.int), zero + translate + numpy.array(
                        scale * numpy.array([coordsY[i - 1][1], coordsY[i - 1][0]]), dtype=numpy.int), 2)
        if len(coordsX) > 1:
            pygame.draw.line(surface, pygame.Color('white'),
                             zero + translate3 - numpy.array(coordsX[-1] * scale, dtype=numpy.int),
                             zero + translate3 - numpy.array(scale * coordsX[-2], dtype=numpy.int), 2)
        if len(coordsY) > 1:
            pygame.draw.line(surface, pygame.Color('white'),
                             zero + translate + numpy.array(scale * numpy.array([coordsY[-1][1], coordsY[-1][0]]),
                                                            dtype=numpy.int),
                             zero + translate + numpy.array(scale * numpy.array([coordsY[-2][1], coordsY[-2][0]]),
                                                            dtype=numpy.int), 2)
        pygame.draw.line(surface, pygame.Color('yellow'),
                         zero + translate3 - numpy.array(scale * coordsX[-1], dtype=numpy.int),
                         zero + numpy.array(scale * numpy.array([-pointsX[-1], pointsY[-1]])), 1)
        pygame.draw.line(surface, pygame.Color('yellow'),
                         zero + translate + numpy.array(scale * numpy.array([coordsY[-1][1], coordsY[-1][0]]),
                                                        dtype=numpy.int),
                         zero + numpy.array(scale * numpy.array([-pointsX[-1], pointsY[-1]]), dtype=numpy.int), 1)
        for i in range(-1, -len(pointsX[:num_of_points]), -1):
            surface.set_at((zero[0] - int(scale * pointsX[i]), zero[1] + int(scale * pointsY[i])),
                           pygame.Color('white'))
    elif choice == 'FFT3':
        coords = ep.get_points(pygame.time.get_ticks() / 1000.0)
        points.append(coords[-1])
        if len(points) > num_of_points + 10:
            points.remove(points[0])
        for i in range(len(coords[:-1])):
            if (int(amp[i] * scale) > 0):
                pygame.draw.circle(surface, pygame.Color(100, 100, 100),
                                   zero + numpy.array([coords[i][0] * -scale, coords[i][1] * scale], dtype=numpy.int),
                                   int(amp[i] * scale), 1)
            if i != 0:
                pygame.draw.line(surface, pygame.Color('white'),
                                 zero + numpy.array([-scale * coords[i][0], scale * coords[i][1]], dtype=numpy.int),
                                 zero + numpy.array([-scale * coords[i - 1][0], scale * coords[i - 1][1]],
                                                    dtype=numpy.int), 1)
        if len(coords) > 1:
            pygame.draw.line(surface, pygame.Color('white'),
                             zero + numpy.array([-scale * coords[-1][0], scale * coords[-1][1]], dtype=numpy.int),
                             zero + numpy.array([-scale * coords[-2][0], scale * coords[-2][1]], dtype=numpy.int),
                             1)
        for i in range(-1, -len(points[:num_of_points]), -1):
            surface.set_at((zero[0] - int(scale * points[i][0]), zero[1] + int(scale * points[i][1])),
                           pygame.Color('yellow'))
    if choice != 'FFT1' and isShowing:
        for i in range(-1,-len(user_pts),-1):
            surface.set_at((zero[0] - int(scale * user_pts[i][0]), zero[1] + int(scale * user_pts[i][1])),
                           pygame.Color('white'))
    surface = pygame.transform.flip(surface, False, True)
    screen.blit(surface, (0, 0))
    pygame.display.flip()
    fpsClock.tick(fps)
