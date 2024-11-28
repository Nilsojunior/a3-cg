import math

from OpenGL.GL import *
from OpenGL.GLU import *


class Camera:
    def __init__(self):
        self.position = [0.0, 0.0, -5.0]
        self.rotation = [0.0, 0.0, 0.0]
        self.zoom = 5.0
        self.zoom_speed = 0.5
        self.min_zoom = 0.1
        self.max_zoom = 20.0

        self.orbit_speed = 0.3
        self.orbit_distance = 5.0
        self.target = [0.0, 0.0, 0.0]
        self.phi = 0  # Vertical
        self.theta = 0  # Horizontal

        # Limites
        self.min_phi = -89.0
        self.max_phi = 89.0

    def apply(self):
        glLoadIdentity()

        # Calculos da camera
        self.position[0] = (
            self.orbit_distance
            * math.cos(math.radians(self.phi))
            * math.cos(math.radians(self.theta))
        )
        self.position[1] = self.orbit_distance * math.sin(math.radians(self.phi))
        self.position[2] = (
            self.orbit_distance
            * math.cos(math.radians(self.phi))
            * math.sin(math.radians(self.theta))
        )

        gluLookAt(
            self.position[0],
            self.position[1],
            self.position[2],
            self.target[0],
            self.target[1],
            self.target[2],
            0,
            1,
            0,
        )

    def orbit(self, dx, dy):
        self.theta += dx * self.orbit_speed
        self.phi += dy * self.orbit_speed

        self.phi = max(self.min_phi, min(self.max_phi, self.phi))

        # 360 graus
        self.theta %= 360

    def zoom_in(self):
        self.orbit_distance = max(self.min_zoom, self.orbit_distance - self.zoom_speed)

    def zoom_out(self):
        self.orbit_distance = min(self.max_zoom, self.orbit_distance + self.zoom_speed)
