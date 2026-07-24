import arcade
import time
from clases.salas.tuberias.sala_tuberias import Sala_Tuberias
from sala_instanciada import SalaActualView

class Manager(arcade.View):
    def __init__(self):
        super().__init__()
        self.sala_actual = "ninguna" # Inicialmente no hay sala activa
        self.sprite_transicion = None
        self.fondo_transicion = None
        self.temporizador_inicio = 0.0

    def on_show_view(self):
        # Configuramos el color de fondo por defecto
        arcade.set_background_color(arcade.color.BLACK)
        self.temporizador_inicio = time.time()

    def on_update(self, delta_time):
        # Aquí puedes manejar la lógica de transición entre salas si es necesario
        if self.sala_actual == "ninguna":
            if time.time() - self.temporizador_inicio > 1.0:  # Esperamos 1 segundo antes de iniciar la primera sala
                # Si no hay sala activa, iniciamos con la sala de tuberías
                self.sala_actual = "tuberias"
                self.sala = SalaActualView(Sala_Tuberias(), self)
                self.window.show_view(self.sala)
        elif self.sala_actual == "tuberias":

            from victoria import VictoriaView
            victoria_view = VictoriaView()
            self.window.show_view(victoria_view)

    def on_draw(self):
        self.clear()
        # Aquí puedes dibujar elementos comunes a todas las salas si es necesario
        # Por ejemplo, un fondo o un HUD que se mantenga constante