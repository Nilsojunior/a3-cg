import cv2
from OpenGL.GL import *


class Texture:
    def __init__(self, filename):
        self.texture_id = None
        self.width = 0
        self.height = 0
        self.load_texture(filename)

    def load_texture(self, filename):
        img = cv2.imread(filename, cv2.IMREAD_UNCHANGED)
        if img is None:
            raise Exception(f"Failed to load texture: {filename}")

        self.height, self.width = img.shape[:2]

        # Conversoes de cor
        if len(img.shape) == 2:  # Grayscale
            img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGRA)
        elif img.shape[2] == 3:  # BGR
            img = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
        elif img.shape[2] == 4:  # BGRA
            pass

        # Inverter imagem para o OpenGL
        img = cv2.flip(img, 0)

        # Byte para string
        img_data = img.tobytes()

        # Textura OpenGL
        self.texture_id = glGenTextures(1)
        self.bind()

        # Parametros da textura
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)

        # Criar textura
        glTexImage2D(
            GL_TEXTURE_2D,
            0,
            GL_RGBA,
            self.width,
            self.height,
            0,
            GL_BGRA,
            GL_UNSIGNED_BYTE,
            img_data,
        )

    def bind(self):
        glBindTexture(GL_TEXTURE_2D, self.texture_id)

    def set_wrap_mode(self, wrap_s, wrap_t):
        self.bind()
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, wrap_s)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, wrap_t)

    # Destrutor
    def delete(self):
        if self.texture_id is not None:
            glDeleteTextures([self.texture_id])
            self.texture_id = None
