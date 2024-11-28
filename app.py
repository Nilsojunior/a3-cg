import os

import pygame as pg
from OpenGL.GL import *
from OpenGL.GLU import *
from pygame.locals import *

from background import Background
from camera import Camera
from input import Input
from lightning import Lightning
from model import Model


class ResourceManager:
    def __init__(self):
        self.models = {}
        self.textures = {}
        self.background = None
        self.assets_path = "assets"

    def load_resources(self):
        try:
            background_path = os.path.join(self.assets_path, "Background.png")
            self.background = Background(background_path)

            sword_obj_path = os.path.join(self.assets_path, "Sword.obj")
            sword_texture_path = os.path.join(self.assets_path, "Sword.png")
            self.models["sword"] = Model(sword_obj_path, sword_texture_path)

        except Exception as e:
            print(e)
            pg.quit()
            return False
        return True

    # Destrutor
    def cleanup(self):
        if self.background and hasattr(self.background, "texture"):
            self.background.texture.delete()

        for model in self.models.values():
            if hasattr(model, "texture"):
                model.texture.delete()


def setup_opengl(display):
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_CULL_FACE)
    glCullFace(GL_BACK)
    glShadeModel(GL_SMOOTH)

    # Vsync
    pg.display.gl_set_attribute(pg.GL_SWAP_CONTROL, 1)

    glMatrixMode(GL_PROJECTION)
    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    glMatrixMode(GL_MODELVIEW)

    # glClearColor(0.0, 0.0, 0.0, 0)


class App:
    def __init__(self):
        self.width = 1500
        self.height = 800
        self.display = (self.width, self.height)
        self.running = False
        self.clock = pg.time.Clock()
        self.fps = 60
        self.frame_count = 0
        self.last_time = 0
        self.rotation_angle = 0

        self.resource_manager = ResourceManager()
        self.camera = Camera()
        self.input = Input()
        self.lightning = Lightning(intensity=1.0, color=(1.0, 1.0, 1.0))

    def setup_display(self):
        pg.init()
        pg.display.gl_set_attribute(pg.GL_DEPTH_SIZE, 24)
        pg.display.set_mode(self.display, DOUBLEBUF | OPENGL)

        setup_opengl(self.display)

        if not self.resource_manager.load_resources():
            return False

        self.input.print_controls()

        self.last_time = pg.time.get_ticks()
        return True

    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
                return

            self.input.handle_events(
                event, self.resource_manager.models["sword"], self.camera
            )

    def update(self):
        current_time = pg.time.get_ticks()

        # FPS display
        self.frame_count += 1
        if current_time - self.last_time > 1000:
            fps = self.frame_count
            pg.display.set_caption(f"A3 CG | FPS: {fps}")
            self.frame_count = 0
            self.last_time = current_time

        if self.input.rotation_xyz[0]:
            self.resource_manager.models["sword"].rotation[0] += 0.3
        elif self.input.rotation_xyz[1]:
            self.resource_manager.models["sword"].rotation[1] += 0.3
        elif self.input.rotation_xyz[2]:
            self.resource_manager.models["sword"].rotation[2] += 0.3

        # Atualizar iluminacao
        self.lightning.update(current_time)

    def render(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Remover iluminacao para aplicar o background
        glDisable(GL_LIGHTING)
        if self.resource_manager.background:
            self.resource_manager.background.render()

        # Aplicar iluminacao de volta
        glEnable(GL_LIGHTING)

        # Aplicar iluminacao antes de renderizar o cenario
        self.lightning.apply()

        self.camera.apply()

        glPushMatrix()
        glRotatef(self.rotation_angle, 0, 1, 0)
        self.resource_manager.models["sword"].render()
        glPopMatrix()

        pg.display.flip()

    def run(self):
        if not self.setup_display():
            return

        self.running = True
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(self.fps)

        # Destrutor
        self.resource_manager.cleanup()
        pg.quit()


def main():
    app = App()
    app.run()


if __name__ == "__main__":
    main()
