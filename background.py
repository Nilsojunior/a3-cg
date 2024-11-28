from OpenGL.GL import *

from texture import Texture


class Background:
    def __init__(self, image_path):
        self.texture = Texture(image_path)

        # Nao repetir a textura
        self.texture.set_wrap_mode(GL_CLAMP_TO_EDGE, GL_CLAMP_TO_EDGE)

        self.depth = -2.0
        self.width_ratio = 1.6
        self.height_ratio = 1.2

        self.setup_geometry()

    def setup_geometry(self):

        # Vertices para o background
        self.vertices = [
            [-self.width_ratio, -self.height_ratio, self.depth],  # Esquerda baixo
            [self.width_ratio, -self.height_ratio, self.depth],  # Direita baixo
            [self.width_ratio, self.height_ratio, self.depth],  # Encima direita
            [-self.width_ratio, self.height_ratio, self.depth],  # Encima esquerda
        ]

        self.texcoords = [
            [0.0, 0.0],  # Esquerda baixo
            [1.0, 0.0],  # Direita baixo
            [1.0, 1.0],  # Encima direita
            [0.0, 1.0],  # Encima esquerda
        ]

    def render(self):
        glPushAttrib(GL_ENABLE_BIT | GL_DEPTH_BUFFER_BIT)
        glPushMatrix()

        glLoadIdentity()

        # Sem isso o background cobre o modelo
        glDisable(GL_DEPTH_TEST)
        glDepthMask(GL_FALSE)

        # Textura
        glEnable(GL_TEXTURE_2D)
        self.texture.bind()

        # Cubo do background
        glBegin(GL_QUADS)
        for i in range(4):
            glTexCoord2fv(self.texcoords[i])
            glVertex3fv(self.vertices[i])
        glEnd()

        glDepthMask(GL_TRUE)
        glEnable(GL_DEPTH_TEST)
        glDisable(GL_TEXTURE_2D)
        glPopMatrix()
        glPopAttrib()

    # Destrutor
    def cleanup(self):
        if hasattr(self, "texture"):
            self.texture.delete()

    def set_depth(self, depth):
        self.depth = depth
        self.setup_geometry()

    def set_aspect_ratio(self, width_ratio, height_ratio):
        self.width_ratio = width_ratio
        self.height_ratio = height_ratio
        self.setup_geometry()
