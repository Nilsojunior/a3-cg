from OpenGL.GL import *

from texture import Texture


class Model:
    def __init__(self, filename, texture_file):
        self.vertices = []
        self.texcoords = []

        self.normals = []
        self.faces = []
        self.position = [0.0, 0.0, 0.0]
        self.rotation = [0.0, 0.0, 0.0]
        self.scale = 1.0
        self.display_list = None

        self.load_model(filename)
        self.texture = Texture(texture_file)
        self.create_display_list()

    def load_model(self, filename):
        try:
            with open(filename, "r") as file:
                for line in file:
                    if line.startswith("#"):
                        continue
                    values = line.split()
                    if not values:
                        continue

                    if values[0] == "v":
                        self.vertices.append(list(map(float, values[1:4])))
                    elif values[0] == "vt":
                        self.texcoords.append(list(map(float, values[1:3])))
                    elif values[0] == "vn":
                        self.normals.append(list(map(float, values[1:4])))
                    elif values[0] == "f":
                        face = []
                        texcoords = []
                        norms = []
                        for v in values[1:]:
                            w = v.split("/")
                            face.append(int(w[0]))
                            if len(w) >= 2 and len(w[1]) > 0:
                                texcoords.append(int(w[1]))
                            if len(w) >= 3 and len(w[2]) > 0:
                                norms.append(int(w[2]))
                        self.faces.append((face, texcoords, norms))

        except Exception as e:
            raise Exception(f"Error loading model {filename}: {str(e)}")

    def create_display_list(self):
        self.display_list = glGenLists(1)
        glNewList(self.display_list, GL_COMPILE)

        glEnable(GL_TEXTURE_2D)
        self.texture.bind()

        # Efeito Smooth
        glShadeModel(GL_SMOOTH)

        glBegin(GL_TRIANGLES)
        for face in self.faces:
            vertices, texcoords, normals = face
            for i in range(len(vertices)):
                if normals and i < len(normals):
                    glNormal3fv(self.normals[normals[i] - 1])

                if texcoords and i < len(texcoords):
                    glTexCoord2fv(self.texcoords[texcoords[i] - 1])

                glVertex3fv(self.vertices[vertices[i] - 1])
        glEnd()

        glDisable(GL_TEXTURE_2D)
        glEndList()

    def set_position(self, x, y, z):
        self.position = [x, y, z]

    def set_rotation(self, x, y, z):
        self.rotation = [x, y, z]

    def set_scale(self, scale):
        self.scale = scale

    def render(self):
        glPushMatrix()

        glTranslatef(*self.position)
        glRotatef(self.rotation[0], 1, 0, 0)  # X
        glRotatef(self.rotation[1], 0, 1, 0)  # Y
        glRotatef(self.rotation[2], 0, 0, 1)  # Z
        glScalef(self.scale, self.scale, self.scale)

        # Renderizacao com display list
        glCallList(self.display_list)

        glPopMatrix()

    # Destrutor
    def cleanup(self):
        if self.display_list is not None:
            glDeleteLists(self.display_list, 1)
            self.display_list = None
        if hasattr(self, "texture"):
            self.texture.delete()
