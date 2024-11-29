import math

import pygame as pg
from OpenGL.GL import *
from OpenGL.GLU import *


class Lightning:
    def __init__(self, intensity=1.0, color=(1.0, 1.0, 1.0)):
        self.intensity = intensity
        self.color = color

    def apply(self):

        # Aplicar iluminacao
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)

        # Cor e posicao
        glLightfv(GL_LIGHT0, GL_POSITION, (0.0, 1.0, 0.0, 0.0))
        glLightfv(GL_LIGHT0, GL_DIFFUSE, self.color)
        glLightfv(GL_LIGHT0, GL_SPECULAR, self.color)

        # Intensidade
        glLightf(GL_LIGHT0, GL_CONSTANT_ATTENUATION, self.intensity)

    def update(self):

        # Variar iluminacao
        self.intensity = 0.5 + 0.5 * math.sin(pg.time.get_ticks() / 100.0)
