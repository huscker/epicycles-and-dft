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

pts = update_data(get_points('''45.08068399876785,3.999387301829052
41.19878328185338,4.708950205719096
38.07592481459808,7.1453261371326455
34.720998197337856,8.918902805877565
31.184784631821405,10.75593219525974
28.17852742171246,13.385774932068319
25.753822586440027,16.554089330099405
23.851742103302353,20.084108128048218
22.32626575003004,23.717507075846196
21,27.371850994354247
18.539348978879406,29.96282108263125
16.36118411608088,33.26889558365935
16.18683201980591,37.2046756229248
18.07150863348007,40.69394768263245
17.044312662638188,44.377747492855555
17.43807167651987,47.80098159094143
15.509335551963806,51.29958462184906
13.40459639176941,54.690865650535585
14.020107744066358,58.30885188857299
17.266229634650706,60.60206500611973
19.227337703801453,63.80243281953299
22.09270036713934,66.50419110160088
24.792702733698846,69.37528005333377
26.748027950438626,72.10636705275957
28.744140999999996,71.07122268633843
32.368677287597656,70.83635129296874
30.72802047381847,68.96180192203236
26.826739951351165,68.17036712116241
23.87637989559174,65.60616395931244
20.95909543921423,63.04278708960247
22.522986731742918,61.917001994896765
26.504161559064986,61.97233005820507
30.505678384944037,61.68670062755885
34.41501012818527,60.8804523254776
34.841271935533676,58.549624287894254
30.99612891706959,59.60302178419948
27.020891418129025,59.95229970115471
23.011545452911882,59.951280502219525
19.106251876485825,59.19560699006844
15.687583649116515,57.17762086860656
16.290947564281463,53.643440716770165
18.33892215639764,50.235422718058466
21.081950248046876,48.42810269140625
25.077559266201035,48.57212237455946
29.055275818529726,49.0539633656106
32.946416691344425,49.969392922617615
36.583664456481934,51.58294959863281
39.636560722461226,54.15111885462362
41.57229805137253,57.60956508267641
42.123985093345475,61.54354285792141
43.972252062646625,59.57836276864266
42.96231801560307,55.73084634388053
40.736259680091855,52.43447301576519
37.64806032382202,49.88959581722641
34.04071945951748,48.201172495897325
30.17981852557007,47.18003857903176
26.203637416259767,46.62769015750122
22.21000911542511,46.5
19.108557192207336,44.494742194767
20.730442115294935,41.23272817577136
24.700940927926066,41
28.717203548338887,41
31.315101126475334,43.87785910374498
34.862025282057765,45.64954570979929
38.823192340293105,45.7210784889886
42.44315205537255,44.07535874871515
45.0001162375399,41.04691277770679
45.996267881729025,37.20872557077448
45.22506879007661,33.317089439292374
42.84274162230551,30.14555647207981
39.33823486962505,28.30127351965594
35.37674900082225,28.140578447947433
31.72257019306644,29.703973807642498
28.93440397202692,30.0509959173942
25.44919049993116,28.201046578944506
23.055768340826035,26.498344661483763
24.8470618092736,22.994708135234593
26.45640587298961,19.32338254091421
28.610841316747628,15.9614510533967
31.378305140448745,13.079690923765309
34.7799152439233,11.016895919802558
38.643686736865995,10.062215874919891
42.63361762781743,10.200491439613305
46.57520439687415,10.910929822543807
50.378377323974604,12.139876892822265
49.03744518620733,15.720318578413222
51.47531245019531,15.575476078125
53.527342135513784,13.729493557797909
54.81394010116053,16.554069839354042
55.668169937092884,18.74447825493843
57.944512923844336,17.95553103908205
59.54413454381239,21.615834744027914
59.99999537409592,25.57888195100403
59.87659401094073,29.564911990357636
59.20301674198302,33.507672801260874
58.04986325833893,37.343731079357624
57.928074905458715,33.720207943643516
55.0501706484375,34.98618469342041
52.61288880143738,38.15020833592713
50.16540807718194,41.3314429489995
52.35163023483641,41.76897059682371
54.79443376509969,38.59808865539071
56,39.060798480468755
56,43.05973456945134
55.005848339557446,46.89378547067347
52.02347195227141,49.19722283480556
54.75724649355793,49.21757289137268
58.50403221435547,49.66166113305665
57.9762564190979,53.229352148468024
54.25576734568955,54.462581054544216
53.61423461343384,58.06717740191651
53.949644856990815,62.05619069587708
54.40226061454928,66.0308511179854
55.05324141663653,69.9714349314983
56.914499923195265,72.94832587890615
56.96844074499512,69.32219280526733
56.338507901393655,65.3740715820362
55.894120723374,61.38770504052531
55.57921747367095,57.39996270079803
58.23785833692169,55.439925997574335
60.877952970214366,52.55930528341007
60.272435815581794,48.701933618477824
57.12797531970054,46.768375181898776
58.55295143839061,43.064310657237414
60.99625799530792,39.892758668067934
62,40.94035073509836
62,44.944583831653595
64,44.23504207699299
64,40.230327983817325
64,36.23708174763584
61.63827534700012,35.779806909194946
60.2905172339201,36.778544140160086
61.389171287948614,32.94427948075867
61.92181686638442,28.972222254004986
61.994507384297215,24.975756695222778
61.447880596926105,21.026422801127225
59.909079863047225,17.33463046668932
57.88825119568253,14.086447989545823
57.63227864676577,10.128626749967783
55.44973677750397,6.848002526277543
51.90435204236602,5.109350876190566
48.03062016692352,4.749723843760681
45.0145759119339,6.006887099525976
44.542225101562494,7.958488205078124
40.78006157128191,8.032066876089669
42.69995046338624,6.26267196028518
53.395186852737424,7.81550601219101
55.77322599424409,10.921648874402141
54.410773930766105,11.920959239230157
52.112529790722846,9.106600337094068
49.634587171978,8.58333179756012
47.94589522567988,9.211047617484521
48.48432076830673,7.441494649832535
40.73486467899609,31.05946948195043
43.3485014777422,34.006126589035034
43.932382011624334,37.923950061081406
42.29791919368744,41.50543998098374
38.973373463496856,43.628124578336745
35.026626536503144,43.628124578336745
31.70208080631256,41.50543998098373
30.067617988375666,37.923950061081406
30.651498522257803,34.006126589035034
33.26513532100391,31.05946948195043
23.75662460767973,30.000378883340954
27.42423548957622,31.374952225956555
28.274829321777347,34.773345570800785
28.1924785078125,38.75142393359375
24.518873407896997,39
20.53098561046982,39.204560621246344
18.159704978242875,36.860554780858514
18.641912143188527,32.98039615045061
21.57791859658989,30.391489678601555
22.084858209609983,36.00169769859314
24.53474562072754,37.58564793395996
38.08950761413574,36.056934768676754
38.21616366386414,38.97314486503601
39.42589985656738,36.32006098937988
41.99838642767334,65.67007027319336
38.76562034234619,67.20151044018554
40.472880499999995,67.43375909912109
35.79570200390625,70.48049914257813'''))
choice = 'FFT2'

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

    surface = pygame.transform.flip(surface,False,True)
    screen.blit(surface,(0,0))
    pygame.display.flip()
    fpsClock.tick(fps)


