import pygame as pg


class Input:
    def __init__(self):
        self.controls = {
            # Rotacao
            "rotate_left": pg.K_a,
            "rotate_right": pg.K_d,
            "rotate_up": pg.K_w,
            "rotate_down": pg.K_s,
            # Escala
            "scale_up": pg.K_EQUALS,
            "scale_down": pg.K_MINUS,
            # Zoom
            "zoom_in": pg.K_q,
            "zoom_out": pg.K_e,
            # Translacao
            "translate_left": pg.K_LEFT,
            "translate_right": pg.K_RIGHT,
            "translate_up": pg.K_UP,
            "translate_down": pg.K_DOWN,
            "translate_forward": pg.K_f,
            "translate_backwards": pg.K_b,
            # Alternar rotacao de eixo
            "toggle_rotation_x": pg.K_x,
            "toggle_rotation_y": pg.K_y,
            "toggle_rotation_z": pg.K_z,
        }

        self.rotation_value = 5
        self.scale_value = 1.1
        self.translation_value = 0.1

        self.mouse_dragging = False
        self.last_mouse_pos = None

        self.rotation_xyz = [False, False, False]

    def keyboard_input(self, event, model, camera):
        if event.type == pg.KEYDOWN:
            key = event.key

            if key == self.controls["rotate_left"]:
                model.rotation[1] -= self.rotation_value
            elif key == self.controls["rotate_right"]:
                model.rotation[1] += self.rotation_value
            elif key == self.controls["rotate_up"]:
                model.rotation[0] -= self.rotation_value
            elif key == self.controls["rotate_down"]:
                model.rotation[0] += self.rotation_value

            elif key == self.controls["scale_up"]:
                model.scale *= self.scale_value
            elif key == self.controls["scale_down"]:
                model.scale /= self.scale_value

            elif key == self.controls["zoom_in"]:
                camera.zoom_in()
            elif key == self.controls["zoom_out"]:
                camera.zoom_out()

            elif key == self.controls["translate_left"]:
                model.position[0] -= self.translation_value
            elif key == self.controls["translate_right"]:
                model.position[0] += self.translation_value
            elif key == self.controls["translate_up"]:
                model.position[1] += self.translation_value
            elif key == self.controls["translate_down"]:
                model.position[1] -= self.translation_value
            elif key == self.controls["translate_forward"]:
                model.position[2] += self.translation_value
            elif key == self.controls["translate_backwards"]:
                model.position[2] -= self.translation_value

            elif key == self.controls["toggle_rotation_x"]:
                self.rotation_xyz[0] = not self.rotation_xyz[0]
                print(
                    f"{'Comecando' if self.rotation_xyz[0] else 'Parando'} "
                    "Rotacao de X"
                )
            elif key == self.controls["toggle_rotation_y"]:
                self.rotation_xyz[1] = not self.rotation_xyz[1]
                print(
                    f"{'Comecando' if self.rotation_xyz[1] else 'Parando'} "
                    "Rotacao de Y"
                )
            elif key == self.controls["toggle_rotation_z"]:
                self.rotation_xyz[2] = not self.rotation_xyz[2]
                print(
                    f"{'Comecando' if self.rotation_xyz[2] else 'Parando'} "
                    "Rotacao de Z"
                )

    def mouse_input(self, event, camera):
        if event.type == pg.MOUSEWHEEL:
            if event.y > 0:
                camera.zoom_in()
            else:
                camera.zoom_out()

        elif event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                self.mouse_dragging = True
                self.last_mouse_pos = pg.mouse.get_pos()

        elif event.type == pg.MOUSEBUTTONUP:
            if event.button == 1:
                self.mouse_dragging = False
                self.last_mouse_pos = None

        # Mouse motions
        elif event.type == pg.MOUSEMOTION and self.mouse_dragging:
            current_pos = pg.mouse.get_pos()
            if self.last_mouse_pos:
                dx = current_pos[0] - self.last_mouse_pos[0]
                dy = current_pos[1] - self.last_mouse_pos[1]

                # Invertendo vertical
                camera.orbit(dx, -dy)
            self.last_mouse_pos = current_pos

    def handle_events(self, event, model, camera):
        if event.type in [pg.KEYDOWN]:
            self.keyboard_input(event, model, camera)
        elif event.type in [
            pg.MOUSEWHEEL,
            pg.MOUSEBUTTONDOWN,
            pg.MOUSEBUTTONUP,
            pg.MOUSEMOTION,
        ]:
            self.mouse_input(event, camera)

    def print_controls(self):
        print("Controles do Modelo:")
        print("Rotacionar objeto: WASD")
        print("Transladar objeto: ⬅ ⬆ ⬇ ⮕")
        print("Transladar objeto para frente: F")
        print("Transladar objeto para atras: B")
        print("Aumentar a escala: +")
        print("Diminuir a escala: -")
        print("")
        print("Controles de Camera:")
        print("Rotação da câmera: Clique e arraste o mouse")
        print("Aumentar zoom com o mouse: Roda do mouse para cima")
        print("Diminuir zoom com o mouse: Roda do mouse para baixo")
        print("Aumentar zoom com o teclado: Q")
        print("Diminuir zoom com o teclado: E")
        print("")
        print("Alternar Rotacao de Eixo:")
        print("Alternar rotacao de x: X")
        print("Alternar rotacao de y: Y")
        print("Alternar rotacao de z: Z")
