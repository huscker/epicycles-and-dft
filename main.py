import pygame, numpy, sys, copy
from epicycles import Epicycle
from fft import FFT_1D, FFT_2D_DOUBLE, FFT_2D_PURE


def get_points(s):  # parse string
    return list(map(lambda x: list(map(lambda y: float(y), x.split(','))), s.split()))


def update_data(pts):  # normalize pts
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
120.26479668048115,153.33520405504197'''))  # original pts
pts = list()  # render pts

# render options
fps = 60
width, height = 1500, 1000
num_of_points = 2000
dist_from_origin = 400
sensitivity = 5
time_scale = 1 / 4000.0
peak_threshold = 0.0
# modes:
# FFT1 - 1 epicycle, 1D input data
# FFT2 - 2 epicycles, 2D input data
# FFT3 - 1 epicycle, 2D input data
choice = 'FFT3'


def fft_1d_funct(x):  # funct for fft 1D
    if numpy.sin(x) >= 0:
        return 1
    else:
        return -1


# pygame init
pygame.init()
pygame.display.set_caption('Epicycles and DFT')
pygame.font.init()
font = pygame.font.SysFont(None, 30)
fpsClock = pygame.time.Clock()
screen = pygame.display.set_mode((width, height))
surface = pygame.Surface((width, height))
translate = numpy.array([-dist_from_origin, 0], dtype=numpy.int32)
translate2 = numpy.array([100, 0], dtype=numpy.int32)
translate3 = numpy.array([0, dist_from_origin], dtype=numpy.int32)
zero = numpy.array([width // 2, height // 2], dtype=numpy.int32)
pos = numpy.array([0, 0], dtype=numpy.float64)
points = list()
pointsX = list()
pointsY = list()
scale = 100
scale_val = 1
movementUnlocked = False
isScalling = False
isAdding = False
isShowing = True
prev_timescale = 0.0
total_time = 0.0
prev_time = 0
isPrintingInfo = False
state = 0  # 0 - idle, 1 - peak, 2 - dist, 3 - num, 4 - time
circle_primary_color = pygame.Color('white')
circle_secondary_color = pygame.Color(100, 100, 100)
render_pts_color = pygame.Color('yellow')
user_pts_color = pygame.Color('pink')
info_color = pygame.Color('green')
pygame.time.set_timer(pygame.MIDIOUT, 100)
ep, epX, epY = Epicycle(), Epicycle(), Epicycle()


def redraw():
    global ep, epX, epY, pts, user_pts, amps, amp, freq, phase, freqX, freqY, ampX, ampY, phaseX, phaseY
    if len(user_pts) <= 0:
        return
    pts.clear()
    pts = copy.deepcopy(user_pts)
    if choice == 'FFT1':
        ep = Epicycle()
        fft_parser = FFT_1D(fft_1d_funct, 10, 600)
        freq, amp, phase = fft_parser.get_freq_amp_phase(peak_threshold=peak_threshold)
        for i in range(len(freq)):
            ep.push_back(amp[i], freq[i], phase[i])
        amps = ep.get_amps()
    elif choice == 'FFT2':
        epX = Epicycle()
        epY = Epicycle()
        fft_parser = FFT_2D_DOUBLE(pts)
        freqX, freqY, ampX, ampY, phaseX, phaseY = fft_parser.get_freq_amp_phase(peak_threshold=peak_threshold)
        for i in range(len(freqX)):
            epX.push_back(ampX[i], freqX[i], phaseX[i])
        for i in range(len(freqY)):
            epY.push_back(ampY[i], freqY[i], phaseY[i])
    elif choice == 'FFT3':
        fft_parser = FFT_2D_PURE(pts)
        freq, amp, phase = fft_parser.get_freq_amp_phase(peak_threshold=peak_threshold)
        ep = Epicycle()
        for i in range(len(freq)):
            ep.push_back(amp[i], freq[i], phase[i])


redraw()
prev_time = pygame.time.get_ticks()

# pygame start
while True:
    surface.fill((0, 0, 0))  # clear screen
    total_time += time_scale * (pygame.time.get_ticks() - prev_time)
    prev_time = pygame.time.get_ticks()  # update time

    # update user input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MIDIOUT:  # adding user pts
            if isAdding:
                user_pts.append(
                    (-numpy.array(pygame.mouse.get_pos()) + numpy.array([zero[0], -zero[1] + height])) / scale)
        if event.type == pygame.MOUSEWHEEL:
            if state != 0:
                if state == 1:
                    peak_threshold = max(0.0, peak_threshold + event.y / 10.0)
                if state == 2:
                    dist_from_origin += event.y * 5
                    translate3 = numpy.array([0, dist_from_origin], dtype=numpy.int32)
                    translate = numpy.array([-dist_from_origin, 0], dtype=numpy.int32)
                if state == 3:
                    num_of_points = max(0, num_of_points + event.y * 20)
                if state == 4:
                    time_scale = max(0.0, time_scale + event.y * 0.00001)
        if event.type == pygame.MOUSEMOTION:
            if movementUnlocked and not isScalling:  # joystick camera move
                pos[0] += -event.rel[0] / sensitivity
                pos[1] += event.rel[1] / sensitivity
            if isScalling:  # change scale using mouse
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
            if event.key in {pygame.K_KP_ENTER, pygame.K_r}:
                points.clear()
                pointsX.clear()
                pointsY.clear()
                redraw()
            if event.key == pygame.K_SPACE:
                time_scale, prev_timescale = prev_timescale, time_scale
            if event.key == pygame.K_e:
                user_pts.clear()
            if event.key == pygame.K_s:
                isShowing = not isShowing
            if event.key == pygame.K_F1:
                isPrintingInfo = not isPrintingInfo
            if event.key == pygame.K_p:
                state = 1
            if event.key == pygame.K_t:
                state = 4
            if event.key == pygame.K_d:
                state = 2
            if event.key == pygame.K_n:
                state = 3
            if event.key == pygame.K_m:
                choice = f'FFT{(int(choice[3]) + 1) % 3 + 1}'
                points.clear()
                pointsX.clear()
                pointsY.clear()
                redraw()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_c:
                isScalling = False
            if event.key in {pygame.K_p, pygame.K_d, pygame.K_t, pygame.K_n}:
                state = 0

    # translate
    zero += numpy.array([pos[0], pos[1]], dtype=numpy.int32)
    if choice == 'FFT1':
        coords = ep.get_points(total_time)
        points.append(coords[-1][1])
        if len(points) > num_of_points + 10:
            points.remove(points[0])
        for i in range(len(coords[:-1])):
            if (int(amps[i] * scale) > 0):  # draw circles
                pygame.draw.circle(surface, circle_secondary_color,
                                   zero + translate + numpy.array(scale * coords[i], dtype=numpy.int32),
                                   int(amps[i] * scale), 1)
            if i != 0:  # connect centers
                pygame.draw.line(surface, circle_primary_color,
                                 zero + translate + numpy.array(scale * coords[i], dtype=numpy.int32),
                                 zero + translate + numpy.array(scale * coords[i - 1], dtype=numpy.int32), 2)
        if len(coords) > 1:
            pygame.draw.line(surface, circle_primary_color,
                             zero + translate + numpy.array(scale * coords[-1], dtype=numpy.int32),
                             zero + translate + numpy.array(scale * coords[-2], dtype=numpy.int32), 2)
        pygame.draw.line(surface, render_pts_color,  # connect last center to drawing
                         translate + zero + numpy.array(coords[-1] * scale, dtype=numpy.int32),
                         ((zero)[0] + translate2[0], ((zero)[1] + translate2[1] + int(scale * points[-1]))), 1)
        for i in range(-1, -len(points[:num_of_points]), -1):  # render points
            surface.set_at((zero[0] - i + translate2[0], zero[1] + int(scale * points[i]) + translate2[1]),
                           render_pts_color)
    elif choice == 'FFT2':
        coordsX = epX.get_points(total_time)
        coordsY = epY.get_points(total_time)
        pointsX.append(coordsX[-1][0])
        pointsY.append(coordsY[-1][0])
        if len(pointsX) > num_of_points + 10:
            pointsX.remove(pointsX[0])
        if len(pointsY) > num_of_points + 10:
            pointsY.remove(pointsY[0])
        for i in range(len(coordsX[:-1])):
            if (int(ampX[i] * scale) > 0):  # draw circles
                pygame.draw.circle(surface, circle_secondary_color,
                                   zero + translate3 - numpy.array(scale * coordsX[i], dtype=numpy.int32),
                                   int(ampX[i] * scale), 1)
            if i != 0:  # connect centers
                pygame.draw.line(surface, circle_primary_color,
                                 zero + translate3 - numpy.array(coordsX[i] * scale, dtype=numpy.int32),
                                 zero + translate3 - numpy.array(scale * coordsX[i - 1], dtype=numpy.int32), 2)
            if (int(ampY[i] * scale) > 0):  # draw circles
                pygame.draw.circle(surface, circle_secondary_color,
                                   zero + translate + numpy.array(scale * numpy.array([coordsY[i][1], coordsY[i][0]]),
                                                                  dtype=numpy.int32), int(ampY[i] * scale), 1)
            if i != 0:  # connect centers
                pygame.draw.line(surface, circle_primary_color,
                                 zero + translate + numpy.array(scale * numpy.array([coordsY[i][1], coordsY[i][0]]),
                                                                dtype=numpy.int32), zero + translate + numpy.array(
                        scale * numpy.array([coordsY[i - 1][1], coordsY[i - 1][0]]), dtype=numpy.int32), 2)
        if len(coordsX) > 1:
            pygame.draw.line(surface, circle_primary_color,
                             zero + translate3 - numpy.array(coordsX[-1] * scale, dtype=numpy.int32),
                             zero + translate3 - numpy.array(scale * coordsX[-2], dtype=numpy.int32), 2)
        if len(coordsY) > 1:
            pygame.draw.line(surface, circle_primary_color,
                             zero + translate + numpy.array(scale * numpy.array([coordsY[-1][1], coordsY[-1][0]]),
                                                            dtype=numpy.int32),
                             zero + translate + numpy.array(scale * numpy.array([coordsY[-2][1], coordsY[-2][0]]),
                                                            dtype=numpy.int32), 2)
        pygame.draw.line(surface, render_pts_color,  # connect last center to drawing
                         zero + translate3 - numpy.array(scale * coordsX[-1], dtype=numpy.int32),
                         zero + numpy.array(scale * numpy.array([-pointsX[-1], pointsY[-1]])), 1)
        pygame.draw.line(surface, render_pts_color,  # connect last center to drawing
                         zero + translate + numpy.array(scale * numpy.array([coordsY[-1][1], coordsY[-1][0]]),
                                                        dtype=numpy.int32),
                         zero + numpy.array(scale * numpy.array([-pointsX[-1], pointsY[-1]]), dtype=numpy.int32), 1)
        for i in range(-1, -len(pointsX[:num_of_points]), -1):  # render points
            surface.set_at((zero[0] - int(scale * pointsX[i]), zero[1] + int(scale * pointsY[i])),
                           circle_primary_color)
    elif choice == 'FFT3':
        coords = ep.get_points(total_time)
        points.append(coords[-1])
        if len(points) > num_of_points + 10:
            points.remove(points[0])
        for i in range(len(coords[:-1])):
            if (int(amp[i] * scale) > 0):  # draw circles
                pygame.draw.circle(surface, circle_secondary_color,
                                   zero + numpy.array([coords[i][0] * -scale, coords[i][1] * scale], dtype=numpy.int32),
                                   int(amp[i] * scale), 1)
            if i != 0:  # connect centers
                pygame.draw.line(surface, circle_primary_color,
                                 zero + numpy.array([-scale * coords[i][0], scale * coords[i][1]], dtype=numpy.int32),
                                 zero + numpy.array([-scale * coords[i - 1][0], scale * coords[i - 1][1]],
                                                    dtype=numpy.int32), 1)
        if len(coords) > 1:
            pygame.draw.line(surface, circle_primary_color,
                             zero + numpy.array([-scale * coords[-1][0], scale * coords[-1][1]], dtype=numpy.int32),
                             zero + numpy.array([-scale * coords[-2][0], scale * coords[-2][1]], dtype=numpy.int32),
                             1)
        for i in range(-1, -len(points[:num_of_points]), -1):  # render points
            surface.set_at((zero[0] - int(scale * points[i][0]), zero[1] + int(scale * points[i][1])),
                           render_pts_color)
    if choice != 'FFT1' and isShowing:  # render original pts
        for i in range(len(user_pts)):
            surface.set_at((zero[0] - int(scale * user_pts[i][0]), zero[1] + int(scale * user_pts[i][1])),
                           user_pts_color)

    # render epicycles
    surface = pygame.transform.flip(surface, False, True)
    screen.blit(surface, (0, 0))

    # fonts render
    if isPrintingInfo:
        info = font.render(f'timescale: {round(time_scale, 6)}', True, info_color)
        screen.blit(info, (0, 0))
        info = font.render(f'num of points: {num_of_points}', True, info_color)
        screen.blit(info, (0, 30))
        info = font.render(f'dist from origin: {dist_from_origin}', True, info_color)
        screen.blit(info, (0, 60))
        info = font.render(f'showing user pts: {isShowing}', True, info_color)
        screen.blit(info, (0, 90))
        info = font.render(f'total user pts: {len(user_pts)}', True, info_color)
        screen.blit(info, (0, 120))
        info = font.render(f'peak threshold: {round(peak_threshold, 2)}', True, info_color)
        screen.blit(info, (0, 150))
        info = font.render(f'render mode: {choice}', True, info_color)
        screen.blit(info, (0, 180))
    pygame.display.flip()
    fpsClock.tick(fps)  # try to keep fps
