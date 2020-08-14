import numpy


class Epicycle:
    def __init__(self):
        self.children = list()
    def push_back(self,amp,freq,phase):
        self.children.append(numpy.array([amp,freq,phase]))

    def get_amps(self):
        return [i[0] for i in self.children]
    def get_points(self,time):
        coords = numpy.array([0.0,0.0])
        res = list()
        res.append(numpy.array([0.0,0.0]))
        for i in self.children:
            coords += numpy.array([numpy.cos(time*i[1]+i[2]+numpy.pi),numpy.sin(time*i[1]+i[2]+numpy.pi)])*i[0]
            res.append(numpy.array(coords))
        return res
